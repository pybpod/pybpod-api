# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class Event(object):
	"""
	Bpod event (or state change). An event may occur several times, thus it has a list of timestamps.
	"""
	def __init__(self, name, timestamps=[]):
		self.name = name  # type: str
		self.timestamps = timestamps  # type: list(float)

	def __str__(self):
		return "{name}: {timestamps}".format(name=self.name, timestamps=self.timestamps)
