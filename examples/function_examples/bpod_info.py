# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Get hardware info from Bpod

"""

import logging

from pybpodapi.model.bpod import Bpod

import examples.settings as settings

logger = logging.getLogger("examples")

def run():
	my_bpod = Bpod().start(settings.SERIAL_PORT)

	my_bpod.disconnect()

	logger.info("Bpod version: %s", my_bpod.hardware.bpod_version)
	logger.info("Bpod firmware version: %s", my_bpod.hardware.firmware_version)
	logger.info("Bpod machine type version: %s", my_bpod.hardware.machine_type)

if __name__ == '__main__': run()