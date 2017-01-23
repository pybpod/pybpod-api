# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from pybpodapi.model.state_machine import StateMachine

logger = logging.getLogger(__name__)


class Trial(object):
	def __init__(self, sma):
		self.bpod_start_timestamp = None  # type: float
		self.states_timestamps = {}  # {'Reward': [(429496.7295, 429496.7295)], 'WaitForPort2Poke': [(0, 429496.7295)], 'FlashStimulus': [(429496.7295, 429496.7295)], 'WaitForResponse': [(429496.7295, 429496.7295)], 'Punish': [(nan, nan)]}
		self.events_timestamps = {}  # {'Tup': [429496.7295, 429496.7295], 'Port3In': [429496.7295, 429496.7295], 'Port2In': [429496.7295, 429496.7295], 'Port2Out': [429496.7295, 429496.7295], 'Port3Out': [429496.7295], 'Port1Out': [429496.7295]}
		self.sma = sma  # type: StateMachine

	def __str__(self):
		data_dict = {'Bpod start timestamp': self.bpod_start_timestamp,
		             'Raw data': str(self.sma.raw_data),
		             'States timestamps': self.states_timestamps,
		             'Events timestamps': self.events_timestamps}

		return str(data_dict)
