# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class RawData(object):
	def __init__(self):
		self.events = []
		self.event_timestamps = []
		self.states = [0]
		self.state_timestamps = [0]
		self.trial_start_timestamp = [];
		self.trials = []

	def __str__(self):
		data_dict = {'States': self.states,
		             'TrialStartTimestamp': self.trial_start_timestamp,
		             'EventTimestamps': self.event_timestamps,
		             'Events': self.events,
		             'StateTimestamps': self.state_timestamps}

		return str(data_dict)
