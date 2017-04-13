# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Get hardware info from Bpod

"""

from pybpodapi.model.bpod import Bpod

import examples.settings as settings


def run():
	my_bpod = Bpod().start(settings.SERIAL_PORT, settings.WORKSPACE_PATH, "bpod_info")

	my_bpod.stop()

	print("Bpod version: ", my_bpod.hardware.bpod_version)
	print("Bpod firmware version: ", my_bpod.hardware.firmware_version)
	print("Bpod machine type version: ", my_bpod.hardware.machine_type)


if __name__ == '__main__':
	settings.run_this_protocol(run)
