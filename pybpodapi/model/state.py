# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class State(object):
	def __init__(self, name):
		"""

		:param name:
		"""
		self.name = name  # type: str
		self.timestamps = []  # type: list(StateDuration)

	def add_state_dur(self, start, end):
		"""

		:param start:
		:param end:
		:return:
		"""
		self.timestamps.append(StateDuration(start, end))

	def __str__(self):
		formatted_timestamps = [str(state_dur) for state_dur in self.timestamps]
		return "{name}: {timestamps}".format(name=self.name, timestamps=formatted_timestamps)


class StateDuration(object):
	def __init__(self, start, end):
		"""

		:param start:
		:param end:
		"""
		self.start = start  # type: float
		self.end = end  # type: float

	def __str__(self):
		return "({0}, {1})".format(self.start, self.end)
