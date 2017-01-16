# !/usr/bin/python3
# -*- coding: utf-8 -*-

import loggingbootstrap
import logging
import random

from bpodapi.model.bpod import Bpod
from bpodapi.model.state_machine.state_machine import StateMachine

# setup different loggers but output to single file
loggingbootstrap.create_double_logger("bpodapi", logging.DEBUG, 'bpodapi.log', logging.DEBUG)
loggingbootstrap.create_double_logger("add_trial_events", logging.DEBUG, 'bpodapi.log', logging.DEBUG)

logger = logging.getLogger("add_trial_events")

my_bpod = Bpod('/dev/tty.usbmodem1461')  # Create a new instance of a Bpod object on serial port COM13

nTrials = 5
trialTypes = [1, 2]  # 1 (rewarded left) or 2 (rewarded right)

for i in range(nTrials):  # Main loop
	logger.info('Trial: %s', str(i))
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

	raw_events = my_bpod.run_state_machine(sma)  # Run state machine and return events

	print(raw_events)  # Print events to console

	my_bpod.add_trial_events(sma, raw_events)  # Add trial events to myBpod.data struct, formatted for human readability

	print('States: {0}'.format(my_bpod.session.trials[i].states_timestamps))
	print('Events: {0}'.format(my_bpod.session.trials[i].events_timestamps))

	my_bpod.disconnect()  # Disconnect Bpod
