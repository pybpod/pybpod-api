# !/usr/bin/python3
# -*- coding: utf-8 -*-

import loggingbootstrap
import logging

from bpodapi.model.bpod import Bpod
from bpodapi.model.state_machine import StateMachine

# setup different loggers but output to single file
loggingbootstrap.create_double_logger("bpodapi", logging.DEBUG, 'bpodapi.log',
                                      logging.DEBUG)


my_bpod = Bpod('/dev/tty.usbmodem1461')  # Create a new instance of a Bpod object on serial port COM13

sma = StateMachine(my_bpod)  # Create a new state machine (events + outputs tailored for myBpod)

sma.add_state('Name', 'myState',
              'Timer', 1,
              'StateChangeConditions', ('Tup', 'exit'),
              'OutputActions', ())

my_bpod.send_state_machine(sma)  # Send state machine description to Bpod device

raw_events = my_bpod.run_state_machine()  # Run state machine and return events

print(raw_events)  # Print events to console

my_bpod.disconnect()  # Disconnect Bpod
