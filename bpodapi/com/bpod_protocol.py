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
	RUN_STATE_MACHINE = 'R'
