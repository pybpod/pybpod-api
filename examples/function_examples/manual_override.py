# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Manually set values on Bpod channels via serial instructions.

Example adapted from Josh Sanders' original version on Sanworks Bpod repository
"""

import time

from pybpodapi.model.bpod import Bpod
from pybpodapi.hardware.channels import ChannelType
from pybpodapi.hardware.channels import ChannelName

import examples.settings as settings


def run():
	myBpod = Bpod().start(settings.SERIAL_PORT)  # Start bpod

	wait_active_time_ms = 2

	### PORT 1 LED ###

	print("Set LED of port 1 to max intensity")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.PWM, channel_number=1, value=255)
	time.sleep(wait_active_time_ms)

	print("Set LED of port 1 to lower intensity")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.PWM, channel_number=1, value=8)
	time.sleep(wait_active_time_ms)

	print("Set LED of port 1 to zero intensity")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.PWM, channel_number=1, value=0)
	time.sleep(1)

	### PORT 2 LED ###

	print("Set LED of port 2 to max intensity")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.PWM, channel_number=2, value=255)
	time.sleep(wait_active_time_ms)

	print("Set LED of port 2 to lower intensity")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.PWM, channel_number=2, value=8)
	time.sleep(wait_active_time_ms)

	print("Set LED of port 2 to zero intensity")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.PWM, channel_number=2, value=0)
	time.sleep(1)  # Wait 1s

	### PORT 1 VALVE ###

	print("Set valve of port 1 to open")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.VALVE, 1, value=1)
	time.sleep(wait_active_time_ms)

	print("Set valve of port 1 to close")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.VALVE, 1, value=0)
	time.sleep(1)  # Wait 1s

	### PORT 3 VALVE ###

	print("Set valve of port 3 to open")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.VALVE, channel_number=3, value=1)
	time.sleep(wait_active_time_ms)  # Wait 250ms

	print("Set valve of port 3 to close")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.VALVE, channel_number=3, value=0)
	time.sleep(1)  # Wait 1s

	### PORT 2 BNC ###

	print("Set BNC output ch2 to high")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.BNC, channel_number=2, value=1)
	time.sleep(0.01)  # Wait 10ms

	print("Set BNC output ch2 to low")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.BNC, channel_number=2, value=0)
	time.sleep(1)  # Wait 1s

	### PORT 3 Wire ###

	print("Set Wire output ch3 to high")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.WIRE, channel_number=3, value=1)
	time.sleep(0.01)  # Wait 10ms

	print("Set Wire output ch3 to low")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.WIRE, channel_number=3, value=0)
	time.sleep(1)  # Wait 1s

	### PORT 2 Serial ###

	print("Send byte 65 on UART port 2")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.SERIAL, channel_number=2, value=65)
	time.sleep(0.01)  # Wait 10ms

	print("Send byte 66 on UART port 1")
	myBpod.manual_override(ChannelType.OUTPUT, ChannelName.SERIAL, channel_number=1, value=66)

	# Disconnect Bpod
	myBpod.disconnect()  # Sends a termination byte and closes the serial port. PulsePal stores current params to its EEPROM.


if __name__ == '__main__':
	settings.run_this_protocol(run)
