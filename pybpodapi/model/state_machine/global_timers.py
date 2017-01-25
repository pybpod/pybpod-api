# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class GlobalTimers(object):
	def __init__(self, max_states, n_global_timers):
		self.start_matrix = [[] for i in range(max_states)]
		self.end_matrix = [[] for i in range(max_states)]
		self.timers = [0] * n_global_timers
		self.on_set_delays = [0] * n_global_timers
		self.channels = [0] * n_global_timers
		self.on_messages = [0] * n_global_timers
		self.off_messages = [0] * n_global_timers

