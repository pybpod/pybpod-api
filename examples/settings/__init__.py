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
