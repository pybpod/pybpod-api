# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from pybpodapi.model.state_machine import StateMachine
from pybpodapi.model.event import Event
from pybpodapi.model.state import State

logger = logging.getLogger(__name__)


class Trial(object):
	def __init__(self, sma):
		self.bpod_start_timestamp = None  # type: float
		self.states_timestamps = {}  # {'Reward': [(429496.7295, 429496.7295)], 'WaitForPort2Poke': [(0, 429496.7295)], 'FlashStimulus': [(429496.7295, 429496.7295)], 'WaitForResponse': [(429496.7295, 429496.7295)], 'Punish': [(nan, nan)]}
		self.events_timestamps = {}  # {'Tup': [429496.7295, 429496.7295], 'Port3In': [429496.7295, 429496.7295], 'Port2In': [429496.7295, 429496.7295], 'Port2Out': [429496.7295, 429496.7295], 'Port3Out': [429496.7295], 'Port1Out': [429496.7295]}
		self.sma = sma  # type: StateMachine
		self.events = []  # type: list(Event)
		self.states = []  # type: list(State)

	def add_state_duration(self, state_name, start, end):
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

	def add_state_change(self, event_name, timestamps):
		"""

		:param str event_name:
		:param list(float) timestamps:
		:return:
		"""
		event = [event for event in self.events if event.name == event_name]  # type: list(Event)

		if not event:
			event = Event(event_name, timestamps)
			self.events.append(event)

	def export(self):
		return {'Bpod start timestamp': self.bpod_start_timestamp,
		        'Raw data': self.sma.raw_data.export(),
		        'States timestamps': self.states_timestamps,
		        'Events timestamps': self.events_timestamps}

	def __str__(self):
		return str(self.export())
