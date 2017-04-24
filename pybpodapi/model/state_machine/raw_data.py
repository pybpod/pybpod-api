# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

from pybpodapi.model.event_occurrence import EventOccurrence


class RawData(object):
	def __init__(self):
		self.events = []  # type: list(int)
		self.event_timestamps = []
		self.states = [0]
		self.state_timestamps = [0]
		self.trial_start_timestamp = None  # type: float
		self.trials = []
		self.events_occurrences = []  # type: list(EventOccurrence)

	def export(self):
		return {'States': self.states,
		        'TrialStartTimestamp': self.trial_start_timestamp,
		        'EventTimestamps': self.event_timestamps,
		        'Events': self.events,
		        'StateTimestamps': self.state_timestamps}

	def add_state(self, state_name, start, end):
		"""
		Add state duration to state
		:param str state_name:
		:param float start:
		:param float end:
		:return:
		"""
		state = [state for state in self.states if state.name == state_name]  # type: list(State)

		if not state:
			state = State(state_name)
			self.states.append(state)
		else:
			state = state[0]

		state.add_state_dur(start, end)

	def add_event_occurrence(self, event_index, event_name, timestamp=None):
		"""
		Event has happened, save occurrence.
		
		:param int event_index: 
		:param str event_name: 
		:param float timestamp: (optional for now because bpod doesn't send it)
		
		:return: event object
		"""
		self.events.append(event_index)  # legacy

		event = EventOccurrence(event_name, event_index, timestamp)

		self.events_occurrences.append(event)

		return event

	# GETTERS

	def get_timestamps_by_event_name(self, event_name):
		"""
		Get timestamps by event name
		
		:param event_name: 
		:return: 
		"""
		event_timestamps = []  # type: list(float)

		for event in self.events_occurrences:
			if event.name == event_name:
				event_timestamps.append(event.timestamp)

		return event_timestamps

	def get_events_names(self):
		"""
		Get events names without repetitions
		:return: 
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

	def __str__(self):
		return str(self.export())
