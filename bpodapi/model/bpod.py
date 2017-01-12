# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import math
from datetime import datetime

from bpodapi.com.bpod_com import BpodCom
from bpodapi.model.hardware import Hardware

from bpodapi.com.serial_containers import HardwareInfoContainer

logger = logging.getLogger(__name__)


class Bpod(object):
	"""
	Bpod main class
	"""

	def __init__(self, serialPortName):
		"""

		:param str serialPortName: serial port name
		"""
		self.hardware = Hardware()

		self.data = TrialsData()

		# [Channel,Mode] 255 = no sync, otherwise set to a hardware channel number. Mode 0 = flip logic every trial, 1 = every state
		self.sync_channel = 255
		self.sync_mode = 1

		self.bpod_protocol = BpodCom()

		self.start(serialPortName)

	def start(self, serial_port):
		"""
		Connect to bpod using serial port

		:param str serial_port:
		:return:
		"""

		self.bpod_protocol.connect(serial_port)

		# request handshake
		response = self.bpod_protocol.handshake()
		if response != '5':
			raise BpodError('Error: Bpod failed to confirm connectivity. Please reset Bpod and try again.')

		# request firmware version
		self.hardware.firmware_version = self.bpod_protocol.firmware_version()
		if self.hardware.firmware_version < 8:
			raise BpodError('Error: Old firmware detected. Please update Bpod 0.7+ firmware and try again.')
		logger.info("Firmware version: %s", self.hardware.firmware_version)

		# request hardware description
		logger.info("Reading HW description...")
		hw_info = HardwareInfoContainer()
		self.bpod_protocol.hardware_description(hw_info)

		self.hardware.set_up(hw_info)

		# request ports enabling
		logger.info("Enabling ports...")
		response = self.bpod_protocol.enable_ports(self.hardware.inputs_enabled)
		if not response:
			raise BpodError('Error: Failed to enable Bpod inputs.')

		# request sync channel and mode configuration
		logger.info("Setting sync channel and mode...")
		confirmation = self.bpod_protocol.set_sync_channel_and_mode(sync_channel=self.sync_channel,
		                                                            sync_mode=self.sync_mode)
		if not confirmation:
			raise BpodError('Error: Failed to configure syncronization.')

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
		Message = [len(sma.state_names),]
		for i in range(sma.total_states_added):  # Send state timer transitions (for all states)
			if math.isnan(sma.state_timer_matrix[i]):
				Message += (sma.total_states_added,)
			else:
				Message += (sma.state_timer_matrix[i],)
		for i in range(sma.total_states_added):  # Send event-triggered transitions (where they are different from default)
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
		for i in range(sma.total_states_added):  # Send global timer triggered transitions (where they are different from default)
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
		for i in range(sma.total_states_added):  # Send condition triggered transitions (where they are different from default)
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

	def _process_opcode(self, sma, opcode, data, raw_events, state_change_indexes, current_state):

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

	def run_state_machine(self, sma):
		self.stateMachineStartTime = datetime.now()

		raw_events = RawEvents()
		state_change_indexes = []

		current_state = 0

		self.bpod_protocol.run_state_machine()

		sma.is_running = True
		while sma.is_running:
			if self.bpod_protocol.data_available():
				opcode, data = self.bpod_protocol.read_opcode_message()
				self._process_opcode(sma, opcode, data, raw_events, state_change_indexes, current_state)

		raw_events.trial_start_timestamp.append(self.bpod_protocol.read_trial_start_timestamp_ms()) # start timestamp of first trial
		timestamps = self.bpod_protocol.read_timestamps()

		raw_events.event_timestamps = [i / float(self.hardware.cycle_frequency) for i in timestamps];
		for state_change_idx in state_change_indexes:
			raw_events.state_timestamps.append(raw_events.event_timestamps[state_change_idx])
		raw_events.state_timestamps.append(raw_events.event_timestamps[-1])

		return raw_events

	def add_trial_events(self):

		if self.data.n_trials == 0:
			self.data.sessionDateTime = self.stateMachineStartTime
			self.data.sessionStartTime = str(self.stateMachineStartTime)
			self.data.trialStartTimestamp = []
			self.data.rawData = []
			self.data.rawEvents = Struct()
			self.data.rawEvents.Trial = []

		self.data.rawEvents.Trial.append(Struct())
		self.data.rawEvents.Trial[self.data.nTrials].Events = Struct()
		self.data.rawEvents.Trial[self.data.nTrials].States = Struct()
		self.data.trialStartTimestamp.append(RawEvents.TrialStartTimestamp)
		self.data.rawData.append(RawEvents)
		states = RawEvents.States
		events = RawEvents.Events
		nStates = len(states)
		nEvents = len(events)
		nPossibleStates = self.stateMachine.nStates
		visitedStates = [0] * nPossibleStates
		# determine unique states while preserving visited order
		uniqueStates = []
		nUniqueStates = 0
		uniqueStateIndexes = [0] * nStates
		for i in range(nStates):
			if states[i] in uniqueStates:
				uniqueStateIndexes[i] = uniqueStates.index(states[i])
			else:
				uniqueStateIndexes[i] = nUniqueStates
				nUniqueStates += 1
				uniqueStates.append(states[i])
				visitedStates[states[i]] = 1
		uniqueStateDataMatrices = [[] for i in range(nStates)]
		# Create a 2-d matrix for each state in a list
		for i in range(nStates):
			uniqueStateDataMatrices[uniqueStateIndexes[i]] += [
				(RawEvents.StateTimestamps[i], RawEvents.StateTimestamps[i + 1])]
		# Append one matrix for each unique state
		for i in range(nUniqueStates):
			thisStateName = self.stateMachine.stateNames[uniqueStates[i]]
			setattr(self.data.rawEvents.Trial[self.data.nTrials].States, thisStateName, uniqueStateDataMatrices[i])
		for i in range(nPossibleStates):
			thisStateName = self.stateMachine.stateNames[i]
			if not visitedStates[i]:
				setattr(self.data.rawEvents.Trial[self.data.nTrials].States, thisStateName,
				        [(float('NaN'), float('NaN'))])
		for i in range(nEvents):
			thisEvent = events[i]
			thisEventName = self.stateMachineInfo.eventNames[thisEvent]
			thisEventIndexes = [j for j, k in enumerate(events) if k == thisEvent]
			thisEventTimestamps = []
			for i in thisEventIndexes:
				thisEventTimestamps.append(RawEvents.EventTimestamps[i])
			setattr(self.data.rawEvents.Trial[self.data.nTrials].Events, thisEventName, thisEventTimestamps)
		self.data.nTrials += 1

	def manual_override(self, sma, channel_type, channel_name, channel_number, value):
		if channel_type.lower() == 'input':
			raise BpodError('Manually overriding a Bpod input channel is not yet supported in Python.')
		elif channel_type.lower() == 'output':
			if channel_name == 'Valve':
				if value > 0:
					value = math.pow(2, channel_number - 1)
					channel_number = sma.channels.events_positions.output_SPI
				byteString = (ord('O'), channel_number, value)
			elif channel_name == 'Serial':
				byteString = (ord('U'), channel_number, value)
			else:
				try:
					channel_number = self.stateMachineInfo.outputChannelNames.index(channel_name + str(channel_number))
					byteString = (ord('O'), channel_number, value)
				except:
					raise BpodError('Error using manualOverride: ' + channel_name + ' is not a valid channel name.')
			self.serialObject.write(byteString, 'uint8')
		else:
			raise BpodError('Error using manualOverride: first argument must be "Input" or "Output".')

	def load_serial_message(self, serial_channel, message_ID, message):
		nMessages = 1

		if len(message) > 3:
			raise BpodError('Error: Serial messages cannot be more than 3 bytes in length.')

		if message_ID > 255 or message_ID < 1:
			raise BpodError('Error: Bpod can only store 255 serial messages (indexed 1-255).')

		message_container = (serial_channel - 1, nMessages, message_ID, len(message), message)

		response = self.bpod_protocol.load_serial_message(message_container);
		if not response:
			raise BpodError('Error: Failed to set serial message.')

	def reset_serial_messages(self):
		"""
		Reset serial messages
		"""
		response = self.reset_serial_messages()
		if not response:
			raise BpodError('Error: Failed to reset serial message library.')

	def disconnect(self):
		"""
		Close connection with Bpod
		"""
		self.bpod_protocol.disconnect()

class TrialsData(object):
	def __init__(self):
		self.n_trials = 0
		self.session_date_time = None
		self.session_start_time = None
		self.raw_data = []

class RawEvents(object):
	def __init__(self):
		self.events = []
		self.event_timestamps = []
		self.states = [0]
		self.state_timestamps = [0]
		self.trial_start_timestamp = [];
		self.trials = []

	def __str__(self):
		data_dict = {'States': self.states,
		             'TrialStartTimestamp': self.trial_start_timestamp,
		             'EventTimestamps': self.event_timestamps,
		             'Events': self.events,
		             'StateTimestamps': self.state_timestamps}

		return str(data_dict)


class BpodError(Exception):
	pass
