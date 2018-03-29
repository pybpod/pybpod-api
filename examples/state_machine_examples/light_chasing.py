# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Light Chasing example

Follow light on 3 pokes

Connect noseports to ports 1-3.

"""
from pybpodapi.protocol import Bpod, StateMachine


my_bpod = Bpod()

sma = StateMachine(my_bpod)

sma.add_state(
	state_name='Port1Active1',  # Add a state
	state_timer=0,
	state_change_conditions={Bpod.Events.Port1In: 'Port2Active1'},
	output_actions=[(Bpod.OutputChannels.PWM1, 255)])

sma.add_state(
	state_name='Port2Active1',
	state_timer=0,
	state_change_conditions={Bpod.Events.Port2In: 'Port3Active1'},
	output_actions=[(Bpod.OutputChannels.PWM2, 255)])

sma.add_state(
	state_name='Port3Active1',
	state_timer=0,
	state_change_conditions={Bpod.Events.Port3In: 'Port1Active2'},
	output_actions=[(Bpod.OutputChannels.PWM3, 255)])

sma.add_state(
	state_name='Port1Active2',
	state_timer=0,
	state_change_conditions={Bpod.Events.Port1In: 'Port2Active2'},
	output_actions=[(Bpod.OutputChannels.PWM1, 255)])

sma.add_state(
	state_name='Port2Active2',
	state_timer=0,
	state_change_conditions={Bpod.Events.Port2In: 'Port3Active2'},
	output_actions=[(Bpod.OutputChannels.PWM2, 255)])

sma.add_state(
	state_name='Port3Active2',
	state_timer=0,
	state_change_conditions={Bpod.Events.Port3In: 'exit'},
	output_actions=[(Bpod.OutputChannels.PWM3, 255)])

my_bpod.send_state_machine(sma)

my_bpod.run_state_machine(sma)

print("Current trial info: {0}".format(my_bpod.session.current_trial))

my_bpod.close()