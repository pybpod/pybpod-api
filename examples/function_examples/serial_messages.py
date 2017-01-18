# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Example adapted from Josh Sanders' original version on Sanworks Bpod repository
"""

import time
import logging

from pybpodapi.model.bpod import Bpod
from pybpodapi.hardware.channels import ChannelType
from pybpodapi.hardware.channels import ChannelName

import settings

logger = logging.getLogger("pybodapi-examples")

myBpod = Bpod().start(settings.SERIAL_PORT) # Start Bpod

logger.info("Send byte 65 on UART port 1 - by default, this is ASCII 'A'")
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.SERIAL, 1, 65)
time.sleep(1) # Wait 1s

logger.info("Set byte 65 ('A') on UART port 1 to trigger a 3-byte message: 'BCD'")
myBpod.load_serial_message(1, 65, [66,67,68])
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.SERIAL, 1, 65) # Now, the same command has a different result
time.sleep(1) # Wait 1s

logger.info("Reset the serial message library. Bytes will now pass through again.")
myBpod.reset_serial_messages()
myBpod.manual_override(ChannelType.OUTPUT, ChannelName.SERIAL, 1, 65) # Back to 'A'

# Disconnect Bpod
myBpod.disconnect() # Sends a termination byte and closes the serial port. PulsePal stores current params to its EEPROM.
