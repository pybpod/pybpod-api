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
		self.arcom = None

	def connect(self, serial_port, baudrate=115200):
		self.arcom = ArCOM(serial_port, baudrate)  # Create a new instance of an ArCOM serial port

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

	def hardware_description(self, hw, state_machine_info):
		"""
		Request hardware description from Bpod
		TODO: THIS METHOD SHOULD ONLY DO COMM STUFF, THIS IS ONLY TEMPORARY
		:param hw:
		:param state_machine_info:
		:return:
		"""
		logger.debug("Requesting hardware description (%s)...", BpodProtocol.HARDWARE_DESCRIPTION)

		self.arcom.write_char(BpodProtocol.HARDWARE_DESCRIPTION)
		max_states = self.arcom.read_uint16()
		logger.debug("Max states: %s", max_states)

		hw.cyclePeriod = self.arcom.read_uint16()
		logger.debug("Cycle period: %s", hw.cyclePeriod)
		hw.cycleFrequency = 1000000 / hw.cyclePeriod
		hw.n.EventsPerSerialChannel = self.arcom.read_uint8()
		logger.debug("Number of events per serial channel: %s", hw.n.EventsPerSerialChannel)

		hw.n.GlobalTimers = self.arcom.read_uint8()
		logger.debug("Number of global timers: %s", hw.n.GlobalTimers)

		hw.n.GlobalCounters = self.arcom.read_uint8()
		logger.debug("Number of global counters: %s", hw.n.GlobalCounters)

		hw.n.Conditions = self.arcom.read_uint8()
		logger.debug("Number of conditions: %s", hw.n.Conditions)

		hw.n.Inputs = self.arcom.read_uint8()
		logger.debug("Number of inputs: %s", hw.n.Inputs)

		hw.Inputs = self.arcom.read_char_array(array_size=hw.n.Inputs)
		logger.debug("Inputs: %s", hw.Inputs)

		hw.n.Outputs = self.arcom.read_uint8()
		logger.debug("Number of outputs: %s", hw.n.Outputs)

		hw.Outputs = self.arcom.read_char_array(array_size=hw.n.Outputs)
		logger.debug("Outputs: %s", hw.Outputs)
		hw.Outputs.append('GGG')  # WHAT IS THIS FOR??

		state_machine_info.nOutputChannels = hw.n.Outputs + 3;
		state_machine_info.maxStates = max_states;

		hw.n.UARTSerialChannels = 0;
		for i in range(hw.n.Inputs):
			if hw.Inputs[i] == 'U':
				hw.n.UARTSerialChannels += 1

		# Set input channel enable/disable
		hw.inputsEnabled = [0] * hw.n.Inputs
		PortsFound = 0
		for i in range(hw.n.Inputs):
			if hw.Inputs[i] == 'B':
				hw.inputsEnabled[i] = 1
			elif hw.Inputs[i] == 'W':
				hw.inputsEnabled[i] = 1
			if PortsFound == 0 and hw.Inputs[i] == 'P':  # Enable ports 1-3 by default
				PortsFound = 1
				hw.inputsEnabled[i] = 1
				hw.inputsEnabled[i + 1] = 1
				hw.inputsEnabled[i + 2] = 1

	def enable_ports(self, inputs_enabled):
		logger.debug("Requesting ports enabling (%s)", BpodProtocol.ENABLE_PORTS)
		logger.debug("Inputs enabled (%s): %s", len(inputs_enabled), inputs_enabled)

		self.arcom.write_char(BpodProtocol.ENABLE_PORTS)

		self.arcom.write_uint8_array(inputs_enabled)

		response = self.arcom.read_uint8()

		logger.debug("Confirmation: %s", response)

		return response

	def set_sync_channel_and_mode(self, sync_channel, sync_mode):
		logger.debug("Requesting sync configuration (%s)", BpodProtocol.SYNC_CHANNEL_MODE)

		self.arcom.write_uint8_array([ord(BpodProtocol.SYNC_CHANNEL_MODE)] + [sync_channel, sync_mode])

		# self.arcom.write_char(BpodProtocol.SYNC_CHANNEL_MODE)
		#
		# logger.debug("Setting sync channel (%s)", sync_channel)
		# response = self.arcom.write_uint8(sync_channel)
		#
		# logger.debug("Setting sync mode (%s)", sync_mode)
		# response = self.arcom.write_uint8(sync_mode)
		#

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

		logger.debug("Sending state machine (%s)", Message)
		logger.debug("Data to send (%s)", ThirtyTwoBitMessage)

		self.arcom.write_uint8_array(Message)

		self.arcom.write_uint8_array(ThirtyTwoBitMessage)

		response = self.arcom.read_uint8()

		logger.debug("Confirmation: %s", response)

		return response

	def run_state_machine(self):
		logger.debug("Requesting state machine run (%s)", BpodProtocol.RUN_STATE_MACHINE)

		self.arcom.write_char(BpodProtocol.RUN_STATE_MACHINE)
