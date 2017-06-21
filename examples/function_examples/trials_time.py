# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Testing timer intervals between consecutive trials

@authors: Rachid Azizi, Carlos Mão de Ferro, Ricardo Ribeiro
"""

import examples.settings as settings

from pybpodapi.model.bpod import Bpod
from pybpodapi.model.state_machine import StateMachine
from pybpodapi.hardware.events import EventName
from pybpodapi.hardware.output_channels import OutputChannel
from functools import reduce

import time


def run():
	my_bpod = Bpod().start(settings.SERIAL_PORT, settings.WORKSPACE_PATH, "trials_time")

	nTrials = 1000

	global_timer = time.time()
	TS = 0.1  # time in each state

	timestamps = []

	for i in range(nTrials):
		print('{0}'.format(i + 1))

		sma = StateMachine(my_bpod.hardware)

		sma.add_state(
			state_name='State1',
			state_timer=TS,
			state_change_conditions={EventName.Tup: 'State2'},
			output_actions=[(OutputChannel.PWM2, 255)])
		sma.add_state(
			state_name='State2',
			state_timer=TS,
			state_change_conditions={EventName.Tup: 'State3'},
			output_actions=[(OutputChannel.PWM2, 255)])
		sma.add_state(
			state_name='State3',
			state_timer=TS,
			state_change_conditions={EventName.Tup: 'State4'},
			output_actions=[(OutputChannel.Valve, 1)])
		sma.add_state(
			state_name='State4',
			state_timer=TS,
			state_change_conditions={EventName.Tup: 'State5'},
			output_actions=[(OutputChannel.PWM2, 255)])
		sma.add_state(
			state_name='State5',
			state_timer=TS,
			state_change_conditions={EventName.Tup: 'exit'},
			output_actions=[(OutputChannel.Valve, 1)])

		my_bpod.send_state_machine(sma)  # Send state machine description to Bpod device

		time_before_run = time.time()
		print("Time before run: {0}".format(time_before_run))

		my_bpod.run_state_machine(sma)  # Run state machine

		time_after_run = time.time()
		diff = time_after_run - time_before_run
		print("Time after run: {0}".format(time_after_run))
		print("Diff = {0}".format(diff))
		timestamps.append(diff)


	print("Trial lenght mean: {0}".format(reduce(lambda x, y: x + y, timestamps) / len(timestamps)))

	my_bpod.stop()


if __name__ == '__main__':
	settings.run_this_protocol(run)
