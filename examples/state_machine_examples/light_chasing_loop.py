# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Light Chasing Loop example

Follow light on 3 pokes and repeat states until a timeout occurs.

Connect noseports to ports 1-3.

"""

import examples.settings as settings

from pybpodapi.model.bpod import Bpod
from pybpodapi.model.state_machine import StateMachine


def run():
	"""
	Run this protocol now
	"""

	my_bpod = Bpod().start(settings.SERIAL_PORT, settings.WORKSPACE_PATH, "light_chasing_loop")

	sma = StateMachine(my_bpod.hardware)

	# Set global timer 1 for 3 seconds
	sma.set_global_timer_legacy(timer_ID=1, timer_duration=10)

	sma.add_state(
		state_name='TimerTrig',  # Trigger global timer
		state_timer=0,
		state_change_conditions={'Tup': 'Port1Active1'},
		output_actions=[('GlobalTimerTrig', 1)])

	# Infinite loop (with next state). Only a global timer can save us.
	sma.add_state(
		state_name='Port1Active1',
		state_timer=0,
		state_change_conditions={'Port1In': 'Port2Active1', 'GlobalTimer1_End': 'exit'},
		output_actions=[('PWM1', 255)])

	sma.add_state(
		state_name='Port2Active1',
		state_timer=0,
		state_change_conditions={'Port2In': 'Port3Active1', 'GlobalTimer1_End': 'exit'},
		output_actions=[('PWM2', 255)])

	sma.add_state(
		state_name='Port3Active1',
		state_timer=0,
		state_change_conditions={'Port3In': 'Port1Active1', 'GlobalTimer1_End': 'exit'},
		output_actions=[('PWM3', 255)])

	my_bpod.send_state_machine(sma)

	my_bpod.run_state_machine(sma)

	print(sma.raw_data)

	my_bpod.stop()


if __name__ == '__main__':
	settings.run_this_protocol(run)
