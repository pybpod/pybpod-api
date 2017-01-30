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

import examples.settings as settings

logger = logging.getLogger("examples")


def run():
	myBpod = Bpod().start(settings.SERIAL_PORT)  # Start Bpod

	logger.info("Send byte 65 on UART port 1 - by default, this is ASCII 'A'")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.SERIAL, 1, 65)
	time.sleep(1)  # Wait 1s

	logger.info("Set byte 65 ('A') on UART port 1 to trigger a 3-byte message: 'BCD'")
	myBpod.load_serial_message(1, 65, [66, 67, 68])
	# Now, the same command has a different result
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.SERIAL, channel_number=1, value=65)
	time.sleep(1)  # Wait 1s

	logger.info("Reset the serial message library. Bytes will now pass through again.")
	myBpod.reset_serial_messages()
	# Back to 'A'
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.SERIAL, channel_number=1, value=65)

	# Disconnect Bpod
	myBpod.disconnect()  # Sends a termination byte and closes the serial port. PulsePal stores current params to its EEPROM.


if __name__ == '__main__':
	import loggingbootstrap

	# setup different loggers for example script and api
	loggingbootstrap.create_double_logger("pybpodapi", settings.API_LOG_LEVEL, 'pybpodapi-examples.log',
	                                      settings.API_LOG_LEVEL)
	loggingbootstrap.create_double_logger("examples", settings.EXAMPLE_SCRIPT_LOG_LEVEL, 'pybpodapi-examples.log',
	                                      settings.EXAMPLE_SCRIPT_LOG_LEVEL)

	run()
