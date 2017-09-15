# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Light Chasing example

Follow light on 2 pokes

Connect noseports to ports 1-2.

"""
from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
from pybpodapi.bpod.hardware.events import EventName
from pybpodapi.bpod.hardware.output_channels import OutputChannel


my_bpod = Bpod()

sma = StateMachine(my_bpod)

sma.add_state(
	state_name='Port1Active1',  # Add a state
	state_timer=0,
	state_change_conditions={EventName.Port1In: 'Port2Active1'},
	output_actions=[(OutputChannel.PWM1, 255)])

sma.add_state(
	state_name='Port2Active1',
	state_timer=0,
	state_change_conditions={EventName.Port2In: 'Port1Active2'},
	output_actions=[(OutputChannel.PWM2, 255)])

sma.add_state(
	state_name='Port1Active2',
	state_timer=0,
	state_change_conditions={EventName.Port1In: 'Port2Active2'},
	output_actions=[(OutputChannel.PWM1, 255)])

sma.add_state(
	state_name='Port2Active2',
	state_timer=0,
	state_change_conditions={EventName.Port2In: 'exit'},
	output_actions=[(OutputChannel.PWM2, 255)])

my_bpod.send_state_machine(sma)

my_bpod.run_state_machine(sma)

print("Current trial info: {0}".format(my_bpod.session.current_trial))

my_bpod.stop()
