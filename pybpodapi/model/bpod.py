# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import math

from pybpodapi.com.protocol import Protocol
from pybpodapi.com.hardware_info_container import HardwareInfoContainer
from pybpodapi.com.serial_message_container import SerialMessageContainer
from pybpodapi.hardware.hardware import Hardware
from pybpodapi.hardware.channels import ChannelType
from pybpodapi.hardware.channels import ChannelName
from pybpodapi.model.session import Session
from pybpodapi.model.state_machine.state_machine import StateMachine
from pybpodapi.model.trial import Trial


logger = logging.getLogger(__name__)


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
	def bpod_protocol(self):
		return self._bpod_protocol  # type: Protocol

	@bpod_protocol.setter
	def bpod_protocol(self, value):
		self._bpod_protocol = value  # type: Protocol

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
		self.bpod_protocol = Protocol()  # type: Protocol

		self.bpod_protocol.connect(serial_port, baudrate)

		if not self.bpod_protocol.handshake():
			raise BpodError('Error: Bpod failed to confirm connectivity. Please reset Bpod and try again.')

		self.hardware.firmware_version = self.bpod_protocol.firmware_version()
		if self.hardware.firmware_version < 8:
			raise BpodError('Error: Old firmware detected. Please update Bpod 0.7+ firmware and try again.')

		hw_info = HardwareInfoContainer()
		hw_info.sync_channel = sync_channel
		hw_info.sync_mode = sync_mode
		self.bpod_protocol.hardware_description(hw_info)
		self.hardware.set_up(hw_info)

		if not self.bpod_protocol.enable_ports(self.hardware.inputs_enabled):
			raise BpodError('Error: Failed to enable Bpod inputs.')

		if not self.bpod_protocol.set_sync_channel_and_mode(sync_channel=sync_channel,
		                                                    sync_mode=sync_mode):
			raise BpodError('Error: Failed to configure syncronization.')

		logger.info("Bpod successfully started!")

		return self

	def send_state_machine(self, sma):
		"""
		Replace undeclared states (at the time they were referenced) with actual state numbers

		:param sma:
		:type sma: bpodapi.model.state_machine.state_machine.StateMachine
		:return:
		"""

		for i in range(len(sma.undeclared)):
			undeclaredStateNumber = i + 10000
			thisStateNumber = sma.manifest.index(sma.undeclared[i])
			for j in range(sma.total_states_added):
				if sma.state_timer_matrix[j] == undeclaredStateNumber:
					sma.state_timer_matrix[j] = thisStateNumber
				inputTransitions = sma.input_matrix[j]
				for k in range(0, len(inputTransitions)):
					thisTransition = inputTransitions[k]
					if thisTransition[1] == undeclaredStateNumber:
						inputTransitions[k] = (thisTransition[0], thisStateNumber)
				sma.input_matrix[j] = inputTransitions
				inputTransitions = sma.global_timers.matrix[j]
				for k in range(0, len(inputTransitions)):
					thisTransition = inputTransitions[k]
					if thisTransition[1] == undeclaredStateNumber:
						inputTransitions[k] = (thisTransition[0], thisStateNumber)
				sma.global_timers.matrix[j] = inputTransitions
				inputTransitions = sma.global_counters.matrix[j]
				for k in range(0, len(inputTransitions)):
					thisTransition = inputTransitions[k]
					if thisTransition[1] == undeclaredStateNumber:
						inputTransitions[k] = (thisTransition[0], thisStateNumber)
				sma.global_counters.matrix[j] = inputTransitions
				inputTransitions = sma.conditions.matrix[j]
				for k in range(0, len(inputTransitions)):
					thisTransition = inputTransitions[k]
					if thisTransition[1] == undeclaredStateNumber:
						inputTransitions[k] = (thisTransition[0], thisStateNumber)
				sma.conditions.matrix[j] = inputTransitions

		# Check to make sure all states in manifest exist
		logger.debug("Total states added: %s | Manifested sates: %s", sma.total_states_added, len(sma.manifest))
		if len(sma.manifest) > sma.total_states_added:
			raise BpodError(
				'Error: Could not send state machine - some states were referenced by name, but not subsequently declared.')
		Message = [len(sma.state_names), ]
		for i in range(sma.total_states_added):  # Send state timer transitions (for all states)
			if math.isnan(sma.state_timer_matrix[i]):
				Message += (sma.total_states_added,)
			else:
				Message += (sma.state_timer_matrix[i],)
		for i in range(
				sma.total_states_added):  # Send event-triggered transitions (where they are different from default)
			currentStateTransitions = sma.input_matrix[i]
			nTransitions = len(currentStateTransitions)
			Message += (nTransitions,)
			for j in range(nTransitions):
				thisTransition = currentStateTransitions[j]
				Message += (thisTransition[0],)
				destinationState = thisTransition[1]
				if math.isnan(destinationState):
					Message += (sma.total_states_added,)
				else:
					Message += (destinationState,)
		for i in range(sma.total_states_added):  # Send hardware states (where they are different from default)
			currentHardwareState = sma.output_matrix[i]
			nDifferences = len(currentHardwareState)
			Message += (nDifferences,)
			for j in range(nDifferences):
				thisHardwareConfig = currentHardwareState[j]
				Message += (thisHardwareConfig[0],)
				Message += (thisHardwareConfig[1],)
		for i in range(
				sma.total_states_added):  # Send global timer triggered transitions (where they are different from default)
			currentStateTransitions = sma.global_timers.matrix[i]
			nTransitions = len(currentStateTransitions)
			Message += (nTransitions,)
			for j in range(nTransitions):
				thisTransition = currentStateTransitions[j]
				Message += (thisTransition[0] - sma.channels.events_positions.globalTimer,)
				destinationState = thisTransition[1]
				if math.isnan(destinationState):
					Message += (sma.total_states_added,)
				else:
					Message += (destinationState,)
		for i in range(
				sma.total_states_added):  # Send global counter triggered transitions (where they are different from default)
			currentStateTransitions = sma.global_counters.matrix[i]
			nTransitions = len(currentStateTransitions)
			Message += (nTransitions,)
			for j in range(nTransitions):
				thisTransition = currentStateTransitions[j]
				Message += (thisTransition[0] - sma.channels.events_positions.globalCounter,)
				destinationState = thisTransition[1]
				if math.isnan(destinationState):
					Message += (sma.total_states_added,)
				else:
					Message += (destinationState,)
		for i in range(
				sma.total_states_added):  # Send condition triggered transitions (where they are different from default)
			currentStateTransitions = sma.conditions.matrix[i]
			nTransitions = len(currentStateTransitions)
			Message += (nTransitions,)
			for j in range(nTransitions):
				thisTransition = currentStateTransitions[j]
				Message += (thisTransition[0] - sma.channels.events_positions.condition,)
				destinationState = thisTransition[1]
				if math.isnan(destinationState):
					Message += (sma.total_states_added,)
				else:
					Message += (destinationState,)
		for i in range(self.hardware.n_global_counters):
			Message += (sma.global_counters.attached_events[i],)
		for i in range(self.hardware.n_conditions):
			Message += (sma.conditions.channels[i],)
		for i in range(self.hardware.n_conditions):
			Message += (sma.conditions.values[i],)

		sma.state_timers = sma.state_timers[:sma.total_states_added]

		ThirtyTwoBitMessage = [i * self.hardware.cycle_frequency for i in sma.state_timers] + \
		                      [i * self.hardware.cycle_frequency for i in sma.global_timers.timers] + \
		                      sma.global_counters.thresholds

		response = self.bpod_protocol.send_state_machine(Message, ThirtyTwoBitMessage)

		if not response:
			raise BpodError('Error: Failed to send state machine.')

	def run_state_machine(self, sma):

		self.session.add_trial(sma)

		state_change_indexes = []

		current_state = 0

		self.bpod_protocol.run_state_machine()

		sma.is_running = True
		while sma.is_running:
			if self.bpod_protocol.data_available():
				opcode, data = self.bpod_protocol.read_opcode_message()
				self.__process_opcode(sma, opcode, data, state_change_indexes, current_state)

		sma.raw_data.trial_start_timestamp.append(
			self.bpod_protocol.read_trial_start_timestamp_ms())  # start timestamp of first trial
		timestamps = self.bpod_protocol.read_timestamps()

		sma.raw_data.event_timestamps = [i / float(self.hardware.cycle_frequency) for i in timestamps];
		logger.debug("state_change_indexes: %s", state_change_indexes)
		for i in range(len(state_change_indexes)):
			sma.raw_data.state_timestamps.append(sma.raw_data.event_timestamps[i])
			sma.raw_data.state_timestamps.append(sma.raw_data.event_timestamps[-1])

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
				self.bpod_protocol.override_digital_hardware_state(channel_number, value)
			elif channel_name == 'Serial':
				self.bpod_protocol.send_byte_to_hardware_serial(channel_number, value)
			else:
				try:
					channel_number = self.hardware.channels.output_channel_names.index(
						channel_name + str(channel_number))
					self.bpod_protocol.override_digital_hardware_state(channel_number, value)
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

		message_container = SerialMessageContainer(serial_channel, message_ID, serial_message, n_messages) # type: SerialMessageContainer

		response = self.bpod_protocol.load_serial_message(message_container.format_for_sending());

		if not response:
			raise BpodError('Error: Failed to set serial message.')

	def reset_serial_messages(self):
		"""
		Reset serial messages to equivalent byte codes (i.e. message# 4 = one byte, 0x4)
		"""
		response = self.bpod_protocol.reset_serial_messages()

		if not response:
			raise BpodError('Error: Failed to reset serial message library.')

	def disconnect(self):
		"""
		Close connection with Bpod
		"""
		self.bpod_protocol.disconnect()

	#########################################
	############ PRIVATE METHODS ############
	#########################################

	def __process_opcode(self, sma, opcode, data, state_change_indexes, current_state):

		raw_events = sma.raw_data  # legacy fix

		if opcode == 1:  # Read events
			n_current_events = data
			current_events = self.bpod_protocol.read_current_events(n_current_events)
			transition_event_found = False
			for event in current_events:
				if event == 255:
					sma.is_running = False
				else:
					raw_events.events.append(event)
					if not transition_event_found:
						for transition in sma.input_matrix[current_state]:
							if transition[0] == event:
								current_state = transition[1]
								if not math.isnan(current_state):
									raw_events.states.append(current_state)
									state_change_indexes.append(len(raw_events.events) - 1)
								transition_event_found = True
					if not transition_event_found:
						this_state_timer_transition = sma.state_timer_matrix[current_state]
						if event == sma.channels.events_positions.Tup:
							if not (this_state_timer_transition == current_state):
								current_state = this_state_timer_transition
								if not math.isnan(current_state):
									raw_events.states.append(current_state)
									state_change_indexes.append(len(raw_events.events) - 1)
								transition_event_found = True
					if not transition_event_found:
						for transition in sma.global_timers.matrix[current_state]:
							if transition[0] == event:
								current_state = transition[1]
								if not math.isnan(current_state):
									raw_events.states.append(current_state)
									state_change_indexes.append(len(raw_events.events) - 1)
								transition_event_found = True
		elif opcode == 2:  # Handle soft code
			logger.info("Soft code: %s", data)


class BpodError(Exception):
	pass
