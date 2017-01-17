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

myBpod = Bpod('/dev/tty.usbmodem1461') # Create a new instance of a Bpod object on serial port COM13

print("Send byte 65 on UART port 1 - by default, this is ASCII 'A'")
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.SERIAL, 1, 65)
time.sleep(1) # Wait 1s

print("Set byte 65 ('A') on UART port 1 to trigger a 3-byte message: 'BCD'")
myBpod.load_serial_message(1, 65, [66,67,68])
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.SERIAL, 1, 65) # Now, the same command has a different result
time.sleep(1) # Wait 1s

print("Reset the serial message library. Bytes will now pass through again.")
myBpod.reset_serial_messages()
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.SERIAL, 1, 65) # Back to 'A'

# Disconnect Bpod
myBpod.disconnect() # Sends a termination byte and closes the serial port. PulsePal stores current params to its EEPROM.
