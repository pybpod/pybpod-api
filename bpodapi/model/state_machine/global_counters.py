# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class GlobalCounters(object):
	def __init__(self, max_states, n_global_counters):
		self.matrix = [[] for i in range(max_states)]
		self.attached_events = [254] * n_global_counters
		self.thresholds = [0] * n_global_counters
