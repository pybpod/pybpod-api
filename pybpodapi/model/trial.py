# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from pybpodapi.model.state_machine import StateMachine
from pybpodapi.model.event_occurrence import EventOccurrence
from pybpodapi.model.state_occurrences import StateOccurrences

logger = logging.getLogger(__name__)


class Trial(object):
	"""
	:ivar float bpod_start_timestamp: None
	:ivar StateMachine sma: sma
	:ivar list(StateOccurrences) state_occurrences: list of state occurrences
	:ivar list(EventOccurrence) events_occurrences: list of event occurrences 
	"""

	def __init__(self, sma):

		self.bpod_start_timestamp = None
		self.sma = sma  # type: StateMachine
		self.states_occurrences = []  # type: list(StateOccurrences)
		self.events_occurrences = []  # type: list(EventOccurrence)

	def add_state_duration(self, state_name, start, end):
		"""
		Add state duration to state. If state doesn't exist, create a new one.
		
		:param str state_name: name of the sate
		:param float start: start timestamp
		:param float end: end timestamp
		"""
		state = [state for state in self.states_occurrences if state.name == state_name]  # type: list(StateOccurrences)

		if not state:
			state = StateOccurrences(state_name)
			self.states_occurrences.append(state)
		else:
			state = state[0]

		state.add_state_dur(start, end)

	def get_all_timestamps_by_state(self):
		"""
		Create a dictionary whose keys are state names and values are corresponding timestamps (start and end)

		This is just a convenient method for getting all states occurrences as a dictionary. 

		Example:

		.. code-block:: python

			{
				'TimerTrig': [(0, 0.0001)],
				'Reward': [(429496.7295, 429496.7295)],
				'WaitForPort2Poke': [(0, 429496.7295)], 
				'FlashStimulus': [(429496.7295, 429496.7295)],
				'WaitForResponse': [(429496.7295, 429496.7295)],
				'Punish': [(nan, nan)]}
			}

		:rtype: dict 
		"""
		all_timestamps = {}
		for state in self.states_occurrences:
			all_timestamps[state.name] = [(state_dur.start, state_dur.end) for state_dur in state.timestamps]

		return all_timestamps

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
		
		.. code-block:: python
		
			{
				'Tup': [429496.7295, 429496.7295], 
				'Port3In': [429496.7295, 429496.7295], 
				'Port2In': [429496.7295, 429496.7295], 
				'Port2Out': [429496.7295, 429496.7295], 
				'Port3Out': [429496.7295], 
				'Port1Out': [429496.7295]
			}
		
		:rtype: dict 
		"""
		all_timestamps = {}
		for event_name in self.get_events_names():
			all_timestamps[event_name] = self.get_timestamps_by_event_name(event_name)

		return all_timestamps

	def export(self):
		return {'Bpod start timestamp': self.bpod_start_timestamp,
		        'States timestamps': self.get_all_timestamps_by_state(),
		        'Events timestamps': self.get_all_timestamps_by_event()}

	def __str__(self):
		return str(self.export())
