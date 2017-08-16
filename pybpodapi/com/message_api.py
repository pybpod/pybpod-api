# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, time, numpy as np

from pybpodapi.com.arcom import ArCOM
from pybpodapi.com.message_headers import SendMessageHeader
from pybpodapi.com.message_headers import ReceiveMessageHeader
from pybpodapi.com.serial_message_container import SerialMessageContainer
from pybpodapi.model.bpod_modules.bpod_modules import BpodModules

from pybpodapi.model.bpod.bpod_error_exception import BpodErrorException


logger = logging.getLogger(__name__)


class MessageAPI(object):
	"""
	Define command actions that can be requested to Bpod device.

	**Private attributes**

		_arcom
			:class:`pybpodapi.com.arcom.ArCOM`

			ArCOM object that performs serial communication.

	**Methods**

	"""

	def __init__(self):
		self._arcom 	= None  # type: ArCOM
	
	def connect(self, serial_port, baudrate=115200, timeout=1):
		"""
		Connect to Bpod using serial connection

		:param str serial_port: serial port to connect
		:param int baudrate: baudrate for serial connection
		:param float timeout: timeout which controls the behavior of read()
		"""
		logger.debug("Connecting on port: %s", serial_port)
		self._arcom = ArCOM().open(serial_port, baudrate, timeout)

	def handshake(self):
		"""
		Test connectivity by doing an handshake

		:return: True if handshake received, False otherwise
		:rtype: bool
		"""
		logger.debug("Requesting handshake (%s)", SendMessageHeader.HANDSHAKE)

		self._arcom.write_char(SendMessageHeader.HANDSHAKE)

		response = self._arcom.read_char()  # Receive response

		logger.debug("Response command is: %s", response)

		return True if response == ReceiveMessageHeader.HANDSHAKE_OK else False

	def firmware_version(self):
		"""
		Request firmware and machine type from Bpod

		:return: firmware and machine type versions
		:rtype: int, int
		"""
		logger.debug("Requesting firmware version (%s)", SendMessageHeader.FIRMWARE_VERSION)

		self._arcom.write_char(SendMessageHeader.FIRMWARE_VERSION)

		fw_version   = self._arcom.read_uint16()  # type: int
		machine_type = self._arcom.read_uint16()  # type: int

		logger.debug("Firmware version: %s", fw_version)
		logger.debug("Machine type: %s", machine_type)

		return fw_version, machine_type



	def hardware_description(self):
		"""
		Request hardware description from Bpod

		:param Hardware hardware: hardware 
		"""
		logger.debug("Requesting hardware description (%s)...", SendMessageHeader.HARDWARE_DESCRIPTION)
		self._arcom.write_char(SendMessageHeader.HARDWARE_DESCRIPTION)

		max_states = self._arcom.read_uint16()  # type: int
		logger.debug("Read max states: %s", max_states)

		cycle_period = self._arcom.read_uint16()  # type: int
		logger.debug("Read cycle period: %s", cycle_period)

		max_serial_events = self._arcom.read_uint8()  # type: int
		logger.debug("Read number of events per serial channel: %s", max_serial_events)

		n_global_timers = self._arcom.read_uint8()  # type: int
		logger.debug("Read number of global timers: %s", n_global_timers)

		n_global_counters = self._arcom.read_uint8()  # type: int
		logger.debug("Read number of global counters: %s", n_global_counters)

		n_conditions = self._arcom.read_uint8()  # type: int
		logger.debug("Read number of conditions: %s", n_conditions)

		n_inputs = self._arcom.read_uint8()  # type: int
		logger.debug("Read number of inputs: %s", n_inputs)

		inputs = self._arcom.read_char_array(array_len=n_inputs)  # type: list(str)
		logger.debug("Read inputs: %s", inputs)

		n_outputs = self._arcom.read_uint8()  # type: int
		logger.debug("Read number of outputs: %s", n_outputs)

		outputs = self._arcom.read_char_array(array_len=n_outputs)  # type: list(str)
		logger.debug("Read outputs: %s", outputs)

		hardware.max_states 		= max_states
		hardware.cycle_period 		= cycle_period
		hardware.max_serial_events 	= max_serial_events
		hardware.n_global_timers 	= n_global_timers
		hardware.n_global_counters 	= n_global_counters
		hardware.n_conditions 		= n_conditions
		hardware.inputs 			= inputs
		hardware.outputs 			= outputs + ['G', 'G', 'G']



	def enable_ports(self, inputs_enabled):
		"""
		Enable input ports on Bpod device

		:param list[int] inputs_enabled: list of inputs to be enabled (0 = disabled, 1 = enabled)
		:rtype: bool
		"""
		logger.debug("Requesting ports enabling (%s)", SendMessageHeader.ENABLE_PORTS)
		logger.debug("Inputs enabled (%s): %s", len(inputs_enabled), inputs_enabled)

		bytes2send = self._arcom.get_uint8_array([ord(SendMessageHeader.ENABLE_PORTS)] + inputs_enabled)

		self._arcom.write_array(bytes2send)

		response = self._arcom.read_uint8()  # type: int

		logger.debug("Response: %s", response)

		return True if response == ReceiveMessageHeader.ENABLE_PORTS_OK else False

	def set_sync_channel_and_mode(self, sync_channel, sync_mode):
		"""
		Request sync channel and sync mode configuration

		:param int sync_channel: 255 = no sync, otherwise set to a hardware channel number
		:param int sync_mode: 0 = flip logic every trial, 1 = every state
		:rtype: bool
		"""
		logger.debug("Requesting sync channel and mode (%s)", SendMessageHeader.SYNC_CHANNEL_MODE)

		bytes2send = self._arcom.get_uint8_array([ord(SendMessageHeader.SYNC_CHANNEL_MODE), sync_channel, sync_mode])

		self._arcom.write_array(bytes2send)

		response = self._arcom.read_uint8()  # type: int

		logger.debug("Response: %s", response)

		return True if response == ReceiveMessageHeader.SYNC_CHANNEL_MODE_OK else False

	def send_state_machine(self, message, message32):
		"""
		Sends state machine to Bpod

		:param list(int) message: TODO
		:param list(int) ThirtyTwoBitMessage: TODO
		"""

		logger.debug("Sending state machine: %s", message)
		logger.debug("Data to send: %s", message32)

		bytes2send = self._arcom.get_uint8_array(
			[ord(SendMessageHeader.NEW_STATE_MATRIX)] + message) + self._arcom.get_uint32_array(message32)

		self._arcom.write_array(bytes2send)

	def run_state_machine(self):
		"""
		Request to run state machine now
		"""
		logger.debug("Requesting state machine run (%s)", SendMessageHeader.RUN_STATE_MACHINE)

		self._arcom.write_char(SendMessageHeader.RUN_STATE_MACHINE)

	def state_machine_installation_status(self):
		"""
		Confirm if new state machine was correctly installed

		:rtype: bool
		"""
		response = self._arcom.read_uint8()  # type: int

		logger.debug("Read state machine installation status: %s", response)

		return True if response == ReceiveMessageHeader.STATE_MACHINE_INSTALLATION_STATUS else False

	def data_available(self):
		"""
		Finds out if there is data received from Bpod

		:rtype: bool
		"""
		return self._arcom.bytes_available() > 0

	def read_opcode_message(self):
		"""
		A new incoming opcode message is available. Read opcode code and data.

		:return: opcode and data
		:rtype: tuple(int, int)
		"""
		response = self._arcom.read_uint8_array(array_len=2)
		opcode = response[0]
		data = response[1]

		logger.debug("Received opcode message: opcode=%s, data=%s", opcode, data)

		return opcode, data

	def read_trial_start_timestamp_seconds(self):
		"""
		A new incoming timestamp message is available. Read trial start timestamp in millseconds and convert to seconds.

		:return: trial start timestamp in milliseconds
		:rtype: float
		"""
		response = self._arcom.read_uint32()  # type: int

		logger.debug("Received start trial timestamp in millseconds: %s", response)

		trial_start_timestamp = float(response) / 1000

		return trial_start_timestamp

	def read_timestamps(self):
		"""
		A new incoming timestamps message is available.
		Read number of timestamps to be sent and then read timestamps array.

		:return: timestamps array
		:rtype: list(float)
		"""
		n_timestamps = self._arcom.read_uint16()  # type: int

		timestamps = self._arcom.read_uint32_array(array_len=n_timestamps)

		logger.debug("Received timestamps: %s", timestamps)

		return timestamps

	def read_current_events(self, n_events):
		"""
		A new incoming events message is available.
		Read number of timestamps to be sent and then read timestamps array.

		:param int n_events: number of events to read
		:return: a list with events
		:rtype: list(int)
		"""
		current_events = self._arcom.read_uint8_array(array_len=n_events)

		logger.debug("Received current events: %s", current_events)

		return current_events

	def load_serial_message(self, message_container):
		"""
		Load serial message on channel

		:param SerialMessageContainer message_container: serial message container
		:rtype: bool
		"""
		logger.debug("Requesting load serial message (%s)", SendMessageHeader.LOAD_SERIAL_MESSAGE)
		logger.debug("Message: %s", message_container)

		bytes2send = self._arcom.get_uint8_array([ord(SendMessageHeader.LOAD_SERIAL_MESSAGE)] + message_container)

		self._arcom.write_array(bytes2send)

		response = self._arcom.read_uint8()  # type: int

		logger.debug("Confirmation: %s", response)

		return True if response == ReceiveMessageHeader.LOAD_SERIAL_MESSAGE_OK else False

	def reset_serial_messages(self):
		"""
		Reset serial messages on Bpod device

		:rtype: bool
		"""
		logger.debug("Requesting serial messages reset (%s)", SendMessageHeader.RESET_SERIAL_MESSAGES)

		self._arcom.write_char(SendMessageHeader.RESET_SERIAL_MESSAGES)

		response = self._arcom.read_uint8()  # type: int

		logger.debug("Confirmation: %s", response)

		return True if response == ReceiveMessageHeader.RESET_SERIAL_MESSAGES else False

	def override_digital_hardware_state(self, channel_number, value):
		"""
		Manually set digital value on channel

		:param int channel_number: number of Bpod port
		:param int value: value to be written
		"""

		bytes2send = self._arcom.get_uint8_array(
			[ord(SendMessageHeader.OVERRIDE_DIGITAL_HW_STATE), channel_number, value])
		self._arcom.write_array(bytes2send)

	def send_byte_to_hardware_serial(self, channel_number, value):
		"""
		Send byte to hardware serial channel 1-3

		:param int channel_number:
		:param int value: value to be written
		"""
		self._arcom.get_uint8_array([ord(SendMessageHeader.SEND_TO_HW_SERIAL), channel_number, value])

	def disconnect(self):
		"""
		Signal Bpod device to disconnect now
		"""
		logger.debug("Requesting disconnect (%s)", SendMessageHeader.DISCONNECT)

		self._arcom.write_char(SendMessageHeader.DISCONNECT)


	def get_modules_info(self, hardware):
		
		bpod_modules = BpodModules(self) # type: BpodModules

		input_modules 	= [inp for inp in hardware.inputs if inp == 'U']
		n_modules 	 	= len(input_modules)
		n_serial_events = int(hardware.max_serial_events/(n_modules+1))

		for inp in input_modules: 
			bpod_modules.add_module(n_serial_events)

		self._arcom.write_char(SendMessageHeader.GET_MODULES)
		time.sleep(0.1)

		modules_requested_events = np.array([0] * n_modules)

		names = {}

		if self._arcom.bytes_available()>1:
			for i in range(n_modules):

				connected 		 = self._arcom.read_uint8()==1
				firmware_version = None
				module_name 	 = None
				events_names 	 = []

				if connected:
					firmware_version = self._arcom.read_uint32()
					name_length 	 = self._arcom.read_uint8()
					name_string 	 = self._arcom.read_char_array(name_length)

					if name_string not in names: names[name_string] = 0
					names[name_string] += 1

					module_name  = name_string + str(names[name_string])
					
					while self._arcom.read_uint8()==1: #has more info to be read
						param_type = self._arcom.read_uint8()
						if  param_type = ReceiveMessageHeader.MODULE_REQUESTED_EVENT:
							modules_requested_events[i] = self._arcom.read_uint8()
						elif param_type = ReceiveMessageHeader.MODULE_EVENT_NAMES:
							n_event_names = self._arcom.read_uint8()
							for j in range(n_event_names):
								n_chars    = self._arcom.read_uint8()
								event_name = self._arcom.read_char_array(name_length)
								events_names.append(event_name)


				bpod_modules += BpodModule(connected, module_name, firmware_version, events_names)
				

		if (modules_requested_events.sum()+n_serial_events)>hardware.max_serial_events:
			raise BpodErrorException('Error: Connected modules requested too many events.')

		for i, module in enmerate(bpod_modules):
			if module.connected:

				if modules_requested_events[i] > module.n_serial_events:
					n_to_reassign = modules_requested_events[i] - module.n_serial_events
					module.n_serial_events = modules_requested_events[i]
				else:
					n_to_reassign = 0

				index = n_modules-1
				while n_to_reassign>0:
					if bpod_modules[index].n_serial_events >= n_to_reassign:
						bpod_modules[index].n_serial_events = bpod_modules[index].n_serial_events - n_to_reassign
						n_to_reassign = 0
					else:
						n_to_reassign = n_to_reassign - bpod_modules[index].n_serial_events
						bpod_modules[index].n_serial_events = 0
					index -= 1

		n_serial_events_array = [m.n_serial_events for m in bpod_modules]
		n_soft_codes = hardware.max_serial_events - sum(n_serial_events_array)
		self._arcom.write_array(['%']+n_serial_events_array+[n_soft_codes])
		
		if not self._arcom.read_uint8():
			raise BpodErrorException('Error: Failed to configure module event assignment.')     
		
		return bpod_modules


	def activate_module_relay(self, module_index):
		self._arcom.write_array([SendMessageHeader.SET_MODULE_RELAY, module_index, 1])

	def deactivate_module_relay(self, module_index):
		self._arcom.write_array([SendMessageHeader.SET_MODULE_RELAY, module_index, 0])


	def clean_any_data_in_the_buffer(self):
		n_bytes_available = self.bytes_available()
		if n_bytes_available > 0:
			self._arcom.read_uint8_array(n_bytes_available)


	def module_write(self, module_index, message):
		if len(message)>64:
			raise BpodError('Error: module messages must be under 64 bytes per transmission')

		self._arcom.write_array([SendMessageHeader.WIRTE_TO_MODULE, module_index, len(message)])
		self._arcom.write_array(message)


	def module_read(self, module_index, size):    
		return self._arcom.read_uint8_array(size)