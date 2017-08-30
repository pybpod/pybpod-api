# !/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime, time, logging


PYBPOD_API_LOG_LEVEL = None
PYBPOD_API_LOG_FILE  = 'pybpod-api.log'

# SUPPORTED BPOD FIRMWARE VERSION
#TARGET_BPOD_FIRMWARE_VERSION = "9" # 0.7.5
#TARGET_BPOD_FIRMWARE_VERSION = "13" # 0.7.9
TARGET_BPOD_FIRMWARE_VERSION  = "15" # 0.8

PYBPOD_API_PUBLISH_DATA_FUNC = lambda x:x

SERIAL_PORT 	= None
WORKSPACE_PATH 	= 'BPOD-WORKSPACE'
PROTOCOL_NAME 	= datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
BAUDRATE 		= 1312500
SYNC_CHANNEL 	= 255
SYNC_MODE 		= 1


#SERIAL_PORT = '/dev/ttyACM0'