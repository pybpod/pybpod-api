# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Light Chasing Loop example

Follow light on 3 pokes and repeat states until a timeout occurs.

Connect noseports to ports 1-3.

"""
from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
from pybpodapi.bpod.hardware.events import EventName
from pybpodapi.bpod.hardware.output_channels import OutputChannel

my_bpod = Bpod()

sma = StateMachine(my_bpod)

# Set global timer 1 for 3 seconds
sma.set_global_timer_legacy(timer_id=1, timer_duration=10)

sma.add_state(
	state_name='TimerTrig',  # Trigger global timer
	state_timer=0,
	state_change_conditions={EventName.Tup: 'Port1Active1'},
	output_actions=[(OutputChannel.GlobalTimerTrig, 1)])

# Infinite loop (with next state). Only a global timer can save us.
sma.add_state(
	state_name='Port1Active1',
	state_timer=0,
	state_change_conditions={EventName.Port1In: 'Port2Active1', EventName.GlobalTimer1_End: 'exit'},
	output_actions=[(OutputChannel.PWM1, 255)])

sma.add_state(
	state_name='Port2Active1',
	state_timer=0,
	state_change_conditions={EventName.Port2In: 'Port3Active1', EventName.GlobalTimer1_End: 'exit'},
	output_actions=[(OutputChannel.PWM2, 255)])

sma.add_state(
	state_name='Port3Active1',
	state_timer=0,
	state_change_conditions={EventName.Port3In: 'Port1Active1', EventName.GlobalTimer1_End: 'exit'},
	output_actions=[(OutputChannel.PWM3, 255)])

my_bpod.send_state_machine(sma)

my_bpod.run_state_machine(sma)

print("Current trial info: {0}".format(my_bpod.session.current_trial()))

my_bpod.stop()