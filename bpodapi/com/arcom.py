# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import struct
import sys
import serial
import numpy as np

logger = logging.getLogger(__name__)


class DataType(object):
	def __init__(self, name, size):
		self.name = name
		self.size = size


class ArduinoTypes(object):
	CHAR = DataType('char', 1)
	UINT8 = DataType('uint8', 1)
	UINT16 = DataType('uint16', 2)
	UINT32 = DataType('uint32', 4)
	FLOAT = DataType('float', 4)


class ArCOM(object):
	"""
	ArCOM is an interface to simplify data transactions between Arduino and Python.
	"""

	def open(self, serialPortName, baudRate):
		"""
		Open serial connection
		:param serialPortName:
		:param baudRate:
		:return:
		"""
		self.serial_object = serial.Serial(serialPortName, baudRate, timeout=1)

	def close(self):
		"""
		Close serial connection
		:return:
		"""
		self.serial_object.close()

	def bytes_available(self):
		"""

		:return:
		"""
		return self.serial_object.inWaiting()

	def write_char(self, value):
		self.serial_object.write(str.encode(value))

	def write_uint8(self, value):
		self.serial_object.write(bytes(value))

	def write_array(self, data):
		self.serial_object.write(np.array(data).tobytes())

	def read_char(self):
		message_bytes = self.serial_object.read(ArduinoTypes.CHAR.size)

		return message_bytes.decode("utf-8")

	def read_uint8(self):
		message_bytes = self.serial_object.read(ArduinoTypes.UINT8.size)
		logger.debug("Read %s bytes: %s", ArduinoTypes.UINT8.size, message_bytes)
		message = int.from_bytes(message_bytes, byteorder='little')
		return message

	def read_uint16(self):
		message_bytes = self.serial_object.read(ArduinoTypes.UINT16.size)
		logger.debug("Read %s bytes: %s", ArduinoTypes.UINT16.size, message_bytes)
		message = int.from_bytes(message_bytes, byteorder='little')
		return message

	def read_uint32(self):
		message_bytes = self.serial_object.read(ArduinoTypes.UINT32.size)
		logger.debug("Read %s bytes: %s", ArduinoTypes.UINT32.size, message_bytes)
		message = int.from_bytes(message_bytes, byteorder='little')
		return message

	def read_char_array(self, array_len=1):
		message_array = []
		for pos in range(0, array_len):
			message_bytes = self.read_char()
			message_array.append(message_bytes)

		return message_array

	def read_uint8_array(self, array_len=1):
		message_array = []
		for pos in range(0, array_len):
			message_bytes = self.read_uint8()
			message_array.append(message_bytes)

		return message_array

	def read_uint16_array(self, array_len=1):
		message_array = []
		for pos in range(0, array_len):
			message_bytes = self.read_uint16()
			message_array.append(message_bytes)

		return message_array

	def read_uint32_array(self, array_len=1):
		message_array = []
		for pos in range(0, array_len):
			message_bytes = self.read_uint32()
			message_array.append(message_bytes)

		return message_array


class ArCOMError(Exception):
	pass
