# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class BpodProtocol(object):
	HANDSHAKE = '6'
	FIRMWARE_VERSION = 'F'
	HARDWARE_DESCRIPTION = 'H'
	ENABLE_PORTS = 'E'
	SYNC_CHANNEL_MODE = 'K'
	NEW_STATE_MATRIX = 'C'
	RUN_STATE_MACHINE = 'R'
	LOAD_SERIAL_MESSAGE = 'L'
	RESET_SERIAL_MESSAGES = '>'
	OVERRIDE_DIGITAL_HW_STATE = 'O'
	SEND_TO_HW_SERIAL = 'U'
	DISCONNECT = 'Z'

class BpodProtocolReceive(object):
	HANDSHAKE_OK = '5'