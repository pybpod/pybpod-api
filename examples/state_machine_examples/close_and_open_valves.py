# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
A protocol to calibrate the water system. In addition, to contro the lights.
"""

from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
from pybpodapi.bpod.hardware.events import EventName
from pybpodapi.bpod.hardware.output_channels import OutputChannel
import timeit

my_bpod = Bpod()


# ----> Start the task
for i in range(2):  # Main loop
    print('Trial: ', i + 1)

    sma = StateMachine(my_bpod)

    sma.add_state(
        state_name='GetWater_P1',
        state_timer=1,
        state_change_conditions={EventName.Tup: 'GetWater_P2'},
        output_actions = [('Valve',1), (OutputChannel.PWM1, 255)])
    sma.add_state(
	state_name='GetWater_P2',
	state_timer=1,
	state_change_conditions={EventName.Tup: 'GetWater_P3'},
	output_actions = [('Valve',2),(OutputChannel.PWM2, 255) ])
    sma.add_state(
	state_name='GetWater_P3',
	state_timer=1,
	state_change_conditions={EventName.Tup: 'End'},
	output_actions = [('Valve',3), (OutputChannel.PWM3, 255)])
    sma.add_state(
        state_name = 'End',
        state_timer = 1,
        state_change_conditions={EventName.Tup: 'exit'},
        output_actions=[(OutputChannel.PWM1, 255), (OutputChannel.PWM2, 255), (OutputChannel.PWM3, 255)])

    my_bpod.send_state_machine(sma)  # Send state machine description to Bpod device
    my_bpod.run_state_machine(sma)  # Run state machine

my_bpod.stop()

