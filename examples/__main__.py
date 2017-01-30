# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import loggingbootstrap
import logging

import examples.settings as settings
from examples.function_examples import add_trial_events
from examples.function_examples import manual_override
from examples.function_examples import serial_messages
from examples.function_examples import bpod_info
import pybpodapi

try:
	from examples.settings.user_settings import *
except:
	print("user_settings.py not found")

# setup different loggers for example script and api
loggingbootstrap.create_file_logger("pybpodapi", 'pybpodapi-examples.log', settings.API_LOG_LEVEL)
loggingbootstrap.create_double_logger("examples", settings.EXAMPLE_SCRIPT_LOG_LEVEL, 'pybpodapi-examples.log',
                                      settings.EXAMPLE_SCRIPT_LOG_LEVEL)


def start():
	config_menu()

def print_menu_info():
	print("Available examples:")
	print("1. Print Bpod info")
	print("2. Add trial events")
	print("3. Test manual override")
	print("4. Test serial messages")
	print("0. Close program")

def config_menu():
	print('\nRunning pybpod-api version: {0}'.format(pybpodapi.__version__))
	print('\nBpod supported version: {0}'.format(pybpodapi.BPOD_VERSION))
	print('Firmware supported version: {0}\n'.format(pybpodapi.BPOD_FIRMWARE_VERSION))
	selection = None
	while True:
		try:
			print_menu_info()
			selection = int(input('\nSelect option: '))

			if selection == 1:
				print("Printing bpod info")
				bpod_info.run()
			elif selection == 2:
				print("Running add trial events")
				add_trial_events.run()
			elif selection == 3:
				print("Running manual override test")
				manual_override.run()
			elif selection == 4:
				print("Running serial messages test")
				serial_messages.run()
			else:
				print("Program closed by user")
				sys.exit()

			print("\n\n")
		except Exception as err:
			print("Program closed by user")
			sys.exit()

if __name__ == '__main__': start()
