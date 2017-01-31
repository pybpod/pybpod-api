# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Example adapted from Josh Sanders' original version on Sanworks Bpod repository
"""

import time

from pybpodapi.model.bpod import Bpod
from pybpodapi.hardware.channels import ChannelType
from pybpodapi.hardware.channels import ChannelName

import examples.settings as settings


def run():
	myBpod = Bpod().start(settings.SERIAL_PORT)  # Start Bpod

	print("Send byte 65 on UART port 1 - by default, this is ASCII 'A'")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.SERIAL, 1, 65)
	time.sleep(1)  # Wait 1s

	print("Set byte 65 ('A') on UART port 1 to trigger a 3-byte message: 'BCD'")
	myBpod.load_serial_message(1, 65, [66, 67, 68])
	# Now, the same command has a different result
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.SERIAL, channel_number=1, value=65)
	time.sleep(1)  # Wait 1s

	print("Reset the serial message library. Bytes will now pass through again.")
	myBpod.reset_serial_messages()
	# Back to 'A'
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.SERIAL, channel_number=1, value=65)

	# Disconnect Bpod
	myBpod.disconnect()  # Sends a termination byte and closes the serial port. PulsePal stores current params to its EEPROM.


if __name__ == '__main__':
	settings.run_this_protocol(run)
