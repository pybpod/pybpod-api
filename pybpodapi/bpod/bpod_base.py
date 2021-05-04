# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import math
import socket
import sys

from confapp import conf as settings
from datetime import datetime as datetime_now
from pybpodapi.bpod.hardware.hardware import Hardware
from pybpodapi.bpod.hardware.channels import ChannelType
from pybpodapi.bpod.hardware.channels import ChannelName
from pybpodapi.bpod.hardware.events import EventName
from pybpodapi.bpod.hardware.output_channels import OutputChannel

from pybpodapi.bpod.emulator import Emulator

from pybpodapi.bpod_modules.bpod_modules import BpodModules
from pybpodapi.exceptions.bpod_error import BpodErrorException

from pybpodapi.com.messaging.end_trial import EndTrial
from pybpodapi.com.messaging.trial import Trial
from pybpodapi.com.messaging.event_occurrence import EventOccurrence
from pybpodapi.com.messaging.event_resume import EventResume
from pybpodapi.com.messaging.softcode_occurrence import SoftcodeOccurrence
from pybpodapi.com.messaging.session_info import SessionInfo
from pybpodapi.com.messaging.warning import WarningMessage
from pybpodapi.com.messaging.value import ValueMessage
from pybpodapi.com.messaging.state_transition import StateTransition

from pybpodapi.session import Session

from .non_blockingstreamreader import NonBlockingStreamReader
from .non_blockingsocketreceive import NonBlockingSocketReceive

logger = logging.getLogger(__name__)


