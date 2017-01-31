# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Example adapted from Josh Sanders' original version on Sanworks Bpod repository
"""

import examples.settings as settings

from pybpodapi.model.bpod import Bpod
from pybpodapi.model.state_machine import StateMachine


def run():
	"""
	Run this protocol now
	"""

	my_bpod = Bpod().start(settings.SERIAL_PORT)

	sma = StateMachine(my_bpod.hardware)

	sma.set_global_counter(counter_number=1, target_event='Port1In', threshold=5)

	sma.add_state(
		state_name='InitialDelay',
		state_timer=2,
		state_change_conditions={'Tup': 'ResetGlobalCounter1'},
		output_actions=[('PWM2', 255)])

	sma.add_state(
		state_name='ResetGlobalCounter1',
		state_timer=0,
		state_change_conditions={'Tup': 'Port1Lit'},
		output_actions=[('GlobalCounterReset', 1)])

	sma.add_state(
		state_name='Port1Lit',  # Infinite loop (with next state). Only a global counter can save us.
		state_timer=.25,
		state_change_conditions={'Tup': 'Port3Lit', 'GlobalCounter1_End': 'exit'},
		output_actions=[('PWM1', 255)])

	sma.add_state(
		state_name='Port3Lit',
		state_timer=.25,
		state_change_conditions={'Tup': 'Port1Lit', 'GlobalCounter1_End': 'exit'},
		output_actions=[('PWM3', 255)])

	my_bpod.send_state_machine(sma)

	raw_events = my_bpod.run_state_machine(sma)

	print(raw_events)

	my_bpod.disconnect()


if __name__ == '__main__':
	settings.run_this_protocol(run)
