# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class EventOccurrence(object):
	"""
	Bpod event. An event may occur several times, thus it has a timestamp.
	"""

	def __init__(self, name, index, timestamp):
		self.name = name  # type: str
		self.index = index  # type: int
		self.timestamp = timestamp  # type: float

	def __str__(self):
		return "Name={name} | Index={index} | Timestamp={timestamp}".format(name=self.name, index=self.index,
		                                                                    timestamp=self.timestamp)
