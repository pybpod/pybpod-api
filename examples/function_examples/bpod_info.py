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


if __name__ == '__main__':
	import loggingbootstrap

	# setup different loggers for example script and api
	loggingbootstrap.create_double_logger("pybpodapi", settings.API_LOG_LEVEL, 'pybpodapi-examples.log',
	                                      settings.API_LOG_LEVEL)
	loggingbootstrap.create_double_logger("examples", settings.EXAMPLE_SCRIPT_LOG_LEVEL, 'pybpodapi-examples.log',
	                                      settings.EXAMPLE_SCRIPT_LOG_LEVEL)

	run()
