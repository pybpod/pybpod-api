# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import math

from bpodapi.com.bpod_com import BpodCom
from bpodapi.model.state_machine.state_machine import StateMachine
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
		self.firmware_version = None

		self.hardware = Hardware()
		self.state_machine = StateMachine()

		self.data = []

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
		self.firmware_version = self.bpod_protocol.firmware_version()
		if self.firmware_version < 8:
			raise BpodError('Error: Old firmware detected. Please update Bpod 0.7+ firmware and try again.')
		logger.info("Firmware version: %s", self.firmware_version)

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

		self.state_machine.set_up(self.hardware)

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
			for j in range(sma.nStates):
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
		sma.nStates = len(sma.state_names)

		if len(sma.manifest) > sma.nStates:
			raise BpodError(
				'Error: Could not send state machine - some states were referenced by name, but not subsequently declared.')
		Message = (ord('C'),)
		Message += (len(sma.state_names),)
		for i in range(sma.nStates):  # Send state timer transitions (for all states)
			if math.isnan(sma.state_timer_matrix[i]):
				Message += (sma.nStates,)
			else:
				Message += (sma.state_timer_matrix[i],)
		for i in range(sma.nStates):  # Send event-triggered transitions (where they are different from default)
			currentStateTransitions = sma.input_matrix[i]
			nTransitions = len(currentStateTransitions)
			Message += (nTransitions,)
			for j in range(nTransitions):
				thisTransition = currentStateTransitions[j]
				Message += (thisTransition[0],)
				destinationState = thisTransition[1]
				if math.isnan(destinationState):
					Message += (sma.nStates,)
				else:
					Message += (destinationState,)
		for i in range(sma.nStates):  # Send hardware states (where they are different from default)
			currentHardwareState = sma.output_matrix[i]
			nDifferences = len(currentHardwareState)
			Message += (nDifferences,)
			for j in range(nDifferences):
				thisHardwareConfig = currentHardwareState[j]
				Message += (thisHardwareConfig[0],)
				Message += (thisHardwareConfig[1],)
		for i in range(sma.nStates):  # Send global timer triggered transitions (where they are different from default)
			currentStateTransitions = sma.global_timers.matrix[i]
			nTransitions = len(currentStateTransitions)
			Message += (nTransitions,)
			for j in range(nTransitions):
				thisTransition = currentStateTransitions[j]
				Message += (thisTransition[0] - sma.channels.events_positions.globalTimer,)
				destinationState = thisTransition[1]
				if math.isnan(destinationState):
					Message += (sma.nStates,)
				else:
					Message += (destinationState,)
		for i in range(
				sma.nStates):  # Send global counter triggered transitions (where they are different from default)
			currentStateTransitions = sma.global_counters.matrix[i]
			nTransitions = len(currentStateTransitions)
			Message += (nTransitions,)
			for j in range(nTransitions):
				thisTransition = currentStateTransitions[j]
				Message += (thisTransition[0] - sma.channels.events_positions.globalCounter,)
				destinationState = thisTransition[1]
				if math.isnan(destinationState):
					Message += (sma.nStates,)
				else:
					Message += (destinationState,)
		for i in range(sma.nStates):  # Send condition triggered transitions (where they are different from default)
			currentStateTransitions = sma.conditions.matrix[i]
			nTransitions = len(currentStateTransitions)
			Message += (nTransitions,)
			for j in range(nTransitions):
				thisTransition = currentStateTransitions[j]
				Message += (thisTransition[0] - sma.channels.events_positions.condition,)
				destinationState = thisTransition[1]
				if math.isnan(destinationState):
					Message += (sma.nStates,)
				else:
					Message += (destinationState,)
		for i in range(self.hardware.n_global_counters):
			Message += (sma.global_counters.attached_events[i],)
		for i in range(self.hardware.n_conditions):
			Message += (sma.conditions.channels[i],)
		for i in range(self.hardware.n_conditions):
			Message += (sma.conditions.values[i],)

		sma.state_timers = sma.state_timers[:sma.nStates]

		ThirtyTwoBitMessage = [i * self.hardware.cycle_frequency for i in sma.state_timers] + \
		                      [i * self.hardware.cycle_frequency for i in sma.global_timers.timers] + \
		                      sma.global_counters.thresholds

		response = self.bpod_protocol.send_state_machine(Message, ThirtyTwoBitMessage)

		if not response:
			raise BpodError('Error: Failed to send state machine.')
		self.stateMachine = sma

	def run_state_machine(self):
		from datetime import datetime
		self.stateMachineStartTime = datetime.now()
		RawEvents = Struct()
		eventPos = 0
		currentState = 0
		StateChangeIndexes = []
		RawEvents.Events = []
		RawEvents.EventTimestamps = []
		RawEvents.States = [currentState]
		RawEvents.StateTimestamps = [0]
		RawEvents.TrialStartTimestamp = 0;

		self.bpod_protocol.run_state_machine()

		runningStateMachine = True
		while runningStateMachine:
			if self.bpod_protocol.arcom.bytesAvailable() > 0:
				opCodeBytes = self.serialObject.readArray(2, 'uint8')
				opCode = opCodeBytes[0]
				if opCode == 1:  # Read events
					nCurrentEvents = opCodeBytes[1]
					CurrentEvents = self.bpod_protocol.arcom.read_uint8(nCurrentEvents)
					TransitionEventFound = False
					for i in range(nCurrentEvents):
						thisEvent = CurrentEvents[i]
						if thisEvent == 255:
							runningStateMachine = False
						else:
							RawEvents.Events.append(thisEvent)
							if not TransitionEventFound:
								thisStateTransitions = self.stateMachine.input_matrix[currentState]
								nTransitions = len(thisStateTransitions)
								for j in range(nTransitions):
									thisTransition = thisStateTransitions[j]
									if thisTransition[0] == thisEvent:
										currentState = thisTransition[1]
										if not math.isnan(currentState):
											RawEvents.States.append(currentState)
											StateChangeIndexes.append(len(RawEvents.Events) - 1)
										TransitionEventFound = True
							if not TransitionEventFound:
								thisStateTimerTransition = self.stateMachine.state_timer_matrix[currentState]
								if thisEvent == self.state_machine.channels.events_positions.Tup:
									if not (thisStateTimerTransition == currentState):
										currentState = thisStateTimerTransition
										if not math.isnan(currentState):
											RawEvents.States.append(currentState)
											StateChangeIndexes.append(len(RawEvents.Events) - 1)
										TransitionEventFound = True
							if not TransitionEventFound:
								thisGlobalTimerTransitions = self.stateMachine.globalTimers.matrix[currentState]
								nTransitions = len(thisGlobalTimerTransitions)
								for j in range(nTransitions):
									thisTransition = thisGlobalTimerTransitions[j]
									if thisTransition[0] == thisEvent:
										currentState = thisTransition[1]
										if not math.isnan(currentState):
											RawEvents.States.append(currentState)
											StateChangeIndexes.append(len(RawEvents.Events) - 1)
										TransitionEventFound = True
				elif opCode == 2:  # Handle soft code
					SoftCode = opCodeBytes[1]
		RawEvents.TrialStartTimestamp = float(
			self.serialObject.read('uint32')) / 1000  # Start-time of the trial in milliseconds
		nTimeStamps = self.serialObject.read('uint16')
		TimeStamps = self.serialObject.readArray(nTimeStamps, 'uint32')
		RawEvents.EventTimestamps = [i / float(self.HW.cycleFrequency) for i in TimeStamps];
		for i in range(len(StateChangeIndexes)):
			RawEvents.StateTimestamps.append(RawEvents.EventTimestamps[StateChangeIndexes[i]])
		RawEvents.StateTimestamps.append(RawEvents.EventTimestamps[-1])
		return RawEvents

	def addTrialEvents(self, RawEvents):
		if not hasattr(self.data, 'nTrials'):
			self.data.nTrials = 0
			self.data.info = Struct()
			if self.firmwareVersion < 7:
				self.data.info.BpodVersion = 5
			else:
				self.data.info.BpodVersion = 7
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

	def manualOverride(self, channelType, channelName, channelNumber, value):
		if channelType.lower() == 'input':
			raise BpodError('Manually overriding a Bpod input channel is not yet supported in Python.')
		elif channelType.lower() == 'output':
			if channelName == 'Valve':
				if value > 0:
					value = math.pow(2, channelNumber - 1)
				channelNumber = self.HW.Pos.output_SPI
				byteString = (ord('O'), channelNumber, value)
			elif channelName == 'Serial':
				byteString = (ord('U'), channelNumber, value)
			else:
				try:
					channelNumber = self.stateMachineInfo.outputChannelNames.index(channelName + str(channelNumber))
					byteString = (ord('O'), channelNumber, value)
				except:
					raise BpodError('Error using manualOverride: ' + channelName + ' is not a valid channel name.')
			self.serialObject.write(byteString, 'uint8')
		else:
			raise BpodError('Error using manualOverride: first argument must be "Input" or "Output".')

	def loadSerialMessage(self, serialChannel, messageID, message):
		nMessages = 1
		messageLength = len(message)
		if messageLength > 3:
			raise BpodError('Error: Serial messages cannot be more than 3 bytes in length.')
		if (messageID > 255) or (messageID < 1):
			raise BpodError('Error: Bpod can only store 255 serial messages (indexed 1-255).')
		ByteString = (ord('L'), serialChannel - 1, nMessages, messageID, messageLength) + message
		print
		ByteString
		self.serialObject.write(ByteString, 'uint8')
		Confirmed = self.serialObject.read('uint8');
		if (not Confirmed):
			raise BpodError('Error: Failed to set serial message.')

	def resetSerialMessages(self):
		self.serialObject.write(ord('>'), 'uint8')
		Confirmed = self.serialObject.read('uint8');
		if (not Confirmed):
			raise BpodError('Error: Failed to reset serial message library.')

	def disconnect(self):
		self.serialObject.write(ord('Z'), 'uint8')


class Struct:
	pass


class BpodError(Exception):
	pass
