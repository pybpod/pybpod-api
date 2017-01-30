# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Demonstration of AddTrialEvents used in a simple visual 2AFC session.
AddTrialEvents formats each trial's data in a human-readable struct, and adds to myBpod.data (to save to disk later)
Connect noseports to ports 1-3.

Example adapted from Josh Sanders' original version on Sanworks Bpod repository
"""

import logging
import random

import examples.settings as settings

from pybpodapi.model.bpod import Bpod
from pybpodapi.model.state_machine import StateMachine

logger = logging.getLogger("examples")


def run():
	"""
	Run this protocol now
	"""

	my_bpod = Bpod().start(settings.SERIAL_PORT)  # Start bpod

	nTrials = 5
	trialTypes = [1, 2]  # 1 (rewarded left) or 2 (rewarded right)

	for i in range(nTrials):  # Main loop
		logger.info('Trial: %s', i + 1)
		thisTrialType = random.choice(trialTypes)  # Randomly choose trial type =
		if thisTrialType == 1:
			stimulus = 'PWM1'  # set stimulus channel for trial type 1
			leftAction = 'Reward'
			rightAction = 'Punish'
			rewardValve = 1
		elif thisTrialType == 2:
			stimulus = 'PWM3'  # set stimulus channel for trial type 1
			leftAction = 'Punish'
			rightAction = 'Reward'
			rewardValve = 3

		sma = StateMachine(my_bpod.hardware)

		sma.add_state(
			state_name='WaitForPort2Poke',
			state_timer=1,
			state_change_conditions={'Port2In': 'FlashStimulus'},
			output_actions=[('PWM2', 255)])
		sma.add_state(
			state_name='FlashStimulus',
			state_timer=0.1,
			state_change_conditions={'Tup': 'WaitForResponse'},
			output_actions=[(stimulus, 255)])
		sma.add_state(
			state_name='WaitForResponse',
			state_timer=1,
			state_change_conditions={'Port1In': leftAction, 'Port3In': rightAction},
			output_actions=[])
		sma.add_state(
			state_name='Reward',
			state_timer=0.1,
			state_change_conditions={'Tup': 'exit'},
			output_actions=[('Valve', rewardValve)])  # Reward correct choice
		sma.add_state(
			state_name='Punish',
			state_timer=3,
			state_change_conditions={'Tup': 'exit'},
			output_actions=[('LED', 1), ('LED', 2), ('LED', 3)])  # Signal incorrect choice

		my_bpod.send_state_machine(sma)  # Send state machine description to Bpod device

		logger.info("Waiting for poke. Reward: %s", 'left' if thisTrialType == 1 else 'right')

		raw_events = my_bpod.run_state_machine(sma)  # Run state machine and return events

		# print("Raw events: ", raw_events)  # Print events to console

		my_bpod.add_trial_events()  # Add trial events to myBpod.data struct, formatted for human readability

	# print('States: {0}'.format(my_bpod.session.trials[i].states_timestamps))
	# print('Events: {0}'.format(my_bpod.session.trials[i].events_timestamps))

	my_bpod.disconnect()  # Disconnect Bpod


if __name__ == '__main__':
	import loggingbootstrap

	# setup different loggers for example script and api
	loggingbootstrap.create_double_logger("pybpodapi", settings.API_LOG_LEVEL, 'pybpodapi-examples.log',
	                                      settings.API_LOG_LEVEL)
	loggingbootstrap.create_double_logger("examples", settings.EXAMPLE_SCRIPT_LOG_LEVEL, 'pybpodapi-examples.log',
	                                      settings.EXAMPLE_SCRIPT_LOG_LEVEL)

	run()
