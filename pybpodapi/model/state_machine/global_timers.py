# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class GlobalTimers(object):
	def __init__(self, max_states, n_global_timers):
		self.matrix = [[] for i in range(max_states)]
		self.timers = [0] * n_global_timers
