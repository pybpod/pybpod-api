# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import math
from bpodapi.model.state_machine.channels import StateMachineChannels

logger = logging.getLogger(__name__)


class GlobalTimers(object):
	def __init__(self, max_states, n_global_timers):
		self.matrix = [[] for i in range(max_states)]
		self.timers = [0] * n_global_timers


class GlobalCounters(object):
	def __init__(self, max_states, n_global_counters):
		self.matrix = [[] for i in range(max_states)]
		self.attached_events = [254] * n_global_counters
		self.thresholds = [0] * n_global_counters


class Conditions(object):
	def __init__(self, max_states, n_conditions):
		self.matrix = [[] for i in range(max_states)]
		self.values = [0] * n_conditions
		self.channels = [0] * n_conditions


class StateMachine(object):
	def __init__(self):
		pass

	def set_up(self, hardware):
		self.hardware = hardware

		self.channels = StateMachineChannels()
		self.channels.set_up_input_channels(self.hardware)
		self.channels.set_up_output_channels(self.hardware.outputs)

		logger.debug(self.channels)

		self.state_names = []
		self.state_timers = [0] * self.hardware.max_states

		# state change conditions
		self.state_timer_matrix = [0] * self.hardware.max_states
		self.conditions = Conditions(self.hardware.max_states, self.hardware.n_conditions)
		self.global_counters = GlobalCounters(self.hardware.max_states, self.hardware.n_global_counters)
		self.global_timers = GlobalTimers(self.hardware.max_states, self.hardware.n_global_timers)
		self.input_matrix = [[] for i in range(self.hardware.max_states)]
		self.manifest = []  # List of states that have been added to the state machine
		self.undeclared = []  # List of states that have been referenced but not yet added

		# output actions
		self.meta_output_names = ('Valve', 'LED')
		self.output_matrix = [[] for i in range(self.hardware.max_states)]

	def add_state(self, state_name, state_timer, state_change_conditions={}, output_actions=()):
		"""

		:param name:
		:param timer:
		:param state_change_conditions:
		:param output_actions:
		"""

		if state_name not in self.manifest:
			self.state_names.append(state_name)
			self.manifest.append(state_name)
			state_name_idx = len(self.manifest) - 1
		else:
			state_name_idx = self.manifest.index(state_name)
			self.state_names[state_name_idx] = state_name

		print(state_name_idx)
		self.state_timer_matrix[state_name_idx] = state_name_idx

		self.state_timers[state_name_idx] = state_timer

		for event_name, event_state_transition in state_change_conditions.items():
			try:
				event_code = self.channels.event_names.index(event_name)
			except:
				raise SMAError('Error creating state: ' + state_name + '. ' + event_name + ' is an invalid event name.')

			if event_state_transition in self.manifest:
				destination_state_number = self.manifest.index(event_state_transition)
			else:
				if event_state_transition == 'exit':
					destination_state_number = float('NaN')
				else:  # Send to an undeclared state (replaced later with actual state in myBpod.sendStateMachine)
					self.undeclared.append(event_state_transition)
					destination_state_number = (len(self.undeclared) - 1) + 10000
			if event_code == self.channels.events_positions.Tup:
				self.state_timer_matrix[state_name_idx] = destination_state_number
			elif event_code >= self.channels.events_positions.condition:
				self.conditions.matrix[state_name_idx].append((event_code, destination_state_number))
			elif event_code >= self.channels.events_positions.globalCounter:
				self.global_counters.matrix[state_name_idx].append((event_code, destination_state_number))
			elif event_code >= self.channels.events_positions.globalTimer:
				self.globalTimers.matrix[state_name_idx].append((event_code, destination_state_number))
			else:
				self.input_matrix[state_name_idx].append((event_code, destination_state_number))

		for action_name, action_value in output_actions.items():
			if action_name in self.meta_output_names:
				meta_action = self.meta_output_names.index(action_name)
				if meta_action == 0:  # Valve
					output_code = self.channels.output_channel_names.index('ValveState')
					output_value = math.pow(2, action_value - 1)
				elif meta_action == 1:  # LED
					output_code = self.channels.output_channel_names.index('PWM' + str(action_value))
					output_value = 255;
				else:
					raise SMAError('Error: a meta-action was unhandled.')
			else:
				try:
					output_code = self.channels.output_channel_names.index(action_name)
				except:
					raise SMAError(
						'Error creating state: ' + state_name + '. ' + action_name + ' is an invalid output name.')
				output_value = action_value

			self.output_matrix[state_name_idx].append((output_code, output_value))

	def set_global_timer(self, timer_number, timer_duration):
		"""
		Set global timer

		:param timerNumber:
		:param timerDuration:
		:return:
		"""
		self.global_timers.timers[timer_number - 1] = timer_duration

	def set_global_counter(self, counter_number, counter_event, threshold):
		"""
		Set global counter

		:param counterNumber:
		:param counterEvent:
		:param threshold:
		:return:
		"""
		event_code = self.channels.event_names.index(counter_event)
		self.global_counters.attached_events[counter_number - 1] = event_code
		self.global_counters.thresholds[counter_number - 1] = threshold

	def set_condition(self, condition_number, condition_channel, channel_value):
		"""
		Set condition

		:param conditionNumber:
		:param conditionChannel:
		:param channelValue:
		:return:
		"""
		channel_code = self.channels.input_channel_names.index(condition_channel)
		self.conditions.channels[condition_number - 1] = channel_code
		self.conditions.values[condition_number - 1] = channel_value


class SMAError(Exception):
	pass
