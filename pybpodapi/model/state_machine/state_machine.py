# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import math
from pybpodapi.hardware.hardware import Hardware
from pybpodapi.model.state_machine.conditions import Conditions
from pybpodapi.model.state_machine.global_counters import GlobalCounters
from pybpodapi.model.state_machine.global_timers import GlobalTimers
from pybpodapi.model.state_machine.raw_data import RawData

logger = logging.getLogger(__name__)


class StateMachine(object):
	"""
	State Machine for Bpod
	"""

	def __init__(self, hardware):
		"""

		:param Hardware hardware:
		"""
		self.hardware = hardware  # type: Hardware

		self.channels = hardware.channels  # TODO: temporary fix, this is not needed

		self.state_names = []
		self.state_timers = [0] * self.hardware.max_states
		self.total_states_added = 0  # holds all states added, even if name is repeated

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

		self.raw_data = RawData()

	def add_state(self, state_name, state_timer, state_change_conditions={}, output_actions=()):
		"""
		Add new state

		:param str name: name of the state
		:param float timer: timer in seconds
		:param dict state_change_conditions:
		:param tuple output_actions:
		"""

		# TODO: WHY DO WE NEED THIS IF-ELSE?
		if state_name not in self.manifest:
			self.state_names.append(state_name)
			self.manifest.append(state_name)
			state_name_idx = len(self.manifest) - 1
		else:
			state_name_idx = self.manifest.index(state_name)
			self.state_names[state_name_idx] = state_name

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
			elif event_code >= self.channels.events_positions.globalTimerEnd:
				self.global_timers.end_matrix[state_name_idx].append((event_code, destination_state_number))
			elif event_code >= self.channels.events_positions.globalTimerStart:
				self.global_timers.start_matrix[state_name_idx].append((event_code, destination_state_number))
			else:
				self.input_matrix[state_name_idx].append((event_code, destination_state_number))

		for action in output_actions:
			action_name = action[0]
			action_value = action[1]
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

		self.total_states_added += 1

	def set_global_timer_legacy(self, timer_number=None, timer_duration=None):
		"""
		Set global timer (legacy version)

		:param int timer_number:
		:param float timer_duration: timer duration in seconds
		"""
		self.global_timers.timers[timer_number - 1] = timer_duration

	def set_global_timer(self, timer_ID, timer_duration, on_set_delay, channel, on_message=1, off_message=0):
		"""
		Set global timer
		:param int timer_ID:
		:param float timer_duration: timer duration in seconds
		:param float on_set_delay:
		:param str channel: channel/port name Ex: 'PWM2'
		:param int on_message:
		"""
		try:
			timer_channel_idx = self.outputChannelNames.index(channel)  # type: int
		except:
			raise SMAError('Error: ' + channel + ' is an invalid output channel name.')

		self.global_timers.timers[timer_ID - 1] = timer_duration
		self.global_timers.on_set_delays[timer_ID - 1] = on_set_delay
		self.global_timers.channels[timer_ID - 1] = timer_channel_idx
		self.global_timers.on_messages[timer_ID - 1] = on_message
		self.global_timers.off_messages[timer_ID - 1] = off_message

	def set_global_counter(self, counter_number=None, target_event=None, threshold=None):
		"""
		Set global counter

		:param int counter_number:
		:param str target_event:
		:param int threshold:
		"""
		event_code = self.channels.event_names.index(target_event)
		self.global_counters.attached_events[counter_number - 1] = event_code
		self.global_counters.thresholds[counter_number - 1] = threshold

	def set_condition(self, condition_number, condition_channel, channel_value):
		"""
		Set condition

		:param int condition_number:
		:param str condition_channel:
		:param int channel_value:
		"""
		channel_code = self.channels.input_channel_names.index(condition_channel)
		self.conditions.channels[condition_number - 1] = channel_code
		self.conditions.values[condition_number - 1] = channel_value


class SMAError(Exception):
	pass
