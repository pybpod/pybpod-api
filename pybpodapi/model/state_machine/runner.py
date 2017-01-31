# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import math

from pybpodapi.model.state_machine.builder import Builder

logger = logging.getLogger(__name__)


class Runner(Builder):
	"""
	Extend state machine with running logic
	"""

	def __init__(self, hardware):
		Builder.__init__(self, hardware)

		#: Whether this state machine is being run on bpod hardware
		self.is_running = False # type: bool

		#: Holds state machine current state while running
		self.current_state = 0 # type: int

	#########################################
	############## PROPERTIES ###############
	#########################################

	@property
	def is_running(self):
		return self._is_running  # type: bool

	@is_running.setter
	def is_running(self, value):
		self._is_running = value  # type: bool

	@property
	def current_state(self):
		return self._current_state  # type: int

	@current_state.setter
	def current_state(self, value):
		self._current_state = value  # type: int


class StateMachineRunnerError(Exception):
	pass
