# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Example adapted from Josh Sanders' original version on Sanworks Bpod repository
"""

import logging

import examples.settings as settings

from pybpodapi.model.bpod import Bpod
from pybpodapi.model.state_machine import StateMachine

logger = logging.getLogger("examples")


def run():
	"""
	Run this protocol now
	"""

	my_bpod = Bpod().start(settings.SERIAL_PORT)

	sma = StateMachine(my_bpod.hardware)

	sma.set_condition(condition_number=1, condition_channel='Port2', channel_value=1)

	sma.add_state(
		state_name='Port1Light',
		state_timer=1,
		state_change_conditions={'Tup': 'Port2Light'},
		output_actions=[('PWM1', 255)])

	sma.add_state(
		state_name='Port2Light',
		state_timer=1,
		state_change_conditions={'Tup': 'Port3Light', 'Condition1': 'Port3Light'},
		output_actions=[('PWM2', 255)])

	sma.add_state(
		state_name='Port3Light',
		state_timer=1,
		state_change_conditions={'Tup': 'exit'},
		output_actions=[('PWM3', 255)])

	logger.info("Conditions matrix: %s", sma.conditions.matrix)

	my_bpod.send_state_machine(sma)  # Send state machine description to Bpod device

	raw_events = my_bpod.run_state_machine(sma)  # Run state machine and return events

	logger.info("Raw events: %s", raw_events)

	my_bpod.disconnect()  # Disconnect Bpod


if __name__ == '__main__':
	import loggingbootstrap

	# setup different loggers for example script and api
	loggingbootstrap.create_double_logger("pybpodapi", settings.API_LOG_LEVEL, 'pybpodapi-examples.log',
	                                      settings.API_LOG_LEVEL)
	loggingbootstrap.create_double_logger("examples", settings.EXAMPLE_SCRIPT_LOG_LEVEL, 'pybpodapi-examples.log',
	                                      settings.EXAMPLE_SCRIPT_LOG_LEVEL)

	run()
