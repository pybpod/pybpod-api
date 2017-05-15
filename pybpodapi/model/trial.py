# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from pybpodapi.model.state_machine import StateMachine
from pybpodapi.model.event_occurrence import EventOccurrence
from pybpodapi.model.state import State

logger = logging.getLogger(__name__)


class Trial(object):
	"""
	:ivar float bpod_start_timestamp: None
	:ivar dict states_timestamps: {}
	:ivar dict events_timestamps: {}
	:ivar StateMachine sma: sma
	"""

	def __init__(self, sma):

		self.bpod_start_timestamp = None
		self.states_timestamps = {}  # {'Reward': [(429496.7295, 429496.7295)], 'WaitForPort2Poke': [(0, 429496.7295)], 'FlashStimulus': [(429496.7295, 429496.7295)], 'WaitForResponse': [(429496.7295, 429496.7295)], 'Punish': [(nan, nan)]}
		self.events_timestamps = {}  # {'Tup': [429496.7295, 429496.7295], 'Port3In': [429496.7295, 429496.7295], 'Port2In': [429496.7295, 429496.7295], 'Port2Out': [429496.7295, 429496.7295], 'Port3Out': [429496.7295], 'Port1Out': [429496.7295]}
		self.sma = sma  # type: StateMachine
		self.states = []  # type: list(State)
		self.events_occurrences = []  # type: list(EventOccurrence)

	def add_state_duration(self, state_name, start, end):
		"""
		Add state duration to state. If state doesn't exist, create a new one.
		
		:param str state_name: name of the sate
		:param float start: start timestamp
		:param float end: end timestamp
		"""
		state = [state for state in self.states if state.name == state_name]  # type: list(State)

		if not state:
			state = State(state_name)
			self.states.append(state)
		else:
			state = state[0]

		state.add_state_dur(start, end)

	def get_timestamps_by_event_name(self, event_name):
		"""
		Get timestamps by event name
		
		:param event_name: name of the event to get timestamps
		:rtype: list(float) 
		"""
		event_timestamps = []  # type: list(float)

		for event in self.events_occurrences:
			if event.name == event_name:
				event_timestamps.append(event.timestamp)

		return event_timestamps

	def get_events_names(self):
		"""
		Get events names without repetitions
		
		:rtype: list(str) 
		"""
		events_names = []  # type: list(str)

		for event in self.events_occurrences:
			if event.name not in events_names:
				events_names.append(event.name)

		return events_names

	def get_all_timestamps_by_event(self):
		"""
		Create a dictionary whose keys are events names and values are corresponding timestamps
		
		Example:
		{'Tup': [429496.7295, 429496.7295], 'Port3In': [429496.7295, 429496.7295], 'Port2In': [429496.7295, 429496.7295], 'Port2Out': [429496.7295, 429496.7295], 'Port3Out': [429496.7295], 'Port1Out': [429496.7295]}
		
		:return: 
		"""
		all_timestamps = {}
		for event_name in self.get_events_names():
			all_timestamps[event_name] = self.get_timestamps_by_event_name(event_name)

		return all_timestamps

	def export(self):
		return {'Bpod start timestamp': self.bpod_start_timestamp,
		        'Raw data': self.sma.raw_data.export(),
		        'States timestamps': self.states_timestamps,
		        'Events timestamps': self.events_timestamps}

	def __str__(self):
		return str(self.export())
