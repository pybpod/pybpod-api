# !/usr/bin/python3
# -*- coding: utf-8 -*-
import logging

PYBPOD_API_LOG_LEVEL = logging.DEBUG
PYBPOD_API_LOG_FILE = "pybpod-api.log"

PYBPOD_API_MODULES = [
    # 'pybpod_rotaryencoder_module'
]

PYBPOD_API_STREAM2STDOUT = False

PYBPOD_API_ACCEPT_STDIN = False

TARGET_BPOD_FIRMWARE_VERSION = "22"
EMULATOR_BPOD_MACHINE_TYPE = 3

PYBPOD_SERIAL_PORT = None

BPOD_BNC_PORTS_ENABLED = [True, True]
BPOD_WIRED_PORTS_ENABLED = [True, True]
BPOD_BEHAVIOR_PORTS_ENABLED = [True, True, True, True, True, True, True, True]
