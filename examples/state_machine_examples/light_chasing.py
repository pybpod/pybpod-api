# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Light Chasing example

Follow light on 3 pokes

Connect noseports to ports 1-3.

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

	my_bpod = Bpod().start(settings.SERIAL_PORT, settings.WORKSPACE_PATH, "light_chasing")

	sma = StateMachine(my_bpod.hardware)

	sma.add_state(
		state_name='Port1Active1',  # Add a state
		state_timer=0,
		state_change_conditions={EventName.Port1In: 'Port2Active1'},
		output_actions=[(OutputChannel.PWM1, 255)])

	sma.add_state(
		state_name='Port2Active1',
		state_timer=0,
		state_change_conditions={EventName.Port2In: 'Port3Active1'},
		output_actions=[(OutputChannel.PWM2, 255)])

	sma.add_state(
		state_name='Port3Active1',
		state_timer=0,
		state_change_conditions={EventName.Port3In: 'Port1Active2'},
		output_actions=[(OutputChannel.PWM3, 255)])

	sma.add_state(
		state_name='Port1Active2',
		state_timer=0,
		state_change_conditions={EventName.Port1In: 'Port2Active2'},
		output_actions=[(OutputChannel.PWM1, 255)])

	sma.add_state(
		state_name='Port2Active2',
		state_timer=0,
		state_change_conditions={EventName.Port2In: 'Port3Active2'},
		output_actions=[(OutputChannel.PWM2, 255)])

	sma.add_state(
		state_name='Port3Active2',
		state_timer=0,
		state_change_conditions={EventName.Port3In: 'exit'},
		output_actions=[(OutputChannel.PWM3, 255)])

	my_bpod.send_state_machine(sma)

	my_bpod.run_state_machine(sma)

	print("Current trial info: {0}".format(my_bpod.session.current_trial()))

	my_bpod.stop()


if __name__ == '__main__':
	settings.run_this_protocol(run)
