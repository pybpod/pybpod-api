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
from examples.state_machine_examples import light_chasing_2_pokes
from examples.state_machine_examples import light_chasing
from examples.state_machine_examples import light_chasing_loop
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
	print("{idx}. Obtain Bpod info".format(idx=next_idx(reset=True)))
	print("{idx}. One state".format(idx=next_idx()))
	print("{idx}. Light chasing (2 pokes)".format(idx=next_idx()))
	print("{idx}. Light chasing (3 pokes)".format(idx=next_idx()))
	print("{idx}. Light chasing (3 pokes loop with timer)".format(idx=next_idx()))
	print("{idx}. Add trial events".format(idx=next_idx()))
	print("{idx}. Add trial events 2".format(idx=next_idx()))
	print("{idx}. Manual override".format(idx=next_idx()))
	print("{idx}. Serial messages".format(idx=next_idx()))
	print("{idx}. Simple global timer".format(idx=next_idx()))
	print("{idx}. Digital global timer".format(idx=next_idx()))
	print("{idx}. Global timer with start and end events".format(idx=next_idx()))
	print("{idx}. Global counter".format(idx=next_idx()))
	print("{idx}. Setting a condition".format(idx=next_idx()))
	print("{idx}. UART triggered state".format(idx=next_idx()))
	print("0. Close program")


def config_menu():
	print('\nRunning pybpod-api version: {0}'.format(pybpodapi.__version__))
	print('\nBpod firmware supported version: {0}'.format(pybpodapi.settings.TARGET_BPOD_FIRMWARE_VERSION))
	selection = None
	while True:
		try:
			print_menu_info()
			selection = int(input('\nSelect option: '))

			if selection == next_idx(reset=True):
				print("Printing bpod info")
				bpod_info.run()
			elif selection == next_idx():
				print("State machine with a single state")
				one_state.run()
			elif selection == next_idx():
				print("Running light chasing (2 pokes) example")
				light_chasing_2_pokes.run()
			elif selection == next_idx():
				print("Running light chasing (3 pokes) example")
				light_chasing.run()
			elif selection == next_idx():
				print("Running light chasing (3 pokes loop with timer) example")
				light_chasing_loop.run()
			elif selection == next_idx():
				print("Running add trial events example")
				add_trial_events.run()
			elif selection == next_idx():
				print("Running add trial events example 2")
				add_trial_events2.run()
			elif selection == next_idx():
				print("Running a manual overriding example")
				manual_override.run()
			elif selection == next_idx():
				print("Running serial messages example")
				serial_messages.run()
			elif selection == next_idx():
				print("Running simple global timer example")
				global_timer_example.run()
			elif selection == next_idx():
				print("Running digital global timer example")
				global_timer_example_digital.run()
			elif selection == next_idx():
				print("Running global timer with start and end events example")
				global_timer_start_and_end_events.run()
			elif selection == next_idx():
				print("Running global counter example")
				global_counter_example.run()
			elif selection == next_idx():
				print("Running set condition example")
				condition_example.run()
			elif selection == next_idx():
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


def next_idx(reset=False):
	global current_idx

	if reset:
		current_idx = 0

	current_idx += 1
	return current_idx


if __name__ == '__main__': start()
