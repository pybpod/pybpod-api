# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from bpodapi.com.arcom import ArCOM
from bpodapi.com.bpod_protocol import BpodProtocol

logger = logging.getLogger(__name__)


class BpodCom(object):
	"""
	Handle communication protocol with Bpod
	"""

	def __init__(self):
		# type arcom: bpodapi.com.arcom.ArCOM
		self.arcom = None

	def connect(self, serial_port, baudrate=115200):
		self.arcom = ArCOM()
		self.arcom.open(serial_port, baudrate)

	def handshake(self):
		"""
		Test connectivity by doing an handshake
		:return:
		"""

		logger.debug("Requesting handshake (%s)", BpodProtocol.HANDSHAKE)

		self.arcom.write_char(BpodProtocol.HANDSHAKE)

		response = self.arcom.read_char()  # Receive response

		logger.debug("Response command is: %s", response)

		return response

	def firmware_version(self):
		"""
		Request firmware version from Bpod
		:return:
		"""
		logger.debug("Requesting firmware version: %s", BpodProtocol.FIRMWARE_VERSION)

		self.arcom.write_char(BpodProtocol.FIRMWARE_VERSION)

		response = self.arcom.read_uint32()  # Receive response

		logger.debug("FW version: %s", response)

		return response

	def hardware_description(self, hardware_info):
		"""
		Request hardware description from Bpod
		:type hardware_info: bpodapi.com.serial_containers.HardwareInfoContainer
		:param hardware_info: empty container to be filled with serial data
		"""
		logger.debug("Requesting hardware description (%s)...", BpodProtocol.HARDWARE_DESCRIPTION)
		self.arcom.write_char(BpodProtocol.HARDWARE_DESCRIPTION)

		hardware_info.max_states = self.arcom.read_uint16()
		logger.debug("Read max states: %s", hardware_info.max_states)

		hardware_info.cycle_period = self.arcom.read_uint16()
		logger.debug("Read cycle period: %s", hardware_info.cycle_period)

		hardware_info.n_events_per_serial_channel = self.arcom.read_uint8()
		logger.debug("Read number of events per serial channel: %s", hardware_info.n_events_per_serial_channel)

		hardware_info.n_global_timers = self.arcom.read_uint8()
		logger.debug("Read number of global timers: %s", hardware_info.n_global_timers)

		hardware_info.n_global_counters = self.arcom.read_uint8()
		logger.debug("Read number of global counters: %s", hardware_info.n_global_counters)

		hardware_info.n_conditions = self.arcom.read_uint8()
		logger.debug("Read number of conditions: %s", hardware_info.n_conditions)

		hardware_info.n_inputs = self.arcom.read_uint8()
		logger.debug("Read number of inputs: %s", hardware_info.n_inputs)

		hardware_info.inputs = self.arcom.read_char_array(array_len=hardware_info.n_inputs)
		logger.debug("Read inputs: %s", hardware_info.inputs)

		hardware_info.n_outputs = self.arcom.read_uint8()
		logger.debug("Read number of outputs: %s", hardware_info.n_outputs)

		hardware_info.outputs = self.arcom.read_char_array(array_len=hardware_info.n_outputs)
		logger.debug("Read outputs: %s", hardware_info.outputs)

	def enable_ports(self, inputs_enabled):
		"""

		:param inputs_enabled:
		:return:
		"""
		logger.debug("Requesting ports enabling (%s)", BpodProtocol.ENABLE_PORTS)
		logger.debug("Inputs enabled (%s): %s", len(inputs_enabled), inputs_enabled)

		self.arcom.write_uint8_array([ord(BpodProtocol.ENABLE_PORTS)] + inputs_enabled)

		response = self.arcom.read_uint8()

		logger.debug("Confirmation: %s", response)

		return response

	def set_sync_channel_and_mode(self, sync_channel, sync_mode):
		logger.debug("Requesting sync configuration (%s)", BpodProtocol.SYNC_CHANNEL_MODE)

		self.arcom.write_uint8_array([ord(BpodProtocol.SYNC_CHANNEL_MODE), sync_channel, sync_mode])

		response = self.arcom.read_uint8()

		logger.debug("Confirmation: %s", response)

		return response

	def send_state_machine(self, Message, ThirtyTwoBitMessage):
		"""
		Send state machine to Bpod
		:param Message:
		:param ThirtyTwoBitMessage:
		:return:
		"""

		logger.debug("Sending state machine: %s", Message)
		logger.debug("Data to send: %s", ThirtyTwoBitMessage)

		self.arcom.write_uint8_array(Message)

		self.arcom.write_uint32_array(ThirtyTwoBitMessage)

		response = self.arcom.read_uint8()

		logger.debug("Confirmation: %s", response)

		return response

	def run_state_machine(self):
		logger.debug("Requesting state machine run (%s)", BpodProtocol.RUN_STATE_MACHINE)

		self.arcom.write_char(BpodProtocol.RUN_STATE_MACHINE)

	def data_available(self):
		return self.arcom.bytes_available() > 0

	def read_opcode_message(self):
		response = self.arcom.read_uint8_array(array_len=2)
		opcode = response[0]
		data = response[1]

		logger.debug("Read opcode message: opcode=%s, data=%s", opcode, data)

		return opcode, data

	def read_trial_start_timestamp_ms(self):
		response = self.arcom.read_uint32()

		trial_start_timestamp = float(response) / 1000  # Start-time of the trial in milliseconds

		return trial_start_timestamp

	def read_timestamps(self):
		n_timestamps = self.arcom.read_uint16()

		timestamps = self.arcom.read_uint32_array(array_len=n_timestamps)

		return timestamps

	def read_current_events(self, n_events):
		current_events = self.arcom.read_uint8_array(array_len=n_events)

		logger.debug("Read current events: %s", current_events)

		return current_events

	def load_serial_message(self, message):
		logger.debug("Requesting load serial message (%s)", BpodProtocol.LOAD_SERIAL_MESSAGE)

		self.arcom.write_uint8_array([ord(BpodProtocol.SYNC_CHANNEL_MODE), message])

		response = self.arcom.read_uint8()

		logger.debug("Confirmation: %s", response)

		return response

	def reset_serial_messages(self):
		logger.debug("Requesting serial messages reset (%s)", BpodProtocol.RESET_SERIAL_MESSAGES)

		self.arcom.write_char(BpodProtocol.RESET_SERIAL_MESSAGES)

		response = self.arcom.read_uint8()

		logger.debug("Confirmation: %s", response)

		return response

	def disconnect(self):
		logger.debug("Requesting disconnect (%s)", BpodProtocol.DISCONNECT)

		self.arcom.write_char(BpodProtocol.DISCONNECT)
