# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class Conditions(object):
	def __init__(self, max_states, n_conditions):
		self.matrix 	= [[] for i in range(max_states)]
		self.values 	= [0] * n_conditions
		self.channels 	= [0] * n_conditions
