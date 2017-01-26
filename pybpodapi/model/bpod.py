# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import math

from pybpodapi.com.message_api import MessageAPI
from pybpodapi.com.hardware_info_container import HardwareInfoContainer
from pybpodapi.com.serial_message_container import SerialMessageContainer
from pybpodapi.hardware.hardware import Hardware
from pybpodapi.hardware.channels import ChannelType
from pybpodapi.hardware.channels import ChannelName
from pybpodapi.model.session import Session
from pybpodapi.model.state_machine import StateMachine
from pybpodapi.model.trial import Trial
from pybpodapi.model.state_machine.raw_data import RawData

logger = logging.getLogger(__name__)


class Status():
	def __init__(self):
		self.new_sma_sent = False  # type: bool


class Bpod(object):
	"""
	Bpod is the main entity.
	"""

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

	@hardware.setter
	def hardware(self, value):
		self._hardware = value  # type: Hardware

	@property
	def message_api(self):
		return self._message_api  # type: MessageAPI

	@message_api.setter
	def message_api(self, value):
		self._message_api = value  # type: MessageAPI

	@property
	def status(self):
		return self._status  # type: Status

	@status.setter
	def status(self, value):
		self._status = value  # type: Status

	#########################################
	############ PUBLIC METHODS #############
	#########################################

	def start(self, serial_port, baudrate=115200, sync_channel=255, sync_mode=1):
		"""
		Starts Bpod.

		Connect to Bpod board through serial port, test handshake, retrieve firmware version,
		retrieve hardware description, enable input ports and configure channel synchronization.

		:param str serial_port: serial port to connect
		:param int baudrate: baudrate for serial connection
		:param int sync_channel: Serial synchronization channel: 255 = no sync, otherwise set to a hardware channel number
		:param int sync_mode: Serial synchronization mode: 0 = flip logic every trial, 1 = every state
		:return: reference to Bpod class
		:return type: Bpod
		"""

		self.hardware = Hardware()  # type: Hardware
		self.session = Session()  # type: Session
		self.message_api = MessageAPI()  # type: MessageAPI
		self.status = Status()  # type: Status

		self.message_api.connect(serial_port, baudrate)

		if not self.message_api.handshake():
			raise BpodError('Error: Bpod failed to confirm connectivity. Please reset Bpod and try again.')

		self.hardware.firmware_version = self.message_api.firmware_version()
		if self.hardware.firmware_version < 8:
			raise BpodError('Error: Old firmware detected. Please update Bpod 0.7+ firmware and try again.')

		hw_info = HardwareInfoContainer()
		hw_info.sync_channel = sync_channel
		hw_info.sync_mode = sync_mode
		self.message_api.hardware_description(hw_info)
		self.hardware.set_up(hw_info)

		if not self.message_api.enable_ports(self.hardware.inputs_enabled):
			raise BpodError('Error: Failed to enable Bpod inputs.')

		if not self.message_api.set_sync_channel_and_mode(sync_channel=sync_channel,
		                                                  sync_mode=sync_mode):
			raise BpodError('Error: Failed to configure syncronization.')

		logger.info("Bpod successfully started!")

		return self

	def send_state_machine(self, sma):
		"""
		Send state machine to Bpod

		:param sma: initialized state machine
		:type sma: StateMachine
		"""

		sma.update_state_numbers()

		message = sma.build_message()

		message32 = sma.build_message_32_bits()

		self.status.new_sma_sent = True

		self.message_api.send_state_machine(message, message32)

	def run_state_machine(self, sma):
		"""

		Run state machine on Bpod now

		:param sma: initialized state machine
		:type sma: StateMachine
		:return: state machine raw data
		:rtype: RawData
		"""

		self.session.add_trial(sma)

		state_change_indexes = []

		current_state = 0

		self.message_api.run_state_machine()
		if self.status.new_sma_sent:
			if not self.message_api.state_machine_installation_status():
				raise BpodError('Error: The last state machine sent was not acknowledged by the Bpod device.')
			self.status.new_sma_sent = False

		sma.is_running = True
		while sma.is_running:
			if self.message_api.data_available():
				opcode, data = self.message_api.read_opcode_message()
				self.__process_opcode(sma, opcode, data, state_change_indexes, current_state)

		self.__update_timestamps(sma, state_change_indexes)

		return sma.raw_data

	def add_trial_events(self):
		"""

		:param StateMachine sma: state machine associated with this trial
		:param raw_events:
		"""

		self.session.add_trial_events()

	def manual_override(self, channel_type, channel_name, channel_number, value):
		"""
		Manually override a Bpod channel

		:param ChannelType channel_type: channel type input or output
		:param ChannelName channel_name: channel name like PWM, Valve, etc.
		:param channel_number:
		:param int value: value to write on channel
		"""
		if channel_type == ChannelType.INPUT:
			raise BpodError('Manually overriding a Bpod input channel is not yet supported in Python.')
		elif channel_type == ChannelType.OUTPUT:
			if channel_name == ChannelName.VALVE:
				if value > 0:
					value = math.pow(2, channel_number - 1)
				channel_number = self.hardware.channels.events_positions.output_SPI
				self.message_api.override_digital_hardware_state(channel_number, value)
			elif channel_name == 'Serial':
				self.message_api.send_byte_to_hardware_serial(channel_number, value)
			else:
				try:
					channel_number = self.hardware.channels.output_channel_names.index(
						channel_name + str(channel_number))
					self.message_api.override_digital_hardware_state(channel_number, value)
				except:
					raise BpodError('Error using manual_override: ' + channel_name + ' is not a valid channel name.')
		else:
			raise BpodError('Error using manualOverride: first argument must be "Input" or "Output".')

	def load_serial_message(self, serial_channel, message_ID, serial_message, n_messages=1):
		"""
		Load serial message on Bpod

		:param serial_channel:
		:param message_ID:
		:param serial_message:
		:param n_messages:
		:return:
		"""

		message_container = SerialMessageContainer(serial_channel, message_ID, serial_message,
		                                           n_messages)  # type: SerialMessageContainer

		response = self.message_api.load_serial_message(message_container.format_for_sending());

		if not response:
			raise BpodError('Error: Failed to set serial message.')

	def reset_serial_messages(self):
		"""
		Reset serial messages to equivalent byte codes (i.e. message# 4 = one byte, 0x4)
		"""
		response = self.message_api.reset_serial_messages()

		if not response:
			raise BpodError('Error: Failed to reset serial message library.')

	def disconnect(self):
		"""
		Close connection with Bpod
		"""
		self.message_api.disconnect()

	#########################################
	############ PRIVATE METHODS ############
	#########################################

	def __process_opcode(self, sma, opcode, data, state_change_indexes, current_state):

		raw_events = sma.raw_data  # legacy fix

		if opcode == 1:  # Read events
			n_current_events = data
			current_events = self.message_api.read_current_events(n_current_events)
			transition_event_found = False
			for event in current_events:
				if event == 255:
					sma.is_running = False
				else:
					raw_events.events.append(event)

					# input matrix
					if not transition_event_found:
						for transition in sma.input_matrix[current_state]:
							if transition[0] == event:
								current_state = transition[1]
								if not math.isnan(current_state):
									raw_events.states.append(current_state)
									state_change_indexes.append(len(raw_events.events) - 1)
								transition_event_found = True

					# state timer matrix
					if not transition_event_found:
						this_state_timer_transition = sma.state_timer_matrix[current_state]
						if event == sma.channels.events_positions.Tup:
							if not (this_state_timer_transition == current_state):
								current_state = this_state_timer_transition
								if not math.isnan(current_state):
									raw_events.states.append(current_state)
									state_change_indexes.append(len(raw_events.events) - 1)
								transition_event_found = True

					# global timers start matrix
					if not transition_event_found:
						for transition in sma.global_timers.start_matrix[current_state]:
							if transition[0] == event:
								current_state = transition[1]
								if not math.isnan(current_state):
									raw_events.states.append(current_state)
									state_change_indexes.append(len(raw_events.events) - 1)
								transition_event_found = True

					# global timers end matrix
					if not transition_event_found:
						for transition in sma.global_timers.end_matrix[current_state]:
							if transition[0] == event:
								current_state = transition[1]
								if not math.isnan(current_state):
									raw_events.states.append(current_state)
									state_change_indexes.append(len(raw_events.events) - 1)
								transition_event_found = True

		elif opcode == 2:  # Handle soft code
			logger.info("Soft code: %s", data)

	def __update_timestamps(self, sma, state_change_indexes):
		"""
		Read timestamps from Bpod and update state machine info

		:param StateMachine sma:
		:param list state_change_indexes:
		"""
		sma.raw_data.trial_start_timestamp.append(
			self.message_api.read_trial_start_timestamp_ms())  # start timestamp of first trial

		timestamps = self.message_api.read_timestamps()

		sma.raw_data.event_timestamps = [i / float(self.hardware.cycle_frequency) for i in timestamps];

		logger.debug("state_change_indexes: %s", state_change_indexes)
		for i in range(len(state_change_indexes)):
			sma.raw_data.state_timestamps.append(sma.raw_data.event_timestamps[i])
			sma.raw_data.state_timestamps.append(sma.raw_data.event_timestamps[-1])


class BpodError(Exception):
	pass
