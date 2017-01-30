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

	sma.add_state(
		state_name='myState',
		state_timer=1,
		state_change_conditions={'Tup': 'exit'},
		output_actions=[])

	my_bpod.send_state_machine(sma)

	raw_events = my_bpod.run_state_machine(sma)

	logger.info("Raw events: %s", raw_events)

	my_bpod.disconnect()


if __name__ == '__main__':
	import loggingbootstrap

	# setup different loggers for example script and api
	loggingbootstrap.create_double_logger("pybpodapi", settings.API_LOG_LEVEL, 'pybpodapi-examples.log',
	                                      settings.API_LOG_LEVEL)
	loggingbootstrap.create_double_logger("examples", settings.EXAMPLE_SCRIPT_LOG_LEVEL, 'pybpodapi-examples.log',
	                                      settings.EXAMPLE_SCRIPT_LOG_LEVEL)

	run()