class BpodBase(object):
    """
    API to interact with Bpod

    :ivar Session session: Session for this bpod running experiment
    :ivar Hardware hardware: Hardware object representing Bpod hardware
    :ivar MessageAPI message_api: Abstracts communication with Bpod box
    :ivar bool new_sma_sent: whether a new state machine was already uploaded to Bpod box
    """

    class Events(EventName):
        pass

    class OutputChannels(OutputChannel):
        pass

    class ChannelTypes(ChannelType):
        pass

    class ChannelNames(ChannelName):
        pass

    CHECK_STATE_MACHINE_COUNTER = 0

    def __init__(self, serial_port=None, sync_channel=None, sync_mode=None, net_port=None, emulator_mode=False):
        self._session = self.create_session()

        self.serial_port = serial_port if serial_port is not None else settings.PYBPOD_SERIAL_PORT
        self.baudrate = settings.PYBPOD_BAUDRATE
        self.sync_channel = sync_channel if sync_channel is not None else settings.PYBPOD_SYNC_CHANNEL
        self.sync_mode = sync_mode if sync_mode is not None else settings.PYBPOD_SYNC_MODE
        self.net_port = net_port if net_port is not None else settings.PYBPOD_NET_PORT
        self._hardware = Hardware()    # type: Hardware
        if emulator_mode:
            self._emulator = Emulator(self._hardware)
            self.__initialize_input_command_handler()
            self.bpod_modules = self._emulator.bpod_modules
        else:
            self._emulator = None
            self.bpod_modules = None          # type: BpodModules
        self.bpod_start_timestamp = None

        self._new_sma_sent = False         # type: bool
        self._skip_all_trials = False

        self._hardware.sync_channel = self.sync_channel  # 255 = no sync, otherwise set to a hardware channel number
        self._hardware.sync_mode = self.sync_mode    # 0 = flip logic every trial, 1 = every state

        self.session += SessionInfo(self.session.INFO_SERIAL_PORT, self.serial_port)
        self.session += SessionInfo(self.session.INFO_PROTOCOL_NAME, settings.PYBPOD_PROTOCOL)
        self.session += SessionInfo(self.session.INFO_CREATOR_NAME, settings.PYBPOD_CREATOR)
        self.session += SessionInfo(self.session.INFO_PROJECT_NAME, settings.PYBPOD_PROJECT)
        self.session += SessionInfo(self.session.INFO_EXPERIMENT_NAME, settings.PYBPOD_EXPERIMENT)
        self.session += SessionInfo(self.session.INFO_BOARD_NAME, settings.PYBPOD_BOARD)
        self.session += SessionInfo(self.session.INFO_SETUP_NAME, settings.PYBPOD_SETUP)
        self.session += SessionInfo(self.session.INFO_BPODGUI_VERSION, settings.PYBPOD_BPODGUI_VERSION)

        if self.net_port:
            self.session += SessionInfo(self.session.INFO_NET_PORT, self.net_port)

        for subject_name in settings.PYBPOD_SUBJECTS:
            self.session += SessionInfo(self.session.INFO_SUBJECT_NAME, subject_name)

        if hasattr(settings, 'PYBPOD_VARSNAMES'):
            for varname in settings.PYBPOD_VARSNAMES:
                self.session += ValueMessage(varname, getattr(settings, varname))

    #########################################
    ############ PUBLIC METHODS #############
    #########################################

    def loop_handler(self):
        """
        handler that will execute on every loop when the bpod is running
        """
        pass

    def open(self):
        """
        Starts Bpod.

        Connect to Bpod board through serial port, test handshake, retrieve firmware version,
        retrieve hardware description, enable input ports and configure channel synchronization.

        Example:

        .. code-block:: python

            my_bpod = Bpod().open("/dev/tty.usbmodem1293", "/Users/John/Desktop/bpod_workspace", "2afc_protocol")

        :param str serial_port: serial port to connect
        :param str workspace_path: path for bpod output files (no folders will be created)
        :param str session_name: this name will be used for output files
        :param int baudrate [optional]: baudrate for serial connection
        :param int sync_channel [optional]: Serial synchronization channel: 255 = no sync, otherwise set to a hardware channel number
        :param int sync_mode [optional]: Serial synchronization mode: 0 = flip logic every trial, 1 = every state
        :return: Bpod object created
        :rtype: pybpodapi.model.bpod
        """

        logger.info("Starting Bpod")

        self._bpodcom_connect(self.serial_port, self.baudrate)

        if not self._bpodcom_handshake():
            raise BpodErrorException('Error: Bpod failed to confirm connectivity. Please reset Bpod and try again.')

        #########################################################
        ### check the firmware version ##############################
        #########################################################
        firmware_version, machine_type = self._bpodcom_firmware_version()

        if firmware_version < int(settings.TARGET_BPOD_FIRMWARE_VERSION):
            raise BpodErrorException('Error: Old firmware detected. Please update Bpod 0.7+ firmware and try again.')

        if firmware_version > int(settings.TARGET_BPOD_FIRMWARE_VERSION):
            raise BpodErrorException('Error: Future firmware detected. Please update the Bpod python software.')

        self._hardware.firmware_version = firmware_version
        self._hardware.machine_type = machine_type
        #########################################################
        self._bpodcom_hardware_description(self._hardware)

        if not self._bpodcom_enable_ports(self._hardware):
            raise BpodErrorException('Error: Failed to enable Bpod inputs.')

        if not self._bpodcom_set_sync_channel_and_mode(sync_channel=self.sync_channel, sync_mode=self.sync_mode):
            raise BpodErrorException('Error: Failed to configure syncronization.')

        # check if any module is connected
        self.bpod_modules = self._bpodcom_get_modules_info(self._hardware)

        self._hardware.setup(self.bpod_modules)

        self.__initialize_input_command_handler()

        return self

    def close(self):
        """
        Close connection with Bpod
        """
        self.session += SessionInfo(self.session.INFO_SESSION_ENDED, datetime_now.now())

        if hasattr(settings, 'PYBPOD_VARSNAMES'):
            for varname in settings.PYBPOD_VARSNAMES:
                self.session += ValueMessage(varname, getattr(settings, varname))

        if self._emulator is None:
            self._bpodcom_disconnect()

        del self._session

        if self.socketin is not None:
            self.socketin.close()
            self.sock.close()

        if self.stdin is not None:
            self.stdin.close()

    def stop_trial(self):
        self._bpodcom_stop_trial()

    def pause(self):
        self._bpodcom_pause_trial()

    def resume(self):
        self._bpodcom_resume_trial()

    def refresh_modules(self):
        # check if any module is connected
        self.bpod_modules = self._bpodcom_get_modules_info(self._hardware)
        self._hardware.setup(self.bpod_modules)

    def register_value(self, name, value):
        self._session += ValueMessage(name, value)

    def send_state_machine(self, sma, run_asap=None):
        """
        Builds message and sends state machine to Bpod

        :param pybpodapi.model.state_machine sma: initialized state machine
        """
        if self._emulator is None and not self.bpod_com_ready:
            raise Exception('Bpod connection is closed')

        if self._skip_all_trials is True:
            return

        logger.info("Sending state machine")

        sma.update_state_numbers()

        if self._emulator:
            self._emulator.set_state_machine(sma)
            self._emulator.log_state_machine_info()
        else:
            state_machine_body = sma.build_message() + sma.build_message_global_timer() + sma.build_message_32_bits()

            self._bpodcom_send_state_machine(sma.build_header(run_asap, len(state_machine_body)) + state_machine_body)

        self._new_sma_sent = True

    def run_state_machine(self, sma):
        """

        Adds a new trial to current session and runs state machine on Bpod box.

        While state machine is running, messages are processed accordingly.

        When state machine stops, timestamps are updated and trial events are processed.

        Finally, data is released for registered data consumers / exporters.

        .. seealso::

            Send command "run state machine": :meth:`pybpodapi.bpod.bpod_base.BpodBase.run_state_machine`.

            Process opcode: :meth:`pybpodapi.bpod.bpod_base.BpodBase._BpodBase__process_opcode`.

            Update timestamps: :meth:`pybpodapi.bpod.bpod_base.BpodBase._BpodBase__update_timestamps`.

        :param (:class:`pybpodapi.state_machine.StateMachine`) sma: initialized state machine
        """
        if self._emulator is None and not self.bpod_com_ready:
            raise Exception('Bpod connection is closed')

        if self._skip_all_trials is True:
            return False

        self.session += Trial(sma)

        logger.info("Running state machine, trial %s", len(self.session.trials))

        self.trial_timestamps = []  # Store the trial timestamps in case bpod is using live_timestamps

        if self._emulator:
            self._emulator.set_state_machine(sma)
            self._emulator.initialize()
            self._emulator.mirror_state(sma.current_state)
            # TODO: Do the BpodSystem.RefreshGUI equivalent
            self.trial_start_timestamp = self._emulator.matrix_start_time
        else:
            self._bpodcom_run_state_machine()
            if self._new_sma_sent:
                if self._bpodcom_state_machine_installation_status():
                    self._new_sma_sent = False
                else:
                    raise BpodErrorException('Error: The last state machine sent was not acknowledged by the Bpod device.', self)
            self.trial_start_timestamp = self._bpodcom_get_trial_timestamp_start()

        if self.bpod_start_timestamp is None:
            self.bpod_start_timestamp = self.trial_start_timestamp

        #####################################################
        # create a list of executed states
        state_change_indexes = []

        pause_task = False
        # flags used to stop a trial (or all trials)
        interrupt_task = False
        kill_task = False

        sma.is_running = True
        while sma.is_running:

            # read commands from the stdin ######################
            if self.stdin is not None:
                inline = self.stdin.readline()
                if inline is not None:
                    pause_task, interrupt_task, kill_task = self.handle_inline(inline, sma)
            #####################################################

            # read commands from a net socket ###################
            if self.socketin is not None:
                inline = self.socketin.readline()

                if inline is not None:
                    inline = inline.decode().strip()
                    pause_task, interrupt_task, kill_task = self.handle_inline(inline, sma)
            #####################################################
            if pause_task:
                continue

            opcode, data = None, None
            if self._emulator:
                opcode, data = self._emulator.run()
            elif self.data_available():
                opcode, data = self._bpodcom_read_opcode_message()
            if opcode is not None and data is not None and \
                not self.__process_opcode(
                    sma, opcode, data, state_change_indexes):
                break

            self.loop_handler()

            if interrupt_task or kill_task:
                self._skip_all_trials = True
                break

        if self._emulator:
            self._emulator.mirror_state(None)

        self.session += EndTrial('The trial ended')

        if not interrupt_task:
            self.__update_timestamps(sma, state_change_indexes)
            self.session.add_trial_events()

        logger.info("Publishing Bpod trial")

        if interrupt_task and kill_task:
            self.close()
            exit(0)

        return not interrupt_task

    def handle_inline(self, inline, sma):
        pause_task = False
        interrupt_task = False
        kill_task = False
        if inline.startswith('pause-trial'):
            if self._emulator:
                pause_task = True
            else:
                self.pause()
        elif inline.startswith('resume-trial'):
            if self._emulator:
                pause_task = False
            else:
                self.resume()
        elif inline.startswith('stop-trial'):
            if self._emulator:
                interrupt_task = True
            else:
                self.stop_trial()
        elif inline.startswith('close'):
            if self._emulator is None:
                self.stop_trial()
            interrupt_task = True
        elif inline.startswith('kill'):
            if self._emulator is None:
                self.stop_trial()
            interrupt_task = kill_task = True
        elif inline.startswith('SoftCode'):
            softcode = int(inline[-1]) - 1
            self.trigger_softcode(softcode)
        elif inline.startswith('trigger_input:'):
            tdata = inline.split(':')
            chn_name = tdata[1]
            evt_data = tdata[2]
            # TODO: surround this call in a try except to capture calls with unavailable channel names
            channel_number = sma.hardware.channels.input_channel_names.index(chn_name)
            self.trigger_input(channel_number, evt_data)
        elif inline.startswith('trigger_output:'):
            tdata = inline.split(':')
            chn_name = tdata[1]
            evt_data = tdata[2]
            # TODO: surround this call in a try except to capture calls with unavailable channel names
            channel_number = sma.hardware.channels.output_channel_names.index(chn_name)
            self.trigger_output(channel_number, evt_data)
        elif inline.startswith('message:'):
            tdata = inline.split(':')
            module_index = int(tdata[1])
            msg = tdata[2]
            final_msg = []
            msg_elems = msg.split()
            if msg_elems[0].startswith('\''):
                final_msg.append(ord(msg_elems[0][1]))
            for x in msg_elems[1:]:
                final_msg.append(int(x))
            self.load_message(module_index, final_msg)

        return pause_task, interrupt_task, kill_task

    def load_serial_message(self, serial_channel, message_ID, serial_message):
        """
        Load serial message on Bpod

        :param int serial_channel: Serial port to send, 1, 2 or 3
        :param int message_ID: Unique id for the message. Should be between 1 and 255
        :param list(int) serial_message: Message to send. The message should be bigger than 3 bytes.
        """
        response = self._bpodcom_load_serial_message(serial_channel, message_ID, serial_message, 1)

        if not response:
            raise BpodErrorException('Error: Failed to set serial message.')

    def reset_serial_messages(self):
        """
        Reset serial messages to equivalent byte codes (i.e. message# 4 = one byte, 0x4)
        """
        response = self._bpodcom_reset_serial_messages()

        if not response:
            raise BpodErrorException('Error: Failed to reset serial message library.')

    def softcode_handler_function(self, data):
        """
        Users can override this function directly on the protocol to handle a softcode from Bpod

        :param int data: soft code number
        """
        pass

    def echo_softcode(self, softcode):
        return self._bpodcom_echo_softcode(softcode)

    def trigger_event_by_name(self, event_name):
        if self._emulator:
            self._emulator.add_manual_override_event(event_name)

    def trigger_event(self, event_index, event_data):
        if self._emulator:
            self._emulator.add_manual_override_event(event_index)
        else:
            return self._bpodcom_manual_override_exec_event(event_index, event_data)

    def trigger_input(self, channel_number, value):
        if self._emulator:
            self._emulator.override_input_state(channel_number, int(value))
        else:
            return self._bpodcom_override_input_state(channel_number, value)

    def trigger_output(self, channel_number, value):
        if self._emulator:
            self._emulator.serial_override(channel_number, int(value))
        else:
            return self._bpodcom_override_digital_hardware_state(channel_number, value)

    def trigger_softcode(self, softcode):
        if self._emulator:
            self.softcode_handler_function(softcode)
        else:
            return self._bpodcom_send_softcode(softcode)

    def trigger_serial(self, channel_number, value):
        if self._emulator:
            self._emulator.serial_override(channel_number, value)
        else:
            return self._bpodcom_send_byte_to_hardware_serial(channel_number, value)

    def load_message(self, module_index, msg):
        # get module reference
        module = [x for x in self.modules if x.serial_port == module_index]
        # call module_write. on module reference
        if module:
            self._bpodcom_module_write(module_index - 1, msg)

    #########################################
    ############ PRIVATE METHODS ############
    #########################################

    def create_session(self):
        return Session()

    def __initialize_input_command_handler(self):
        # Initialize the server to handle commands.
        if self.net_port is None:
            self.sock = None
            self.socketin = None
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(('0.0.0.0', self.net_port))
            self.socketin = NonBlockingSocketReceive(self.sock)

        # Initialize the thread that will handle the stdin commands.
        self.stdin = NonBlockingStreamReader(
            sys.stdin) if settings.PYBPOD_API_ACCEPT_STDIN else None

    def __transition_to_new_state(self, sma, event_id, transition_matrix,
                              current_trial, state_change_indexes,
                              is_state_timer_matrix=False,
                              debug_message=None):
        new_state_set = False

        def set_sma_current_state(new_state):
            previous_state = sma.current_state
            if sma.use_255_back_signal and new_state == 255:
                sma.current_state = current_trial.states[-2]
            else:
                sma.current_state = new_state
            logger.debug(('Transition occured: '
                          f'state {previous_state} -> {sma.current_state}'))
            if not math.isnan(sma.current_state):
                if debug_message is not None:
                    logger.debug(debug_message)
                current_trial.states.append(sma.current_state)
                state_change_indexes.append(
                    len(current_trial.events_occurrences) - 1)
        current_state = sma.current_state
        if is_state_timer_matrix:
            this_state_timer_state = transition_matrix[current_state]
            is_event_id_tup = event_id == sma.hardware.channels.events_positions.Tup
            if is_event_id_tup and this_state_timer_state != current_state:
                set_sma_current_state(this_state_timer_state)
                new_state_set = True
        else:
            for transition_event_code, transition_state in transition_matrix[
                    current_state]:
                if transition_event_code == event_id:
                    set_sma_current_state(transition_state)
                    new_state_set = True
                else:
                    logger.debug((f'Event {transition_event_code} required '
                                  f'for transition: state '
                                  f'{sma.current_state} -> '
                                  f'{transition_state}'))
        return new_state_set

    def __process_opcode(self, sma, opcode, data, state_change_indexes):
        """
        Process data from bpod board given an opcode

        In original bpod, sma.raw_data == raw_events

        :param sma: state machine object
        :param int opcode: opcode number
        :param data: data from bpod board
        :param state_change_indexes:
        :return:
        """

        current_trial = self.session.current_trial

        if opcode == 1:  # Read events
            if self._emulator:
                current_events = data  # virtual current events
                logger.debug(f'virtual_current_events: {current_events}')
            else:
                n_current_events = data
                current_events = self._bpodcom_read_current_events(n_current_events)

            transition_event_found = False

            if self.hardware.live_timestamps and self._emulator is None:
                event_timestamp = self._bpodcom_read_event_timestamp()
            else:
                event_timestamp = None

            for event_id in current_events:
                if event_id == 255:
                    sma.is_running = False
                else:
                    self._session += EventOccurrence(
                        event_id,
                        sma.hardware.channels.get_event_name(event_id),
                        event_timestamp
                    )
                    self.trial_timestamps.append(event_timestamp)

                    logger.debug("Current state: %s", sma.current_state)
                    transition_matrices = {
                        'input': sma.input_matrix,
                        'state_timer': sma.state_timer_matrix,
                        'global_timers_start': sma.global_timers.start_matrix,
                        'global_timers_end': sma.global_timers.end_matrix,
                        'global_counters': sma.global_counters.matrix,
                        'conditions': sma.conditions.matrix,
                    }
                    for transition_matrix_name, transition_matrix in \
                            transition_matrices.items():
                        transition_event_found = \
                            self.__transition_to_new_state(
                                sma,
                                event_id,
                                transition_matrix,
                                current_trial,
                                state_change_indexes,
                                is_state_timer_matrix=(transition_matrix_name ==
                                                       'state_timer'),
                                debug_message="Adding {} matrix states".format(
                                    transition_matrix_name))
                        if transition_event_found:
                            break

                logger.debug("States indexes: %s", current_trial.states)
            if self._emulator:
                self._emulator.mirror_events(current_events)
            if transition_event_found and not math.isnan(sma.current_state):
                if self._emulator:
                    self._emulator.mirror_state(sma.current_state)
                    self._emulator.set_state_machine(sma)
                    self._emulator.reset_current_state()
                    self._emulator.set_state_start_time(
                        self._emulator.current_time)
                    self._emulator.set_global_timer_end_time()
                    self._emulator.cancel_global_timers()
                    self._emulator.reset_global_counter_counts()
                    self._emulator.set_softcode(
                        self.hardware.channels.events_positions.output_USB)
                state_name = sma.state_names[sma.current_state]
                self._session += StateTransition(state_name, event_timestamp)
            elif math.isnan(sma.current_state):
                if self._emulator:
                    state_change_indexes.append(
                        len(current_trial.events_occurrences) - 1)
                    return False

        elif opcode == 2:  # Handle soft code
            self._session += SoftcodeOccurrence(data)
            self.softcode_handler_function(data)

        return True

    def __update_timestamps(self, sma, state_change_indexes):
        """
        Read timestamps from Bpod and update state machine info

        :param StateMachine sma:
        :param list state_change_indexes:
        """

        def add_session_info(trial_start_timestamp, trial_end_timestamp):
            self.session += SessionInfo(
                self.session.INFO_TRIAL_BPODTIME,
                trial_end_timestamp - trial_start_timestamp,
                start_time=trial_start_timestamp,
                end_time=trial_end_timestamp
            )

        current_trial = self.session.current_trial
        if self._emulator:
            trial_start_timestamp = \
                self._emulator.matrix_start_time
            timestamps = self._emulator.timestamps[
                :self._emulator.n_events]
            trial_end_timestamp = \
                trial_start_timestamp + \
                timestamps[-1]
            current_trial.bpod_start_timestamp = trial_start_timestamp
            current_trial.trial_start_timestamp = trial_start_timestamp
            current_trial.trial_end_timestamp = trial_end_timestamp
            add_session_info(current_trial.trial_start_timestamp, trial_end_timestamp)
        else:
            current_trial.trial_start_timestamp = self.trial_start_timestamp  # start timestamp of first trial
            current_trial.bpod_start_timestamp = self.bpod_start_timestamp

            trial_end_timestamp, discrepancy = self._bpodcom_read_timestamps()
            current_trial.trial_end_timestamp = trial_end_timestamp

            add_session_info(current_trial.trial_start_timestamp, trial_end_timestamp)

            if discrepancy > 1:
                self.session += WarningMessage("Bpod missed hardware update deadline(s) on the past trial by ~{milliseconds}ms".format(milliseconds=discrepancy))

            if self.hardware.live_timestamps:
                timestamps = self.trial_timestamps
            else:
                timestamps = self._bpodcom_read_alltimestamps()
                timestamps = [float(t) * self._hardware.times_scale_factor for t in timestamps]
        if (self._emulator) or not self.hardware.live_timestamps:
            # update the timestamps of the events #############################################################
            for event, timestamp in zip(current_trial.events_occurrences, timestamps):
                event.host_timestamp = timestamp
                e = EventResume(event.event_id, event.event_name, host_timestamp=timestamp)
                self.session += e
            ###################################################################################################

        current_trial.event_timestamps = timestamps
        current_trial.state_timestamps += [timestamps[i] for i in state_change_indexes]
        current_trial.state_timestamps += timestamps[-1:]

    def find_module_by_name(self, name):
        """
        Search for a module by name
        """
        for m in self.modules:
            if m.name == name:
                return m
        return None

    #########################################
    ############## PROPERTIES ###############
    #########################################

    @property
    def session(self):
        return self._session  # type: Session

    @session.setter
    def session(self, value):
        self._session = value  # type: Session

    @property
    def hardware(self):
        return self._hardware  # type: Hardware

    @property
    def modules(self):
        return [m for m in self.bpod_modules if m.connected]

    @property
    def skip_all_trials(self) -> bool:
        return self._skip_all_trials

    # @property
    # def inputs(self):
    #   return self._hardware.inputs

    # @property
    # def outputs(self):
    #   return self._hardware.outputs

    # @property
    # def channels(self):
    #   return self._hardware.channels

    # @property
    # def max_states(self):
    #   return self._hardware.max_states

    # @property
    # def max_serial_events(self):
    #   return self._hardware.max_serial_events

    # @property
    # def inputs_enabled(self):
    #   return self._hardware.inputs_enabled

    # @property
    # def cycle_period(self):
    #   return self._hardware.cycle_period

    # @property
    # def n_global_timers(self):
    #   return self._hardware.n_global_timers

    # @property
    # def n_global_counters(self):
    #   return self._hardware.n_global_counters

    # @property
    # def n_conditions(self):
    #   return self._hardware.n_conditions

    # @property
    # def n_uart_channels(self):
    #   return self._hardware.n_uart_channels

    # @property
    # def firmware_version(self):
    #   return self._hardware.firmware_version

    # @property
    # def machine_type(self):
    #   return self._hardware.machine_type

    # @property
    # def cycle_frequency(self):
    #   return self._hardware.cycle_frequency
