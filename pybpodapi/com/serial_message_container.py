# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class SerialMessageContainer(object):
	"""
	Serial message container temporarily stores information about serial message to be sent to Bpod
	"""

	def __init__(self, serial_channel, message_ID, serial_message, n_messages=1):
		"""

		:param int serial_channel: UART port to trigger
		:param int message_ID: byte parameter that triggers UART port
		:param list(int) serial_message: 3-byte message to send to UART port
		:param n_messages: TODO
		"""

		if len(serial_message) > 3:
			raise SerialMessageContainerError('Error: Serial messages cannot be more than 3 bytes in length.')

		if message_ID > 255 or message_ID < 1:
			raise SerialMessageContainerError('Error: Bpod can only store 255 serial messages (indexed 1-255).')

		self.serial_channel = serial_channel - 1  # type: int
		self.message_ID = message_ID  # type: int
		self.serial_message = serial_message
		self.n_messages = n_messages

	def format_for_sending(self):
		"""
		Format message container elements to be sent to Bpod over serial connection

		:rtype: list(int)
		"""
		return [self.serial_channel, self.n_messages, self.message_ID, len(self.serial_message)] + self.serial_message


class SerialMessageContainerError(Exception):
	pass
