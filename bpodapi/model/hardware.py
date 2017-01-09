# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import math

logger = logging.getLogger(__name__)


class Hardware(object):
	"""
	Hardware description
	"""

	DEFAULT_FREQUENCY_DIVIDER = 1000000

	def set_up(self, hw_info_container):
		"""

		:param hw_info_container:
		:type hw_info_container: bpodapi.com.serial_containers.HardwareInfoContainer
		:return:
		"""
		self.max_states = hw_info_container.max_states
		self.cycle_period = hw_info_container.cycle_period
		self.n_events_per_serial_channel = hw_info_container.n_events_per_serial_channel
		self.n_global_timers = hw_info_container.n_global_timers
		self.n_global_counters = hw_info_container.n_global_counters
		self.n_conditions = hw_info_container.n_conditions
		self.inputs = hw_info_container.inputs
		self.outputs = hw_info_container.outputs + ['G', 'G', 'G']  # nOutputChannels

		self.n_uart_channels = len([idx for idx in self.inputs if idx == 'U'])

		self._configure_inputs()

		logger.debug(str(self))

	def _configure_inputs(self):
		"""
		TODO: improve this method
		:return:
		"""

		self.inputs_enabled = [0] * len(self.inputs)

		PortsFound = 0
		for i in range(len(self.inputs)):
			if self.inputs[i] == 'B':
				self.inputs_enabled[i] = 1
			elif self.inputs[i] == 'W':
				self.inputs_enabled[i] = 1
			if PortsFound == 0 and self.inputs[i] == 'P':  # Enable ports 1-3 by default
				PortsFound = 1
				self.inputs_enabled[i] = 1
				self.inputs_enabled[i + 1] = 1
				self.inputs_enabled[i + 2] = 1

	@property
	def cycle_period(self):
		return self._cycle_period

	@cycle_period.setter
	def cycle_period(self, value):
		self._cycle_period = value
		self.cycle_frequency = self.DEFAULT_FREQUENCY_DIVIDER / value

	@property
	def cycle_frequency(self):
		return self._cycle_frequency

	@cycle_frequency.setter
	def cycle_frequency(self, value):
		self._cycle_frequency = value

	@property
	def n_events_per_serial_channel(self):
		return self._n_events_per_serial_channel

	@n_events_per_serial_channel.setter
	def n_events_per_serial_channel(self, value):
		self._n_events_per_serial_channel = value

	def __str__(self):
		return "Hardware Configuration\n" \
		       "Max states: {max_states}\n" \
		       "Cycle period: {cycle_period}\n" \
		       "Cycle frequency: {cycle_frequency}\n" \
		       "Number of events per serial channel: {n_events_per_serial_channel}\n" \
		       "Number of global timers: {n_global_timers}\n" \
		       "Number of global counters: {n_global_counters}\n" \
		       "Number of conditions: {n_conditions}\n" \
		       "Inputs ({n_inputs}): {inputs}\n" \
		       "Outputs ({n_outputs}): {outputs}\n" \
		       "Enabled inputs ({n_inputs_enabled}): {inputs_enabled}\n" \
		       "".format(max_states=self.max_states,
		                 cycle_period=self.cycle_period,
		                 cycle_frequency=self.cycle_frequency,
		                 n_events_per_serial_channel=self.n_events_per_serial_channel,
		                 n_global_timers=self.n_global_timers,
		                 n_global_counters=self.n_global_counters,
		                 n_conditions=self.n_conditions,
		                 inputs=self.inputs,
		                 n_inputs=len(self.inputs),
		                 outputs=self.outputs,
		                 n_outputs=len(self.outputs),
		                 inputs_enabled=self.inputs_enabled,
		                 n_inputs_enabled=len([idx for idx in self.inputs_enabled if idx == 1]))
