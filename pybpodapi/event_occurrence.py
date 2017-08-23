# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class EventOccurrence(object):
	"""
	Events detected by Bpod's inputs can be set to trigger transitions between specific states.
	
	An event may occur several times, thus it has a timestamp.
	
	:ivar str name: name of the event
	:ivar int index: index of the event
	:ivar float timestamp: timestamp associated with this event
	"""

	def __init__(self, name, index, timestamp):
		self.name = name  # type: str
		self.index = index  # type: int
		self.timestamp = timestamp  # type: float

	def __str__(self):
		return "Name={name} | Index={index} | Timestamp={timestamp}".format(name=self.name, index=self.index,
		                                                                    timestamp=self.timestamp)
