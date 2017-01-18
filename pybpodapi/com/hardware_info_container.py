# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class HardwareInfoContainer(object):
	"""
	Temporarily store hardware information read from Bpod
	"""

	def __init__(self):
		self.max_states = None
		self.cycle_period = None
		self.n_events_per_serial_channel = None
		self.n_global_timers = None
		self.n_global_counters = None
		self.n_conditions = None
		self.n_inputs = None
		self.inputs = None
		self.n_outputs = None
		self.outputs = None
		self.sync_channel = None # type: int
		self.sync_mode = None # type: int
