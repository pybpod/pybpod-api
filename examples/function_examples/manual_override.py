'''
----------------------------------------------------------------------------

This file is part of the Sanworks Bpod repository
Copyright (C) 2016 Sanworks LLC, Sound Beach, New York, USA

----------------------------------------------------------------------------

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3.

This program is distributed  WITHOUT ANY WARRANTY and without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import time
import loggingbootstrap
import logging

from bpodapi.model.bpod import Bpod
from bpodapi.hardware.channels import ChannelType
from bpodapi.hardware.channels import ChannelName

# setup different loggers but output to single file
loggingbootstrap.create_double_logger("bpodapi", logging.DEBUG, 'bpodapi.log', logging.DEBUG)
loggingbootstrap.create_double_logger("add_trial_events", logging.DEBUG, 'bpodapi.log', logging.DEBUG)

logger = logging.getLogger("add_trial_events")

myBpod = Bpod().start('/dev/tty.usbmodem1461') # Create a new instance of a Bpod object on serial port COM13

wait_active_time_ms = 2

print("Set LED of port 2 to max intensity")
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.PWM, 2, 255) # Set LED of port 2 to max intensity
time.sleep(wait_active_time_ms) # Wait 250ms

print("Set LED of port 2 to lower intensity")
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.PWM, 2, 8) # Set LED of port 2 to lower intensity
time.sleep(wait_active_time_ms) # Wait 250ms

print("Set LED of port 2 to zero intensity")
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.PWM, 2, 0) # Set LED of port 2 to zero intensity
time.sleep(1) # Wait 1s

print("Set valve of port 1 to open")
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.VALVE, 1, 1) # Set valve of port 1 to "open"
time.sleep(wait_active_time_ms) # Wait 250ms

print("Set valve of port 1 to close")
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.VALVE, 1, 0) # Set valve of port 1 to "close"
time.sleep(1) # Wait 1s

print("Set valve of port 3 to open")
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.VALVE, 3, 1) # Set valve of port 3 to "open"
time.sleep(wait_active_time_ms) # Wait 250ms

print("Set valve of port 3 to close")
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.VALVE, 3, 0) # Set valve of port 3 to "close"
time.sleep(1) # Wait 1s

print("Set BNC output ch2 to high")
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.BNC, 2, 1) # Set BNC output ch2 to "high"
time.sleep(0.01) # Wait 10ms

print("Set BNC output ch2 to low")
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.BNC, 2, 0) # Set BNC output ch2 to "low"
time.sleep(1) # Wait 1s

print("Set Wire output ch3 to high")
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.WIRE, 3, 1) # Set Wire output ch3 to "high"
time.sleep(0.01) # Wait 10ms

print("Set Wire output ch3 to low")
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.WIRE, 3, 0) # Set Wire output ch3 to "low"
time.sleep(1) # Wait 1s

print("Send byte 65 on UART port 2")
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.SERIAL, 2, 65) # Send byte 65 on UART port 2
time.sleep(0.01) # Wait 10ms

print("Send byte 66 on UART port 1")
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.SERIAL, 1, 66) # Send byte 66 on UART port 1

# Disconnect Bpod
myBpod.disconnect() # Sends a termination byte and closes the serial port. PulsePal stores current params to its EEPROM.
