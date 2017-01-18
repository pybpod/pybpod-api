# -*- coding: utf-8 -*-

# THIS IS THE SETTINGS FILE FOR EXAMPLES
#
# DO NOT CHANGE THIS FILE!!!
#
# PLEASE REFER TO THE user_settings.py.template

import logging
import loggingbootstrap

API_LOG_LEVEL = logging.INFO
EXAMPLE_SCRIPT_LOG_LEVEL = logging.INFO
SERIAL_PORT = None

try:
	from user_settings import *
except:
	print("user_settings.py not found")

# setup different loggers for example script and api
loggingbootstrap.create_double_logger("pybpodapi", API_LOG_LEVEL, 'pybpodapi-examples.log', API_LOG_LEVEL)
loggingbootstrap.create_double_logger("pybodapi-examples", EXAMPLE_SCRIPT_LOG_LEVEL, 'pybpodapi-examples.log', EXAMPLE_SCRIPT_LOG_LEVEL)

