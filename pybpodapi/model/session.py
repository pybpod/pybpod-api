# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from datetime import datetime

from pybpodapi.model.state_machine import StateMachine
from pybpodapi.model.trial import Trial

logger = logging.getLogger(__name__)


class Session(object):
	"""

	"""

	def __init__(self):
		self.trials = []  # type: list[Trial]
		self.firmware_version = None  # type: int
		self.bpod_version = None  # type: int
		self.datetime = datetime.now()  # type: datetime

	def add_trial(self, sma):
		"""
		Add new trial to this session and associate a state machine to it

		:param StateMachine sma: state machine associated with this trial
		"""
		new_trial = Trial(sma)

		self.trials.append(new_trial)

	def add_trial_events(self):

		current_trial = self.current_trial()  # type: Trial
		sma_data = current_trial.sma.raw_data
		sma = current_trial.sma

		current_trial.bpod_start_timestamp = sma_data.trial_start_timestamp

		visitedStates = [0] * current_trial.sma.total_states_added
		# determine unique states while preserving visited order
		uniqueStates = []
		nUniqueStates = 0
		uniqueStateIndexes = [0] * len(sma_data.states)

		for i in range(len(sma_data.states)):
			if sma_data.states[i] in uniqueStates:
				uniqueStateIndexes[i] = uniqueStates.index(sma_data.states[i])
			else:
				uniqueStateIndexes[i] = nUniqueStates
				nUniqueStates += 1
				uniqueStates.append(sma_data.states[i])
				visitedStates[sma_data.states[i]] = 1

		# Create a 2-d matrix for each state in a list
		uniqueStateDataMatrices = [[] for i in range(len(sma_data.states))]

		# Append one matrix for each unique state
		for i in range(len(sma_data.states)):
			uniqueStateDataMatrices[uniqueStateIndexes[i]] += [
				(sma_data.state_timestamps[i], sma_data.state_timestamps[i + 1])]

		for i in range(nUniqueStates):
			thisStateName = sma.state_names[uniqueStates[i]]
			current_trial.states_timestamps[thisStateName] = uniqueStateDataMatrices[i]

			for state_dur in uniqueStateDataMatrices[i]:
				current_trial.add_state_duration(thisStateName, state_dur[0], state_dur[1])

		logger.debug("State names: %s", sma.state_names)
		logger.debug("nPossibleStates: %s", sma.total_states_added)
		for i in range(sma.total_states_added):
			thisStateName = sma.state_names[i]
			if not visitedStates[i]:
				current_trial.states_timestamps[thisStateName] = [(float('NaN'), float('NaN'))]
				current_trial.add_state_duration(thisStateName, float('NaN'), float('NaN'))

		logger.debug("Trial states: %s", [str(state) for state in current_trial.states])

		# save events occurrences on trial and make available a dictionary with all information
		current_trial.events_occurrences = sma.raw_data.events_occurrences  # type: list
		current_trial.events_timestamps = sma.raw_data.get_all_timestamps_by_event()  # type: dict

		logger.debug("Trial events: %s", [str(event) for event in current_trial.events_occurrences])

		logger.debug("Trial info: %s", str(current_trial))

	def current_trial(self):
		"""
		Get current trial
		
		:rtype: Trial 
		"""
		return self.trials[-1]
