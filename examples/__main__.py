# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import loggingbootstrap

import examples.settings as settings
from examples.function_examples import bpod_info
from examples.function_examples import add_trial_events
from examples.function_examples import add_trial_events2
from examples.function_examples import manual_override
from examples.function_examples import serial_messages
from examples.state_machine_examples import condition_example
from examples.state_machine_examples import global_counter_example
from examples.state_machine_examples import global_timer_example
from examples.state_machine_examples import global_timer_example_digital
from examples.state_machine_examples import global_timer_start_and_end_events
from examples.state_machine_examples import light_chasing
from examples.state_machine_examples import one_state
from examples.state_machine_examples import uart_triggered_state_change
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
	print("1. Obtain Bpod info")
	print("2. One state")
	print("3. Light chasing")
	print("4. Add trial events")
	print("5. Add trial events 2")
	print("6. Manual override")
	print("7. Serial messages")
	print("8. Simple global timer")
	print("9. Digital global timer")
	print("10. Global timer with start and end events")
	print("11. Global counter")
	print("12. Setting a condition")
	print("13. UART triggered state")
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
				print("State machine with a single state")
				one_state.run()
			elif selection == 3:
				print("Running light chasing example")
				light_chasing.run()
			elif selection == 4:
				print("Running add trial events example")
				add_trial_events.run()
			elif selection == 5:
				print("Running add trial events example 2")
				add_trial_events2.run()
			elif selection == 6:
				print("Running a manual overriding example")
				manual_override.run()
			elif selection == 7:
				print("Running serial messages example")
				serial_messages.run()
			elif selection == 8:
				print("Running simple global timer example")
				global_timer_example.run()
			elif selection == 9:
				print("Running digital global timer example")
				global_timer_example_digital.run()
			elif selection == 10:
				print("Running global timer with start and end events example")
				global_timer_start_and_end_events.run()
			elif selection == 11:
				print("Running global counter example")
				global_counter_example.run()
			elif selection == 12:
				print("Running set condition example")
				condition_example.run()
			elif selection == 13:
				print("Running UART triggered state example")
				uart_triggered_state_change.run()
			else:
				print("Program closed by user")
				sys.exit()

			print("\n\n")
		except ValueError as err:
			print("Invalid chosen option")
		except Exception as err:
			print("Error while running example: ", str(err))
			sys.exit()


if __name__ == '__main__': start()
