# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class StateOccurrences(object):
	"""
	Store timestamps for a specific state occurrence of the state machine
	
	:ivar str name: name of the state
	:ivar list(StateDuration) timestamps: a list of timestamps (start and end) that corresponds to occurrences of this state
	"""

	def __init__(self, name):
		"""

		:param str name: name of the state
		"""
		self.name = name  # type: str
		self.timestamps = []  # type: list(StateDuration)

	def add_state_dur(self, start, end):
		"""
		Stores a new state occurrence given start and end timestamps

		:param float start: start timestamp of state duration
		:param float end: end timestamp of state duration
		"""
		self.timestamps.append(StateDuration(start, end))

	def __str__(self):
		formatted_timestamps = [str(state_dur) for state_dur in self.timestamps]
		return "{name}: {timestamps}".format(name=self.name, timestamps=formatted_timestamps)


class StateDuration(object):
	"""
	Start and End timestamps for a state
	
	:ivar float start: start timestamp of state duration
	:ivar float end: end timestamp of state duration
	"""

	def __init__(self, start, end):
		"""

		:param float start: start timestamp of state duration
		:param float end: end timestamp of state duration
		"""
		self.start = start  # type: float
		self.end = end  # type: float

	def __str__(self):
		return "({0}, {1})".format(self.start, self.end)
