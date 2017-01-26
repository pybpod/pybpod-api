# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class SendMessageHeader(object):
	"""
	Define names for message headers sent to the Bpod device.

	The message header is the first byte (character) on a message sent.
	"""

	#: Request initialization handshake
	HANDSHAKE = '6'

	#: Request firmware build number
	FIRMWARE_VERSION = 'F'

	#: Request hardware configuration
	HARDWARE_DESCRIPTION = 'H'

	#: Request enable input ports
	ENABLE_PORTS = 'E'

	#: Set sync channel and sync mode
	SYNC_CHANNEL_MODE = 'K'

	#: Send new compressed state matrix
	NEW_STATE_MATRIX = 'C'

	#: Request to run state matrix now
	RUN_STATE_MACHINE = 'R'

	#: Load serial message
	LOAD_SERIAL_MESSAGE = 'L'

	#: Reset serial messages to equivalent byte codes (i.e. message# 4 = one byte, 0x4)
	RESET_SERIAL_MESSAGES = '>'

	#: Override digital hardware state
	OVERRIDE_DIGITAL_HW_STATE = 'O'

	#: Send byte to hardware serial channel 1-3
	SEND_TO_HW_SERIAL = 'U'

	#: Request end of connection now
	DISCONNECT = 'Z'

class ReceiveMessageHeader(object):
	"""
	Define names for message headers received from the Bpod device.

	The message header is the first byte (character) on a message received.
	"""

	#: Success code from HANDSHAKE command
	HANDSHAKE_OK = '5'

	#: Success code from ENABLE_PORTS command
	ENABLE_PORTS_OK = 1

	#: Success code from SYNC_CHANNEL_MODE command
	SYNC_CHANNEL_MODE_OK = 1

	#: Success code from RUN_STATE_MACHINE command
	STATE_MACHINE_INSTALLATION_STATUS = 1

	#: Success code from LOAD_SERIAL_MESSAGE command
	LOAD_SERIAL_MESSAGE_OK = 1

	#: Success code from RESET_SERIAL_MESSAGES command
	RESET_SERIAL_MESSAGES = 1
