# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

API_LOG_LEVEL = logging.INFO
EXAMPLE_SCRIPT_LOG_LEVEL = logging.INFO
SERIAL_PORT = None

try:
	from examples.settings.user_settings import *
except:
	print("user_settings.py not found")


def run_this_protocol(callback_protocol):
	import loggingbootstrap

	logger = logging.getLogger("examples")

	# setup different loggers for example script and api
	loggingbootstrap.create_double_logger("pybpodapi", API_LOG_LEVEL, 'pybpodapi-examples.log', API_LOG_LEVEL)
	loggingbootstrap.create_double_logger("examples", EXAMPLE_SCRIPT_LOG_LEVEL, 'pybpodapi-examples.log',
	                                      EXAMPLE_SCRIPT_LOG_LEVEL)

	callback_protocol()
