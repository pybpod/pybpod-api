# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class ChannelType(object):
	INPUT = 1
	OUTPUT = 2


class ChannelName(object):
	PWM = 'PWM'
	VALVE = 'Valve'
	BNC = 'BNC'
	WIRE = 'Wire'
	SERIAL = 'Serial'


class EventsPositions(object):
	"""

	"""
	def __init__(self):
		self.Event_USB = 0  # type: int
		self.Event_Port = 0  # type: int
		self.Event_BNC = 0  # type: int
		self.EventWire = 0  # type: int
		self.globalTimerStart = 0  # type: int
		self.globalTimerEnd = 0  # type: int
		self.globalCounter = 0  # type: int
		self.condition = 0  # type: int
		self.jump = 0  # type: int
		self.Tup = 0  # type: int
		self.output_USB = 0  # type: int
		self.output_SPI = 0  # type: int
		self.output_BNC = 0  # type: int
		self.output_Wire = 0  # type: int
		self.output_PWM = 0  # type: int


class Channels(object):
	"""
	Bpod main class
	"""

	def __init__(self):
		self.event_names = ()
		self.input_channel_names = ()
		self.output_channel_names = ()
		self.events_positions = EventsPositions()

	def set_up_input_channels(self, hardware):
		"""
		Generate event and input channel names
		"""
		Pos = 0;
		nUSB = 0;
		nUART = 0;
		nBNCs = 0;
		nWires = 0;
		nPorts = 0;
		for i in range(len(hardware.inputs)):
			if hardware.inputs[i] == 'U':
				nUART += 1
				self.input_channel_names += ('Serial' + str(nUART),)
				for j in range(hardware.n_events_per_serial_channel):
					self.event_names += ('Serial' + str(nUART) + '_' + str(j + 1),)
					Pos += 1
			elif hardware.inputs[i] == 'X':
				if nUSB == 0:
					self.events_positions.Event_USB = Pos
				nUSB += 1
				self.input_channel_names += ('USB' + str(nUSB),);
				for j in range(hardware.n_events_per_serial_channel):
					self.event_names += ('SoftCode' + str(j + 1),)
					Pos += 1
			elif hardware.inputs[i] == 'P':
				if nPorts == 0:
					self.events_positions.Event_Port = Pos
				nPorts += 1;
				self.input_channel_names += ('Port' + str(nPorts),)
				self.event_names += (self.input_channel_names[-1] + 'In',)
				Pos += 1
				self.event_names += (self.input_channel_names[-1] + 'Out',)
				Pos += 1
			elif hardware.inputs[i] == 'B':
				if nBNCs == 0:
					self.events_positions.Event_BNC = Pos
				nBNCs += 1;
				self.input_channel_names += ('BNC' + str(nBNCs),)
				self.event_names += (self.input_channel_names[-1] + 'In',)
				Pos += 1
				self.event_names += (self.input_channel_names[-1] + 'Out',)
				Pos += 1
			elif hardware.inputs[i] == 'W':
				if nWires == 0:
					self.events_positions.Event_Wire = Pos
				nWires += 1;
				self.input_channel_names += ('Wire' + str(nWires),)
				self.event_names += (self.input_channel_names[-1] + 'In',)
				Pos += 1
				self.event_names += (self.input_channel_names[-1] + 'Out',)
				Pos += 1

		self.events_positions.globalTimerStart = Pos;
		for i in range(hardware.n_global_timers):
			self.event_names += ('GlobalTimer' + str(i + 1) + '_Start',)
			Pos += 1

		self.events_positions.globalTimerEnd = Pos;
		for i in range(hardware.n_global_timers):
			self.event_names += ('GlobalTimer' + str(i + 1) + '_End',)
			Pos += 1

		self.events_positions.globalCounter = Pos;
		for i in range(hardware.n_global_counters):
			self.event_names += ('GlobalCounter' + str(i + 1) + '_End',)
			Pos += 1

		self.events_positions.condition = Pos;
		for i in range(hardware.n_conditions):
			self.event_names += ('Condition' + str(i + 1),)
			Pos += 1

		self.events_positions.jump = Pos;
		for i in range(hardware.n_uart_channels):
			self.event_names += ('Serial' + str(i + 1) + 'Jump',)
			Pos += 1
		self.event_names += ('SoftJump',)
		Pos += 1

		self.event_names += ('Tup',)
		self.events_positions.Tup = Pos;
		Pos += 1

	def set_up_output_channels(self, hw_outputs):
		"""
		Generate output channel names
		"""
		Pos = 0;
		nUSB = 0;
		nUART = 0;
		nSPI = 0;
		nBNCs = 0;
		nWires = 0;
		nPorts = 0;
		for i in range(len(hw_outputs)):
			if hw_outputs[i] == 'U':
				nUART += 1
				self.output_channel_names += ('Serial' + str(nUART),)
				Pos += 1
			if hw_outputs[i] == 'X':
				if nUSB == 0:
					self.events_positions.output_USB = Pos;
				nUSB += 1
				self.output_channel_names += ('SoftCode',)
				Pos += 1
			if hw_outputs[i] == 'S':
				if nSPI == 0:
					self.events_positions.output_SPI = Pos;
				nSPI += 1
				self.output_channel_names += (
					'ValveState',)  # Assume an SPI shift register mapping bits of a byte to 8 valves
				Pos += 1
			if hw_outputs[i] == 'B':
				if nBNCs == 0:
					self.events_positions.output_BNC = Pos;
				nBNCs += 1
				self.output_channel_names += (
					'BNC' + str(nBNCs),)  # Assume an SPI shift register mapping bits of a byte to 8 valves
				Pos += 1
			if hw_outputs[i] == 'W':
				if nWires == 0:
					self.events_positions.output_Wire = Pos;
				nWires += 1
				self.output_channel_names += (
					'Wire' + str(nWires),)  # Assume an SPI shift register mapping bits of a byte to 8 valves
				Pos += 1
			if hw_outputs[i] == 'P':
				if nPorts == 0:
					self.events_positions.output_PWM = Pos;
				nPorts += 1
				self.output_channel_names += (
					'PWM' + str(nPorts),)  # Assume an SPI shift register mapping bits of a byte to 8 valves
				Pos += 1
		self.output_channel_names += ('GlobalTimerTrig',)
		Pos += 1
		self.output_channel_names += ('GlobalTimerCancel',)
		Pos += 1
		self.output_channel_names += ('GlobalCounterReset',)
		Pos += 1

	def __str__(self):
		return "SMA Channels\n" \
		       "Event names: {event_names}\n" \
		       "Input channel names: {input_channel_names}\n" \
		       "Output channel names: {output_channel_names}\n" \
		       "".format(event_names=self.event_names,
		                 input_channel_names=self.input_channel_names,
		                 output_channel_names=self.output_channel_names)
