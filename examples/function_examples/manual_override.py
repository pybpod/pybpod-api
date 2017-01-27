# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Manually set values on Bpod channels via serial instructions.

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
	myBpod = Bpod().start(settings.SERIAL_PORT) # Start bpod

	wait_active_time_ms = 2

	logger.info("Set LED of port 2 to max intensity")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.PWM, 2, 255) # Set LED of port 2 to max intensity
	time.sleep(wait_active_time_ms) # Wait 250ms

	logger.info("Set LED of port 2 to lower intensity")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.PWM, 2, 8) # Set LED of port 2 to lower intensity
	time.sleep(wait_active_time_ms) # Wait 250ms

	logger.info("Set LED of port 2 to zero intensity")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.PWM, 2, 0) # Set LED of port 2 to zero intensity
	time.sleep(1) # Wait 1s

	logger.info("Set valve of port 1 to open")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.VALVE, 1, 1) # Set valve of port 1 to "open"
	time.sleep(wait_active_time_ms) # Wait 250ms

	logger.info("Set valve of port 1 to close")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.VALVE, 1, 0) # Set valve of port 1 to "close"
	time.sleep(1) # Wait 1s

	logger.info("Set valve of port 3 to open")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.VALVE, 3, 1) # Set valve of port 3 to "open"
	time.sleep(wait_active_time_ms) # Wait 250ms

	logger.info("Set valve of port 3 to close")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.VALVE, 3, 0) # Set valve of port 3 to "close"
	time.sleep(1) # Wait 1s

	logger.info("Set BNC output ch2 to high")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.BNC, 2, 1) # Set BNC output ch2 to "high"
	time.sleep(0.01) # Wait 10ms

	logger.info("Set BNC output ch2 to low")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.BNC, 2, 0) # Set BNC output ch2 to "low"
	time.sleep(1) # Wait 1s

	logger.info("Set Wire output ch3 to high")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.WIRE, 3, 1) # Set Wire output ch3 to "high"
	time.sleep(0.01) # Wait 10ms

	logger.info("Set Wire output ch3 to low")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.WIRE, 3, 0) # Set Wire output ch3 to "low"
	time.sleep(1) # Wait 1s

	logger.info("Send byte 65 on UART port 2")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.SERIAL, 2, 65) # Send byte 65 on UART port 2
	time.sleep(0.01) # Wait 10ms

	logger.info("Send byte 66 on UART port 1")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.SERIAL, 1, 66) # Send byte 66 on UART port 1

	# Disconnect Bpod
	myBpod.disconnect() # Sends a termination byte and closes the serial port. PulsePal stores current params to its EEPROM.


if __name__ == '__main__': run()