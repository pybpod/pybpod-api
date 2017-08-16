# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from pysettings import conf as bpod_settings

from pybpodapi.hardware.channels import Channels

logger = logging.getLogger(__name__)


class Hardware(object):
	"""
	Represents an hardware description based on information received from the current connected Bpod deviced.
	"""

	DEFAULT_FREQUENCY_DIVIDER = 1000000

	##################################################
	#################### METHODS #####################
	##################################################

	def setup(self, modules):
		"""
		Set up hardware based on hardware description obtained from Bpod device

		:param HardwareInfoContainer hw_info_container: hardware parameters received from Bpod
		"""

		self.outputs = hardware.outputs + ['G', 'G', 'G']

		self.n_uart_channels = len([idx for idx in self.inputs if idx == 'U'])

		# configure inputs enabled
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

		# set up channels
		self.channels = Channels()  # type: Channels
		self.channels.setup_input_channels(self, modules)
		self.channels.setup_output_channels(self.outputs)

		logger.debug(self.channels)

		logger.debug(str(self))





	def __str__(self):
		return "Hardware Configuration\n" \
			   "Max states: {max_states}\n" \
			   "Cycle period: {cycle_period}\n" \
			   "Cycle frequency: {cycle_frequency}\n" \
			   "Number of events per serial channel: {max_serial_events}\n" \
			   "Number of global timers: {n_global_timers}\n" \
			   "Number of global counters: {n_global_counters}\n" \
			   "Number of conditions: {n_conditions}\n" \
			   "Inputs ({n_inputs}): {inputs}\n" \
			   "Outputs ({n_outputs}): {outputs}\n" \
			   "Enabled inputs ({n_inputs_enabled}): {inputs_enabled}\n" \
			   "".format(max_states=self.max_states,
						 cycle_period=self.cycle_period,
						 cycle_frequency=self.cycle_frequency,
						 max_serial_events=self.max_serial_events,
						 n_global_timers=self.n_global_timers,
						 n_global_counters=self.n_global_counters,
						 n_conditions=self.n_conditions,
						 inputs=self.inputs,
						 n_inputs=len(self.inputs),
						 outputs=self.outputs,
						 n_outputs=len(self.outputs),
						 inputs_enabled=self.inputs_enabled,
						 n_inputs_enabled=len([idx for idx in self.inputs_enabled if idx == 1]))

	##################################################
	#################### PROPERTIES ##################
	##################################################

	@property
	def firmware_version(self): 		return self._firmware_version  # type: int
	@firmware_version.setter
	def firmware_version(self, value):  self._firmware_version = value  # type: int

	@property
	def machine_type(self): 			return self._machine_type  # type: int
	@machine_type.setter
	def machine_type(self, value): 		self._machine_type = value  # type: int

	@property
	def cycle_period(self): 			return self._cycle_period
	@cycle_period.setter
	def cycle_period(self, value):
		self._cycle_period   = value
		self.cycle_frequency = int(self.DEFAULT_FREQUENCY_DIVIDER / value)

	@property
	def cycle_frequency(self): 			return self._cycle_frequency
	@cycle_frequency.setter
	def cycle_frequency(self, value): 	self._cycle_frequency = value

	@property
	def max_serial_events(self): 		return self._max_serial_events
	@max_serial_events.setter
	def max_serial_events(self, value): self._max_serial_events = value
