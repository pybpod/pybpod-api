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


class ArCOM(object):
	"""
	ArCOM is an interface to simplify data transactions between Arduino and Python.
	"""

	def __init__(self, serialPortName, baudRate):
		self.serialObject = 0
		self.typeNames = ('uint8', 'int8', 'char', 'uint16', 'int16', 'uint32', 'int32')
		self.typeBytes = (1, 1, 1, 2, 2, 4, 4)
		self.typeSymbols = ('B', 'b', 'c', 'H', 'h', 'L', 'l')
		self.serialObject = serial.Serial(serialPortName, baudRate, timeout=1)

	def open(self, serialPortName, baudRate):
		"""
		Open serial connection
		:param serialPortName:
		:param baudRate:
		:return:
		"""
		self.serialObject = serial.Serial(serialPortName, baudRate, timeout=1)

	def close(self):
		"""
		Close serial connection
		:return:
		"""
		self.serialObject.close()

	def bytesAvailable(self):
		"""

		:return:
		"""
		return self.serialObject.inWaiting()

	def write_char(self, value):
		self.serialObject.write(str.encode(value))

	def write_uint8(self, value):
		self.serialObject.write(bytes(value))

	def write_array(self, data):
		self.serialObject.write(np.array(data).tobytes())

	def read_char(self):
		message_bytes = self.serialObject.read(ArduinoTypes.CHAR.size)

		return message_bytes.decode("utf-8")

	def read_uint8(self):
		message_bytes = self.serialObject.read(ArduinoTypes.UINT8.size)
		logger.debug("Read %s bytes: %s", ArduinoTypes.UINT8.size, message_bytes)
		message_uint8 = int.from_bytes(message_bytes, sys.byteorder)
		return message_uint8

	def read_uint16(self):
		message_bytes = self.serialObject.read(ArduinoTypes.UINT16.size)
		message_uint16 = int.from_bytes(message_bytes, sys.byteorder)
		return message_uint16

	def read_uint32(self):
		message_bytes = self.serialObject.read(ArduinoTypes.UINT32.size)
		message_uint32 = int.from_bytes(message_bytes, sys.byteorder)
		return message_uint32

	def read_char_array(self, array_size=1):

		message_array = []
		for pos in range(0, array_size):
			message_bytes = self.serialObject.read(ArduinoTypes.CHAR.size).decode("utf-8")
			message_array.append(message_bytes)

		return message_array

	def write(self, *arg):
		"""

		:param arg:
		:return:
		"""
		nTypes = int(len(arg) / 2);
		argPos = 0;
		messageBytes = '';
		for i in range(0, nTypes):

			data = arg[argPos]

			argPos += 1

			datatype = arg[argPos]

			if ((datatype in self.typeNames) is False):
				raise ArCOMError('Error: ' + datatype + ' is not a data type supported by ArCOM.')

			datatypePos = self.typeNames.index(datatype)

			argPos += 1

			isList = False

			if isinstance(data, (tuple, list, str)):
				nValues = len(data)
				isList = True
			elif isinstance(data, int):
				nValues = 1
			else:
				raise ArCOMError('Error: Each python datatype to write must be int, str, tuple or list.')

			dataTypeSymbol = '<' + self.typeSymbols[datatypePos] * nValues

			if isList:
				messageBytes += struct.pack(dataTypeSymbol, *data)
			else:
				messageBytes += struct.pack(dataTypeSymbol, data)

		self.serialObject.write(messageBytes)

	def read(self, datatype):
		"""
		 Read one value
		:param datatype:
		:return:
		"""
		if ((datatype in self.typeNames) is False):
			raise ArCOMError('Error: ' + datatype + ' is not a data type supported by ArCOM.')
		typeIndex = self.typeNames.index(datatype)
		dataTypeSymbol = self.typeSymbols[typeIndex]
		byteWidth = self.typeBytes[typeIndex]
		messageBytes = self.serialObject.read(byteWidth)
		nBytesRead = len(messageBytes)
		if nBytesRead < byteWidth:
			raise ArCOMError('Error: serial port timed out. ' + str(nBytesRead) + ' bytes read. Expected ' + str(
				byteWidth) + ' byte(s).')
		dataFormat = '<' + dataTypeSymbol
		if datatype == 'char':
			thisOutput = str(messageBytes)
		else:
			thisOutput = struct.unpack(dataFormat, messageBytes)
			thisOutput = int(thisOutput[0])
		return thisOutput

	def readArray(self, *arg):
		"""
		Read an array of values
		:param arg:
		:return:
		"""
		nTypes = len(arg) / 2;
		argPos = 0;
		outputs = [];
		for i in range(0, nTypes):
			nValues = arg[argPos]
			argPos += 1
			datatype = arg[argPos]
			if ((datatype in self.typeNames) is False):
				raise ArCOMError('Error: ' + datatype + ' is not a data type supported by ArCOM.')
			argPos += 1
			typeIndex = self.typeNames.index(datatype)
			dataTypeSymbol = self.typeSymbols[typeIndex]
			byteWidth = self.typeBytes[typeIndex]
			nBytes2Read = nValues * byteWidth;
			messageBytes = self.serialObject.read(nBytes2Read)
			nBytesRead = len(messageBytes)
			if nBytesRead < nBytes2Read:
				raise ArCOMError('Error: serial port timed out. ' + str(nBytesRead) + ' bytes read. Expected ' + str(
					nBytes2Read) + ' byte(s).')
			dataFormat = '<' + dataTypeSymbol * nValues
			if datatype == 'char':
				thisOutput = str(messageBytes)
			else:
				thisOutput = list(struct.unpack(dataFormat, messageBytes))
			outputs.append(thisOutput)
		if nTypes == 1:
			outputs = thisOutput
		return outputs


class ArCOMError(Exception):
	pass
