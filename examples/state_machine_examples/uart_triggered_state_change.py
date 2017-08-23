# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Example adapted from Josh Sanders' original version on Sanworks Bpod repository
"""
from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
from pybpodapi.bpod.hardware.events import EventName
from pybpodapi.bpod.hardware.output_channels import OutputChannel

"""
Run this protocol now
"""

my_bpod = Bpod()

sma = StateMachine(my_bpod)

sma.add_state(
	state_name='Port1Light',
	state_timer=0,
	state_change_conditions={EventName.Serial2_3: 'Port2Light'},  # Go to Port2Light when byte 0x3 arrives on UART port 2
	output_actions=[(OutputChannel.PWM1, 255)])

sma.add_state(
	state_name='Port2Light',
	state_timer=0,
	state_change_conditions={EventName.Tup: 'exit'},
	output_actions=[(OutputChannel.PWM2, 255)])

my_bpod.send_state_machine(sma)

my_bpod.run_state_machine(sma)

print("Current trial info: ", my_bpod.session.current_trial())

my_bpod.stop()