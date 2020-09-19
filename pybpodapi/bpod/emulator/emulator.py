"""

.. moduleauthor:: Chris Karageorgiou Kaneen

emulator: An implementation of an emulated Bpod device.

"""
__author__ = "Chris Karageorgiou Kaneen"

import logging
import math
import queue
import time

from . import constants as const
from .state import State
from AnyQt import QtCore
from AnyQt import QtNetwork
from PyQt5 import sip
from pybpodapi.bpod_modules.bpod_modules import BpodModules

logger = logging.getLogger(__name__)


# N_VIRTUAL_CURRENT_EVENTS = 10
N_TIMESTAMPS = 10000
UART_CODE = 'U'
USB_CODE = 'X'
BNC_CODE = 'B'
WIRE_CODE = 'W'
PORTS_CODE = 'P'
SERIAL_EVENT_CODE = 'S'
INPUT_CODE = 'I'
GLOBAL_TIMER_CODE = 'T'
GLOBAL_COUNTER_CODE = '+'
CONDITION_CODE = 'C'

CONDITION_EVENT_NAME_PREFIX = 'Condition'
SOFTCODE_OUTPUT_ACTION = 'SoftCode'
GLOBAL_TIMER_TRIG_OUTPUT_ACTION = 'GlobalTimerTrig'
GLOBAL_TIMER_CANCEL_OUTPUT_ACTION = 'GlobalTimerCancel'
GLOBAL_COUNTER_RESET_OUTPUT_ACTION = 'GlobalCounterReset'
FINAL_GLOBAL_COUNTER_EVENT = 254
FINAL_EVENT = 255
FINAL_CHANNEL = 255


class EmulatorError(Exception):
    pass


