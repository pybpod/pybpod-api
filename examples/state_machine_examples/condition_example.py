# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Example adapted from Josh Sanders' original version on Sanworks Bpod repository
"""

import examples.settings as settings

from pybpodapi.model.bpod import Bpod
from pybpodapi.model.state_machine import StateMachine
from pybpodapi.hardware.events import EventName
from pybpodapi.hardware.output_channels import OutputChannel

def run():
	"""
	Run this protocol now
	"""

	my_bpod = Bpod().start(settings.SERIAL_PORT, settings.WORKSPACE_PATH, "condition_example")

	sma = StateMachine(my_bpod.hardware)

	sma.set_condition(condition_number=1, condition_channel='Port2', channel_value=1)

	sma.add_state(
		state_name='Port1Light',
		state_timer=1,
		state_change_conditions={EventName.Tup: 'Port2Light'},
		output_actions=[(OutputChannel.PWM1, 255)])

	sma.add_state(
		state_name='Port2Light',
		state_timer=1,
		state_change_conditions={EventName.Tup: 'Port3Light', EventName.Condition1: 'Port3Light'},
		output_actions=[(OutputChannel.PWM2, 255)])

	sma.add_state(
		state_name='Port3Light',
		state_timer=1,
		state_change_conditions={EventName.Tup: 'exit'},
		output_actions=[(OutputChannel.PWM3, 255)])

	my_bpod.send_state_machine(sma)

	my_bpod.run_state_machine(sma)

	print("Current trial info: {0}".format(my_bpod.session.current_trial()))

	my_bpod.stop()


if __name__ == '__main__':
	settings.run_this_protocol(run)
