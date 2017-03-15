# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Demonstration of AddTrialEvents used in a simple visual 2AFC session.
AddTrialEvents formats each trial's data in a human-readable struct, and adds to myBpod.data (to save to disk later)
Connect noseports to ports 1-3.

Example adapted from Josh Sanders' original version on Sanworks Bpod repository
"""

import random

import examples.settings as settings

from pybpodapi.model.bpod import Bpod
from pybpodapi.model.state_machine import StateMachine


def run():
	"""
	Run this protocol now
	"""

	my_bpod = Bpod().start(settings.SERIAL_PORT)  # Start bpod

	nTrials = 5
	graceTime = 5
	trialTypes = [1, 2]  # 1 (rewarded left) or 2 (rewarded right)

	for i in range(nTrials):  # Main loop
		print('Trial: ', i + 1)

		thisTrialType = random.choice(trialTypes)  # Randomly choose trial type
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

		sma.set_global_timer_legacy(timer_ID=1, timer_duration=graceTime)  # Set timeout

		sma.add_state(
			state_name='WaitForPort2Poke',
			state_timer=1,
			state_change_conditions={'Port2In': 'FlashStimulus'},
			output_actions=[('PWM2', 255)])

		sma.add_state(
			state_name='FlashStimulus',
			state_timer=0.1,
			state_change_conditions={'Tup': 'WaitForResponse'},
			output_actions=[(stimulus, 255, 'GlobalTimerTrig', 1)])

		sma.add_state(
			state_name='WaitForResponse',
			state_timer=1,
			state_change_conditions={'Port1In': leftAction, 'Port3In': rightAction, 'Port2In': 'Warning',
			                         'GlobalTimer1_End': 'MiniPunish'},
			output_actions=[])

		sma.add_state(
			state_name='Warning',
			state_timer=0.1,
			state_change_conditions={'Tup': 'WaitForResponse', 'GlobalTimer1_End': 'MiniPunish'},
			output_actions=[('LED', 1), ('LED', 2), ('LED', 3)])  # Reward correct choice

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

		sma.add_state(
			state_name='MiniPunish',
			state_timer=1,
			state_change_conditions={'Tup': 'exit'},
			output_actions=[('LED', 1), ('LED', 2), ('LED', 3)])  # Signal incorrect choice

		my_bpod.send_state_machine(sma)  # Send state machine description to Bpod device

		print("Waiting for poke. Reward: ", 'left' if thisTrialType == 1 else 'right')

		my_bpod.run_state_machine(sma)  # Run state machine and return events

		print("Raw events: ", sma.raw_data)

		print("Current trial: ", my_bpod.session.current_trial())

	my_bpod.disconnect()  # Disconnect Bpod


if __name__ == '__main__':
	settings.run_this_protocol(run)
