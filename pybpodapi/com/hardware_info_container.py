# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class HardwareInfoContainer(object):
	"""
	Temporarily store hardware information read from Bpod
	"""

	def __init__(self):
		self.max_states = None # type: int
		self.cycle_period = None # type: int
		self.n_events_per_serial_channel = None # type: int
		self.n_global_timers = None # type: int
		self.n_global_counters = None # type: int
		self.n_conditions = None # type: int
		self.n_inputs = None # type: int
		self.inputs = None
		self.n_outputs = None # type: int
		self.outputs = None
		self.sync_channel = None # type: int
		self.sync_mode = None # type: int
