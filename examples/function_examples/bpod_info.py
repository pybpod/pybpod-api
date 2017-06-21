# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Get hardware info from Bpod

"""

from pybpodapi.model.bpod import Bpod
from pysettings import conf

import examples.settings as settings


def run():
	my_bpod = Bpod().start(settings.SERIAL_PORT, settings.WORKSPACE_PATH, "bpod_info")

	my_bpod.stop()

	print("Target Bpod firmware version: ", conf.TARGET_BPOD_FIRMWARE_VERSION)
	print("Firmware version (read from device): ", my_bpod.hardware.firmware_version)
	print("Machine type version (read from device): ", my_bpod.hardware.machine_type)


if __name__ == '__main__':
	settings.run_this_protocol(run)
