# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class SoftCodeOccurrence(object):
	"""
	SoftCode detected by Bpod's.

	:ivar int name: softcode number
	:ivar float timestamp: timestamp associated with this softcode
	"""

	def __init__(self, softcode_number, timestamp):
		self.softcode_number = softcode_number  # type: int
		self.timestamp = timestamp  # type: float

	def __str__(self):
		return "SoftCode={softcode_number} | Timestamp={timestamp}".format(softcode_number=self.softcode_number,
		                                                                   timestamp=self.timestamp)
