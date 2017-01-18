# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

import loggingbootstrap

from pybpodapi.model.bpod import Bpod
from pybpodapi.model.state_machine import StateMachine

# setup different loggers but output to single file
loggingbootstrap.create_double_logger("pybpodapi", logging.DEBUG, 'pybpodapi.log', logging.DEBUG)

my_bpod = Bpod('/dev/tty.usbmodem1461')  # Create a new instance of a Bpod object on serial port COM13

sma = StateMachine(my_bpod.hardware)

sma.add_state(
	state_name='myState',
	state_timer=1,
	state_change_conditions={'Tup': 'exit'},
	output_actions=[])

my_bpod.send_state_machine(sma)  # Send state machine description to Bpod device

raw_events = my_bpod.run_state_machine(sma)  # Run state machine and return events

print(raw_events)  # Print events to console

my_bpod.disconnect()  # Disconnect Bpod