def emulator_init_check(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AttributeError:
            message = 'The emulator initialize() has not been called.'
            logger.error(message)
            raise EmulatorError(message)
    return wrapper


class Emulator:
    """A class for emulating the Bpod device."""

    GUI_PLUGIN_SERVER_NAME = 'emulator_gui_server'

    _GLOBAL_TIMER_START_OFFSET = None
    _GLOBAL_TIMER_END_OFFSET = None
    _GLOBAL_COUNTER_OFFSET = None
    _CONDITION_OFFSET = None
    _JUMP_OFFSET = None
    _CONDITION_EVENT_NAME = None
    _SOCKET_WAIT_FOR_CONNECTED_TIMEOUT = 500

    def __init__(self, hardware):
        self._init_hardware(hardware)
        self._state = State(self.hardware)
        self._manual_override_events = queue.Queue()
        self._socket = None

    @property
    def socket(self):
        if self._socket is None or sip.isdeleted(self._socket):
            self._socket = QtNetwork.QLocalSocket()
        return self._socket

    @property
    def hardware(self):
        return self._hardware

    @property
    @emulator_init_check
    def matrix_start_time(self):
        return self._matrix_start_time

    @property
    @emulator_init_check
    def timestamps(self):
        return self._timestamps

    @property
    @emulator_init_check
    def n_events(self):
        return self._n_events

    def _init_hardware(self, hardware):
        self._hardware = hardware
        self._setup_hardware_description()
        self._hardware.configure_inputs()
        self._setup_hardware_channels()
        self._setup_hardware_event_types()
        self._set_hardware_constants()

    def _set_hardware_constants(self):
        n_event_names = len(self.hardware.channels.event_names)
        n_extra_events = self.hardware.n_global_timers * 2 + \
            self.hardware.n_global_counters + self.hardware.n_conditions
        # Subtract global timer/counter/condition and tup events
        input_matrix_size = n_event_names - (n_extra_events + 1)
        self._GLOBAL_TIMER_START_OFFSET = input_matrix_size
        self._GLOBAL_TIMER_END_OFFSET = self._GLOBAL_TIMER_START_OFFSET + \
            self.hardware.n_global_timers
        self._GLOBAL_COUNTER_OFFSET = self._GLOBAL_TIMER_END_OFFSET + \
            self.hardware.n_global_timers
        self._CONDITION_OFFSET = self._GLOBAL_COUNTER_OFFSET + \
            self.hardware.n_global_counters
        self._JUMP_OFFSET = self._CONDITION_OFFSET + \
            self.hardware.n_conditions
        self._CONDITION_EVENT_NAME = [
            f'{CONDITION_EVENT_NAME_PREFIX}{str(i + 1)}'
            for i in range(self.hardware.n_conditions)]

    def _setup_hardware_description(self):
        HW_DESCR = const.HARDWARE_DESCRIPTION
        machine_type = const.MACHINE_TYPE
        self.hardware.firmware_version = const.FIRMWARE_VERSION
        self.hardware.machine_type = machine_type
        self.hardware.max_states = HW_DESCR['MAX_STATES'][machine_type]
        self.hardware.cycle_period = HW_DESCR['TIMER_PERIOD']
        if machine_type == const.MACHINE_TYPE_ENUM.THREE:
            self.hardware.max_serial_events = \
                HW_DESCR['MAX_SERIAL_EVENTS'][machine_type][const.ETHERNET_COM]
            self.hardware.inputs = \
                HW_DESCR['INPUT_HW'][machine_type][const.ETHERNET_COM]
            self.hardware.outputs = \
                HW_DESCR['OUTPUT_HW'][machine_type][const.ETHERNET_COM]
        else:
            self.hardware.max_serial_events = \
                HW_DESCR['MAX_SERIAL_EVENTS'][machine_type]
            self.hardware.inputs = \
                HW_DESCR['INPUT_HW'][machine_type]
            self.hardware.outputs = \
                HW_DESCR['OUTPUT_HW'][machine_type]
        sm_feature_profile = const.SM_FEATURE_PROFILE[machine_type]
        self.hardware.n_global_timers = HW_DESCR[
            'MAX_GLOBAL_TIMERS'][sm_feature_profile]
        self.hardware.n_global_counters = HW_DESCR[
            'MAX_GLOBAL_COUNTERS'][sm_feature_profile]
        self.hardware.n_conditions = HW_DESCR[
            'MAX_CONDITIONS'][sm_feature_profile]
        self.hardware.n_inputs = len(self.hardware.inputs)
        self.hardware.n_outputs = len(self.hardware.outputs)

    def _setup_hardware_channels(self):
        self.bpod_modules = BpodModules(self)
        input_modules = [inp for inp in self.hardware.inputs
                         if inp == UART_CODE]
        n_modules = len(input_modules)
        n_serial_events = int(
            self.hardware.max_serial_events / (n_modules + 1))
        connected = False
        module_name = None
        firmware_version = None
        events_names = []
        for i in range(n_modules):
            self.bpod_modules += BpodModules.create_module(
                connected,
                module_name,
                firmware_version,
                events_names,
                n_serial_events,
                serial_port=(i + 1),
            )
        self.hardware.setup(self.bpod_modules)

    def _setup_hardware_event_types(self):
        n_bnc_inputs = self.hardware.inputs.count(BNC_CODE)
        n_wire_inputs = self.hardware.inputs.count(WIRE_CODE)
        n_ports = self.hardware.outputs.count(PORTS_CODE)
        n_digital_inputs = n_bnc_inputs + n_wire_inputs + n_ports
        self.hardware_event_types = SERIAL_EVENT_CODE * \
            self.hardware.max_serial_events + INPUT_CODE * \
            n_digital_inputs * 2 + GLOBAL_TIMER_CODE * \
            self.hardware.n_global_timers * 2 + GLOBAL_COUNTER_CODE * \
            self.hardware.n_global_counters + CONDITION_CODE * \
            self.hardware.n_conditions + UART_CODE

    def _output_value(self, output_action=None, output_code=None):
        if output_action is None and output_code is None:
            message = 'Must pass an output action or output_code.'
            logger.error(message)
            raise EmulatorError(message)
        if output_action is not None:
            output_code = \
                self.hardware.channels.output_channel_names.index(
                    output_action)
        for output_code_, output_value in self._state_machine.output_matrix[
                self._current_state]:
            if output_code_ == output_code:
                return output_value
        return 0

    def _assert_state_machine(self):
        if self._state_machine is None:
            message = 'State machine has not been set.'
            logger.error(message)
            raise EmulatorError(message)

    def _set_global_timer_channel(self, channel, on):
        this_channel = self._state_machine.global_timers.channels[channel]
        if this_channel < FINAL_CHANNEL:
            self._state.output[this_channel] = on

    def _send_output_to_gui_server(self, channel_number, value):
        self.socket.connectToServer(
            self.GUI_PLUGIN_SERVER_NAME, QtCore.QIODevice.WriteOnly)
        if self.socket.waitForConnected(
                self._SOCKET_WAIT_FOR_CONNECTED_TIMEOUT):
            output_channel_name = self._hardware.channels.output_channel_names[
                channel_number]
            message = f'{output_channel_name}:{value}'
            self.socket.write(message.encode('utf-8'))
            if not self.socket.waitForBytesWritten(2000):
                error_message = \
                    f'Could not write to socket: {self.socket.errorString()}'
                logger.error(error_message)
                raise EmulatorError(error_message)
            self.socket.disconnectFromServer()
        elif self.socket.error() != \
                QtNetwork.QAbstractSocket.HostNotFoundError:
            error_message = \
                f'Could not connect to server: {self.socket.errorString()}'
            logger.error(error_message)
            raise EmulatorError(error_message)
        else:
            logger.error('Emulator gui plugin server is down.')

    def set_state_machine(self, state_machine):
        self._state_machine = state_machine
        logger.debug('State machine set.')

    def set_state_start_time(self, time):
        self._state_start_time = time
        logger.debug(f'State start time set to: {self._state_start_time}')

    def set_global_timer_end_time(self, set_global_channel_timer=False):
        this_global_timer = self._output_value(
            GLOBAL_TIMER_TRIG_OUTPUT_ACTION)
        if this_global_timer != 0:
            timer_idx = this_global_timer - 1
            if self._state_machine.global_timers.on_set_delays[timer_idx] == 0:
                self._global_timer_end[timer_idx] = self.current_time + \
                    self._state_machine.global_timers.timers[timer_idx]
                self._global_timers_active[timer_idx] = True
                self._global_timers_triggered[timer_idx] = False
                if set_global_channel_timer:
                    self._set_global_timer_channel(this_global_timer, 1)
            else:
                self._global_timer_start[timer_idx] = self.current_time + \
                    self._state_machine.global_timers.on_set_delays[timer_idx]
                self._global_timer_end[timer_idx] = self._global_timer_start[
                    timer_idx] + self._state_machine.global_timers.timers[
                    timer_idx]
                self._global_timers_triggered[timer_idx] = True
            logger.debug('Global timer end time set.')

    def set_softcode(self, output_code):
        self._softcode = self._output_value(
            output_code=output_code)
        logger.debug(f'Softcode set to: {self._softcode}')

    def reset_current_state(self):
        self._assert_state_machine()
        self._current_state = self._state_machine.current_state
        logger.debug(f'Current state reset to: {self._current_state}')

    def reset_global_counter_counts(self):
        this_global_counter = self._output_value(
            GLOBAL_COUNTER_RESET_OUTPUT_ACTION)
        if this_global_counter != 0:
            self._global_counter_counts[this_global_counter - 1] = 0
            logger.debug('Global counter counts reset.')

    def cancel_global_timers(self):
        this_global_timer = self._output_value(
            GLOBAL_TIMER_CANCEL_OUTPUT_ACTION)
        if this_global_timer != 0:
            self._global_timers_active[this_global_timer - 1] = False
            logger.debug('Global timers cancelled.')

    def initialize(self):
        self._assert_state_machine()
        self._n_events = 0
        self._current_state = 0
        self._global_timer_start = [0] * self.hardware.n_global_timers
        self._global_timer_end = [0] * self.hardware.n_global_timers
        self._global_timers_triggered = [
            False] * self.hardware.n_global_timers
        self._global_timers_active = [False] * self.hardware.n_global_timers
        self._global_counter_counts = [0] * self.hardware.n_global_counters
        self._condition_channels = [0] * self.hardware.n_conditions
        self._condition_values = [0] * self.hardware.n_conditions
        self._timestamps = [0] * N_TIMESTAMPS
        self._meaningful_timer = []
        for tup in list(zip(
                self._state_machine.state_timer_matrix,
                range(self._state_machine.total_states_added))):
            self._meaningful_timer.append(tup[0] != tup[1])
        self.current_time = time.time()
        self._matrix_start_time = self.current_time
        self._state_start_time = self.current_time
        self._softcode = self._output_value(SOFTCODE_OUTPUT_ACTION)
        # Set global timer end-time (if triggered in first state)
        self.set_global_timer_end_time(set_global_channel_timer=True)

    def run(self):
        self._assert_state_machine()
        virtual_current_events = []
        # MATLAB EQUIVALENT:
        # virtual_current_events = [0] * N_VIRTUAL_CURRENT_EVENTS
        opcode, data = None, None
        if self._softcode == 0:
            self.current_time = time.time()
            self._n_current_events = 0
            # Add oldest manual override event to current events
            if not self._manual_override_events.empty():
                virtual_current_events.append(
                    self._manual_override_events.get())
                self._n_current_events += 1
            # Evaluate global timer transitions
            for i in range(self.hardware.n_global_timers):
                if self._global_timers_active[i]:
                    if self.current_time > self._global_timer_end[i]:
                        virtual_current_events.append(
                            self._GLOBAL_TIMER_END_OFFSET + i)
                        self._n_current_events += 1
                        self._global_timers_active[i] = False
                        # MATLAB version has this commented out:
                        # self._set_global_timer_channel(i, 0)
                elif self._global_timers_triggered[i] and \
                        not self._global_timers_active[i] and \
                        self.current_time > self._global_timer_start[i]:
                    virtual_current_events.append(
                        self._GLOBAL_TIMER_START_OFFSET + i)
                    self._n_current_events += 1
                    self._global_timers_active[i] = True
                    self._global_timers_triggered[i] = False
                    # MATLAB version has this commented out:
                    # self._set_global_timer_channel(i, 1)
            # Evaluate global counter transitions
            for i in range(self.hardware.n_global_counters):
                sma_global_counters = self._state_machine.global_counters
                if sma_global_counters.attached_events[i] != \
                        FINAL_GLOBAL_COUNTER_EVENT:
                    if self._global_counter_counts[i] == \
                            sma_global_counters.thresholds[i]:
                        virtual_current_events.append(
                            self._GLOBAL_COUNTER_OFFSET + i)
                        self._n_current_events += 1
                    if virtual_current_events and \
                            virtual_current_events[0] == \
                            sma_global_counters.attached_events[i]:
                        self._global_counter_counts[i] += 1
            # Evaluate condition transitions
            for i in range(self.hardware.n_conditions):
                sma_conditions = self._state_machine.conditions
                condition_event_code = \
                    self.hardware.channels.event_names.index(
                        self._CONDITION_EVENT_NAME[i])
                target_state = None
                for event_code, destination_state in sma_conditions.matrix[
                        self._current_state]:
                    if event_code == condition_event_code:
                        target_state = destination_state
                        break
                if target_state and target_state != self._current_state:
                    this_channel = sma_conditions.channels[i]
                    hw_state = self._state.input[this_channel]
                    if hw_state == sma_conditions.values[i]:
                        virtual_current_events.append(
                            self._CONDITION_OFFSET + i)
                        self._n_current_events += 1
            # Evaluate state timer transitions
            time_in_state = self.current_time - self._state_start_time
            state_timer = self._state_machine.state_timers[self._current_state]
            if time_in_state > state_timer and \
                    self._meaningful_timer[self._current_state]:
                hardware_state_timer_position = \
                    self.hardware_event_types.index(UART_CODE)
                virtual_current_events.append(
                    hardware_state_timer_position)
                self._n_current_events += 1
            if virtual_current_events:
                dominant_event = virtual_current_events[0]
                if dominant_event > 0:
                    opcode = 1
                    data = virtual_current_events
                    total_n_events = self._n_events + self._n_current_events
                    self._timestamps[
                        self._n_events:total_n_events + 1] = \
                        [self.current_time - self._matrix_start_time] * \
                        self._n_current_events
                    self._n_events = total_n_events
        else:
            opcode = 2
            data = self._softcode
            self._softcode = 0
        return opcode, data

    def mirror_state(self, state):
        if state is None:
            self._state.clear_input()
            self._state.clear_output()
            # TODO: Do the BpodSystem.RefreshGUI equivalent
        else:
            # Add outputs that have not been overridden to output state
            for new_output_channel, new_output_value in \
                    self._state_machine.output_matrix[state]:
                if new_output_channel not in self._state.output:
                    self._state.output[new_output_channel] = new_output_value
                self._send_output_to_gui_server(
                    new_output_channel, new_output_value)
                logger.debug('State mirrored.')

    def mirror_events(self, events):
        for event in events:
            this_event = event
            if this_event != FINAL_EVENT:
                event_type = self.hardware_event_types[this_event]
                if event_type == INPUT_CODE:
                    io_event_start_position = self.hardware_event_types.index(
                        INPUT_CODE)
                    n_uart_serial_channels = self.hardware.outputs.count(
                        UART_CODE)
                    n_usb_channels = self.hardware.outputs.count(USB_CODE)
                    n_serial_channels = n_uart_serial_channels + n_usb_channels
                    p = ((this_event - io_event_start_position) / 2) + \
                        n_serial_channels
                    this_channel = math.floor(p)
                    is_odd = p % 1
                    if is_odd == 0:
                        self._state.input[this_channel] = 1
                    else:
                        self._state.input[this_channel] = 0
                elif event_type == GLOBAL_TIMER_CODE:
                    global_timer_start_position = \
                        self.hardware_event_types.index(GLOBAL_TIMER_CODE)
                    timer_event = this_event - global_timer_start_position
                    if timer_event <= self.hardware.n_global_timers:
                        timer_number = timer_event
                        event_type = 1  # on
                    else:
                        timer_number = timer_event - \
                            self.hardware.n_global_timers
                        event_type = 0  # off
                    timer_number_idx = timer_number - 1
                    if self._state_machine.global_timers.channels[
                            timer_number_idx] < FINAL_CHANNEL:
                        output_channel = \
                            self._state_machine.global_timers.channels[
                                timer_number_idx]
                        output_channel_type = self.hardware.outputs[
                            output_channel]
                        if output_channel_type in \
                                (BNC_CODE, WIRE_CODE, PORTS_CODE):
                            self._state.output[
                                output_channel] = event_type
        logger.debug('Events mirrored.')

    def override_input_state(self, channel_number, channel_value):
        self._state.input[channel_number] = channel_value
        event_type = self._state.input_type[channel_number]
        if event_type not in (UART_CODE, USB_CODE):
            event_bnc_position = \
                self._hardware.channels.events_positions.Event_BNC
            output_usb_position = \
                self._hardware.channels.events_positions.output_USB
            channel_value_offset = 0
            if channel_value > 0:
                channel_value_offset = 1
            new_event = event_bnc_position - 1 + \
                2 * (channel_number - output_usb_position) - \
                channel_value_offset
            self._manual_override_events.put(new_event)

    def serial_override(self, channel_number, channel_value):
        self._state.output[channel_number] = channel_value

    def add_manual_override_event(self, event):
        hardware_channels = self._hardware.channels
        if isinstance(event, int):
            try:
                hardware_channels.get_event_name(event)
            except IndexError as e:
                raise EmulatorError(str(e))
            else:
                event_code = event
        else:
            if event not in hardware_channels.event_names:
                raise EmulatorError('unknown event name')
            event_code = hardware_channels.event_names.index(event)
        self._manual_override_events.put(event_code)

    def log_state_machine_info(self):
        self._assert_state_machine()
        sma = self._state_machine

        def get_max_index_used(sma_global):
            max_idx = sma_global.get_max_index_used()
            return 0 if max_idx is None else max_idx + 1
        highest_used_global_counter = get_max_index_used(sma.global_counters)
        highest_used_global_timer = get_max_index_used(sma.global_timers)
        highest_used_global_condition = get_max_index_used(
            sma.conditions)
        # State timer matrix (state timer transitions)
        state_timer_matrix = []
        for i in range(sma.total_states_added):
            timer = sma.state_timer_matrix[i]
            if math.isnan(timer):
                timer = sma.total_states_added
            state_timer_matrix.append(timer)
        logger.debug("STATE TIMER MATRIX: %s", state_timer_matrix)
        # Input matrix (event-triggered transitions)
        input_matrix = []
        for i in range(sma.total_states_added):
            state_transitions = sma.input_matrix[i]
            n_transitions = len(state_transitions)
            input_matrix += [n_transitions]
            for transition in state_transitions:
                input_matrix += [transition[0]]
                dest_state = transition[1]
                if math.isnan(dest_state):
                    dest_state = sma.total_states_added
                input_matrix.append(dest_state)
        logger.debug("INPUT MATRIX: %s", input_matrix)
        # Output matrix (hardware states)
        output_matrix = []
        global_timer_trigger_event_pos =  \
            self.hardware.channels.events_positions.globalTimerTrigger
        for i in range(sma.total_states_added):
            hw_state = sma.output_matrix[i]
            pos = global_timer_trigger_event_pos
            hw_state = [evt for evt in hw_state if evt[0] < pos]
            n_differences = len(hw_state)
            output_matrix += [n_differences]
            for hw_conf in hw_state:
                output_matrix += hw_conf[:2]
        logger.debug("OUTPUT MATRIX: %s", output_matrix)
        # Global timer start matrix (global timer-start triggered transitions)
        global_timer_start_matrix = []
        global_timer_start_event_pos = \
            self.hardware.channels.events_positions.globalTimerStart
        for i in range(sma.total_states_added):
            state_transitions = sma.global_timers.start_matrix[i]
            n_transitions = len(state_transitions)
            global_timer_start_matrix += [n_transitions]
            for transition in state_transitions:
                dest_state = transition[1]
                global_timer_start_matrix += [
                    transition[0] - global_timer_start_event_pos]
                if math.isnan(dest_state):
                    dest_state = sma.total_states_added
                global_timer_start_matrix.append(dest_state)
        logger.debug("GLOBAL_TIMER_START_MATRIX: %s",
                     global_timer_start_matrix)

        # Global timer end matrix (global timer-end triggered transitions)
        global_timer_end_matrix = []
        global_timer_end_event_pos = \
            self.hardware.channels.events_positions.globalTimerEnd
        for i in range(sma.total_states_added):
            state_transitions = sma.global_timers.end_matrix[i]
            n_transitions = len(state_transitions)
            global_timer_end_matrix += [n_transitions]
            for transition in state_transitions:
                dest_state = transition[1]
                global_timer_end_matrix += [
                    transition[0] - global_timer_end_event_pos]
                if math.isnan(dest_state):
                    dest_state = sma.total_states_added
                global_timer_end_matrix.append(dest_state)
        logger.debug("GLOBAL_TIMER_END_MATRIX: %s", global_timer_end_matrix)
        # Global counter matrix (global counter triggered transitions)
        global_counter_matrix = []
        global_counter_event_pos = \
            self.hardware.channels.events_positions.globalCounter
        for i in range(sma.total_states_added):
            state_transitions = sma.global_counters.matrix[i]
            n_transitions = len(state_transitions)
            global_counter_matrix += [n_transitions]
            for transition in state_transitions:
                dest_state = transition[1]
                global_counter_matrix += [
                    transition[0] - global_counter_event_pos]
                if math.isnan(dest_state):
                    dest_state = sma.total_states_added
                global_counter_matrix.append(dest_state)
        logger.debug("GLOBAL_COUNTER_MATRIX: %s", global_counter_matrix)

        # Condition matrix (condition triggered transitions)
        condition_matrix = []
        condition_event_pos = self.hardware.channels.events_positions.condition
        for i in range(sma.total_states_added):
            state_transitions = sma.conditions.matrix[i]
            n_transitions = len(state_transitions)
            condition_matrix += [n_transitions]
            for transition in state_transitions:
                dest_state = transition[1]
                condition_matrix += [
                    transition[0] - condition_event_pos]
                if math.isnan(dest_state):
                    dest_state = sma.total_states_added
                condition_matrix.append(dest_state)
        logger.debug("CONDITION_MATRIX: %s", condition_matrix)
        # Global timer channels
        global_timer_channels = []
        for i in range(highest_used_global_timer):
            global_timer_channels += [sma.global_timers.channels[i]]
        logger.debug("GLOBAL_TIMER_CHANNELS: %s", global_timer_channels)
        # Global timer on messages
        global_timer_on_messages = []
        for i in range(highest_used_global_timer):
            v = sma.global_timers.on_messages[i]
            global_timer_on_messages += [255 if v == 0 else v]
        logger.debug("GLOBAL_TIMER_ON_MESSAGES: %s", global_timer_on_messages)
        # Global timer off messages
        global_timer_off_messages = []
        for i in range(highest_used_global_timer):
            v = sma.global_timers.off_messages[i]
            global_timer_off_messages += [255 if v == 0 else v]
        logger.debug("GLOBAL_ TIMER_OFF_MESSAGES: %s",
                     global_timer_off_messages)
        # Global timer loop mode
        global_timer_loop_mode = []
        for i in range(highest_used_global_timer):
            global_timer_loop_mode += [sma.global_timers.loop_mode[i]]
        logger.debug("GLOBAL_TIMER_LOOP_MODE: %s", global_timer_loop_mode)
        # Global timer events
        global_timer_events = []
        for i in range(highest_used_global_timer):
            global_timer_events += [sma.global_timers.send_events[i]]
        logger.debug("GLOBAL_TIMER_EVENTS: %s", global_timer_events)
        # Global counter attached events
        global_counter_attached_events = []
        for i in range(highest_used_global_counter):
            global_counter_attached_events += [
                sma.global_counters.attached_events[i]]
        logger.debug("GLOBAL_COUNTER_ATTACHED_EVENTS: %s",
                     global_counter_attached_events)
        # Conditions channels
        conditions_channels = []
        for i in range(highest_used_global_condition):
            conditions_channels += [sma.conditions.channels[i]]
        logger.debug("CONDITIONS_CHANNELS: %s", conditions_channels)
        # Conditions values
        conditions_values = []
        for i in range(highest_used_global_condition):
            conditions_values += [sma.conditions.values[i]]
        logger.debug("CONDITIONS VALUES: %s", conditions_values)
        # Global counter resets
        global_counter_resets = []
        for i in range(sma.total_states_added):
            global_counter_resets += [sma.global_counters.reset_matrix[i]]
        logger.debug("GLOBAL_COUNTER_RESETS: %s", global_counter_resets)
