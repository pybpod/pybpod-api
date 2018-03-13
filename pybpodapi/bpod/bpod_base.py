# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import math
import time

from pyforms import conf as settings


from pybpodapi.bpod.hardware.hardware import Hardware
from pybpodapi.bpod.hardware.channels import ChannelType
from pybpodapi.bpod.hardware.channels import ChannelName
from pybpodapi.bpod.hardware.events   import EventName
from pybpodapi.bpod.hardware.channels import ChannelType
from pybpodapi.bpod.hardware.output_channels import OutputChannel

from pybpodapi.com.messaging.end_trial          import EndTrial
from pybpodapi.com.messaging.trial              import Trial
from pybpodapi.com.messaging.event_occurrence       import EventOccurrence
from pybpodapi.com.messaging.event_resume           import EventResume
from pybpodapi.com.messaging.softcode_occurrence    import SoftcodeOccurrence
from pybpodapi.com.messaging.session_info           import SessionInfo

from pybpodapi.bpod_modules.bpod_modules import BpodModules
from pybpodapi.exceptions.bpod_error import BpodErrorException

from pybpodapi.session import Session


logger = logging.getLogger(__name__)


class BpodBase(object):
    """
    API to interact with Bpod
    
    :ivar Session session: Session for this bpod running experiment
    :ivar Hardware hardware: Hardware object representing Bpod hardware
    :ivar MessageAPI message_api: Abstracts communication with Bpod box
    :ivar bool new_sma_sent: whether a new state machine was already uploaded to Bpod box
    """

    class Events(EventName):             pass
    class OutputChannels(OutputChannel): pass
    class ChannelTypes(ChannelType):     pass
    class ChannelNames(ChannelName):     pass
    

    CHECK_STATE_MACHINE_COUNTER = 0

    def __init__(self, serial_port=None, sync_channel=None, sync_mode=None):
        self._session = self.create_session()
        
        self.serial_port    = serial_port    if serial_port     is not None else settings.SERIAL_PORT
        self.baudrate       = settings.BAUDRATE
        self.sync_channel   = sync_channel   if sync_channel    is not None else settings.SYNC_CHANNEL
        self.sync_mode      = sync_mode      if sync_mode       is not None else settings.SYNC_MODE
        
        self._hardware      = Hardware()    # type: Hardware
        self.bpod_modules   = None          # type: BpodModules

        self._new_sma_sent  = False         # type: bool


        self._hardware.sync_channel = self.sync_channel  # 255 = no sync, otherwise set to a hardware channel number
        self._hardware.sync_mode    = self.sync_mode    # 0 = flip logic every trial, 1 = every state
        
        self.session += SessionInfo( self.session.INFO_SERIAL_PORT, self.serial_port )
        

    #########################################
    ############ PUBLIC METHODS #############
    #########################################

    def start(self):
        """
        Starts Bpod.

        Connect to Bpod board through serial port, test handshake, retrieve firmware version,
        retrieve hardware description, enable input ports and configure channel synchronization.
        
        Example: 
        
        .. code-block:: python
        
            my_bpod = Bpod().start("/dev/tty.usbmodem1293", "/Users/John/Desktop/bpod_workspace", "2afc_protocol")

        :param str serial_port: serial port to connect
        :param str workspace_path: path for bpod output files (no folders will be created)
        :param str protocol_name: this name will be used for output files
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

        self._hardware.firmware_version     = firmware_version
        self._hardware.machine_type         = machine_type
        #########################################################
        
        
        self._bpodcom_hardware_description(self._hardware)

        if not self._bpodcom_enable_ports(self._hardware):
            raise BpodErrorException('Error: Failed to enable Bpod inputs.')

        if not self._bpodcom_set_sync_channel_and_mode(sync_channel=self.sync_channel, sync_mode=self.sync_mode):
            raise BpodErrorException('Error: Failed to configure syncronization.')

        #check if any module is connected
        self.bpod_modules = self._bpodcom_get_modules_info(self._hardware)


        self._hardware.setup(self.bpod_modules)

        return self


    def stop(self):
        """
        Close connection with Bpod
        """
        self._bpodcom_disconnect()



    def refresh_modules(self):
        #check if any module is connected
        self.bpod_modules = self._bpodcom_get_modules_info(self._hardware)
        self._hardware.setup(self.bpod_modules)


    


    def send_state_machine(self, sma):
        """
        Builds message and sends state machine to Bpod

        :param pybpodapi.model.state_machine sma: initialized state machine
        """

        logger.info("Sending state machine")

        sma.update_state_numbers()

        message = sma.build_message()
    
        message32 = sma.build_message_32_bits()

        self._bpodcom_send_state_machine(message, message32)

        self._new_sma_sent = True

    def run_state_machine(self, sma):
        """

        Adds a new trial to current session and runs state machine on Bpod box.
        
        While state machine is running, messages are processed accordingly.
        
        When state machine stops, timestamps are updated and trial events are processed.
        
        Finally, data is released for registered data consumers / exporters.
        
        .. seealso::
            
            Add trial: :meth:`pybpodapi.model.session.Session.add_trial`.
            
            Send command "run state machine": :meth:`pybpodapi.com.message_api.MessageAPI.run_state_machine`.
            
            Process opcode: :meth:`pybpodapi.model.bpod.bpod_base.BpodBase._BpodBase__process_opcode`.
            
            Update timestamps: :meth:`pybpodapi.model.bpod.bpod_base.BpodBase._BpodBase__update_timestamps`.
            
            Add trial events: :meth:`pybpodapi.model.bpod.bpod_base.BpodBase._BpodBase__add_trial_events`.
        
            Publish data: :meth:`pybpodapi.model.bpod.bpod_base.BpodBase._publish_data`.
    
        :param pybpodapi.mode.state_machine sma: initialized state machine
        """

        self.session += Trial(sma)

        logger.info("Running state machine, trial %s", len(self.session.trials) )

        state_change_indexes = []


        self._bpodcom_run_state_machine()
        if self._new_sma_sent:
            if self._bpodcom_state_machine_installation_status():
                self._new_sma_sent = False
            else:
                raise BpodErrorException('Error: The last state machine sent was not acknowledged by the Bpod device.', self)

        sma.is_running = True
        while sma.is_running:
            if self.data_available():
                opcode, data = self._bpodcom_read_opcode_message()
                self.__process_opcode(sma, opcode, data, state_change_indexes)

        self.session += EndTrial('The trial ended')

        self.__update_timestamps(sma, state_change_indexes)

        self.session.add_trial_events()



        logger.info("Publishing Bpod trial")

    
    def manual_override(self, channel_type, channel_name, channel_number, value):
        """
        Manually override a Bpod channel

        :param ChannelType channel_type: channel type input or output
        :param ChannelName channel_name: channel name like PWM, Valve, etc.
        :param channel_number:
        :param int value: value to write on channel
        """
        if channel_type == ChannelType.INPUT:
            raise BpodErrorException('Manually overriding a Bpod input channel is not yet supported in Python.')
        elif channel_type == ChannelType.OUTPUT:
            if channel_name == ChannelName.VALVE:
                if value > 0:
                    value = math.pow(2, channel_number - 1)
                channel_number = self._hardware.channels.events_positions.output_SPI
                self._bpodcom_override_digital_hardware_state(channel_number, value)
            elif channel_name == 'Serial':
                self._bpodcom_send_byte_to_hardware_serial(channel_number, value)
            else:
                try:
                    channel_number = self._hardware.channels.output_channel_names.index(
                        channel_name + str(channel_number))
                    self._bpodcom_override_digital_hardware_state(channel_number, value)
                except:
                    raise BpodErrorException('Error using manual_override: ' + channel_name + ' is not a valid channel name.')
        else:
            raise BpodErrorException('Error using manualOverride: first argument must be "Input" or "Output".')

    def load_serial_message(self, serial_channel, message_ID, serial_message):
        """
        Load serial message on Bpod

        :param int serial_channel: Serial port to send, 1, 2 or 3
        :param int message_ID: Unique id for the message. Should be between 1 and 255
        :param list(int) serial_message: Message to send. The message should be bigger than 3 bytes. 
        """
        response = self._bpodcom_load_serial_message(serial_channel, message_ID, serial_message, 1);

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

    def trigger_event(self, state_index, event):
        return self._bpodcom_manual_override_exec_event(state_index, event)

    def trigger_softcode(self, softcode):
        return self._bpodcom_send_softcode(softcode)


    #########################################
    ############ PRIVATE METHODS ############
    #########################################

    def create_session(self):
        return Session()

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
            n_current_events = data
            
            current_events = self._bpodcom_read_current_events(n_current_events)
            transition_event_found = False

            
            for event_id in current_events:
                if event_id == 255:
                    sma.is_running = False
                else:
                    self._session += EventOccurrence(event_id, sma.hardware.channels.get_event_name(event_id) )

                    # input matrix
                    if not transition_event_found:
                        logger.debug("transition event not found")
                        logger.debug("Current state: %s", sma.current_state)
                        for transition in sma.input_matrix[sma.current_state]:
                            logger.debug("Transition: %s", transition)
                            if transition[0] == event_id:
                                sma.current_state = transition[1]
                                if not math.isnan(sma.current_state):
                                    logger.debug("adding states input matrix")
                                    current_trial.states.append(sma.current_state)
                                    state_change_indexes.append(len(current_trial.events_occurrences) - 1)
                                transition_event_found = True

                    # state timer matrix
                    if not transition_event_found:
                        this_state_timer_transition = sma.state_timer_matrix[sma.current_state]
                        if event_id == sma.hardware.channels.events_positions.Tup:
                            if not (this_state_timer_transition == sma.current_state):
                                sma.current_state = this_state_timer_transition
                                if not math.isnan(sma.current_state):
                                    logger.debug("adding states state timer matrix")
                                    current_trial.states.append(sma.current_state)
                                    state_change_indexes.append(len(current_trial.events_occurrences) - 1)
                                transition_event_found = True

                    # global timers start matrix
                    if not transition_event_found:
                        for transition in sma.global_timers.start_matrix[sma.current_state]:
                            if transition[0] == event_id:
                                sma.current_state = transition[1]
                                if not math.isnan(sma.current_state):
                                    logger.debug("adding states global timers start matrix")
                                    current_trial.states.append(sma.current_state)
                                    state_change_indexes.append(len(current_trial.events_occurrences) - 1)
                                transition_event_found = True

                    # global timers end matrix
                    if not transition_event_found:
                        for transition in sma.global_timers.end_matrix[sma.current_state]:
                            if transition[0] == event_id:
                                sma.current_state = transition[1]
                                if not math.isnan(sma.current_state):
                                    logger.debug("adding states global timers end matrix")
                                    current_trial.states.append(sma.current_state)
                                    state_change_indexes.append(len(current_trial.events_occurrences) - 1)
                                transition_event_found = True
                                
                logger.debug("States indexes: %s", current_trial.states)

        elif opcode == 2:  # Handle soft code
            self._session += SoftcodeOccurrence(data)
            self.softcode_handler_function(data)


    def __update_timestamps(self, sma, state_change_indexes):
        """
        Read timestamps from Bpod and update state machine info

        :param StateMachine sma:
        :param list state_change_indexes:
        """

        current_trial         = self.session.current_trial
        start_trial_timestamp = self._bpodcom_read_trial_start_timestamp_seconds()
        
        current_trial.trial_start_timestamp = start_trial_timestamp  # start timestamp of first trial
        current_trial.bpod_start_timestamp = start_trial_timestamp

        timestamps = self._bpodcom_read_timestamps()

        current_trial.event_timestamps = [i / float(self._hardware.cycle_frequency) for i in timestamps]
        
        # update the timestamps of the events #############################################################
        for event, timestamp in zip(current_trial.events_occurrences, current_trial.event_timestamps):
            event.host_timestamp = timestamp
            e = EventResume(event.event_id, event.event_name, host_timestamp=timestamp)
            self.session += e
        ###################################################################################################

        current_trial.state_timestamps += current_trial.event_timestamps[:len(state_change_indexes)]
        current_trial.state_timestamps += [current_trial.event_timestamps[-1]]

    #########################################
    ############## PROPERTIES ###############
    #########################################

    @property
    def session(self):
        return self._session  # type: Session
    @session.setter
    def session(self, value):
        self._session = value # type: Session

    @property
    def hardware(self):
        return self._hardware  # type: Hardware


    @property
    def modules(self):
        return [m for m in self.bpod_modules if m.connected]


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