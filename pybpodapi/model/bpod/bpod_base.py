# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import math
import time

from pysettings import conf as bpod_settings

from pybpodapi.com.message_api import MessageAPI
from pybpodapi.com.hardware_info_container import HardwareInfoContainer
from pybpodapi.com.serial_message_container import SerialMessageContainer
from pybpodapi.hardware.hardware import Hardware
from pybpodapi.hardware.channels import ChannelType
from pybpodapi.hardware.channels import ChannelName
from pybpodapi.model.session import Session
from pybpodapi.model.state_machine import StateMachine
from pybpodapi.model.trial import Trial
from pybpodapi.model.state_machine.raw_data import RawData
from pybpodapi.model.event_occurrence import EventOccurrence
from pybpodapi.model.softcode_occurrence import SoftCodeOccurrence

logger = logging.getLogger(__name__)


class Status(object):
	"""
	Holds Bpod state machine status
	
	:ivar bool new_sma_sent: whether a new state machine was already uploaded to Bpod box
	"""

	def __init__(self):
		self.new_sma_sent = False  # type: bool


class BpodBase(object):
	"""
	API to interact with Bpod
	
	:ivar Session session: Session for this bpod running experiment
	:ivar Hardware hardware: Hardware object representing Bpod hardware
	:ivar MessageAPI message_api: Abstracts communication with Bpod box
	:ivar Status status: whether a new state machine was already uploaded to Bpod box
	"""

	#########################################
	############## PROPERTIES ###############
	#########################################

	@property
	def session(self):
		return self._session  # type: Session

	@session.setter
	def session(self, value):
		self._session = value  # type: Session

	@property
	def hardware(self):
		return self._hardware  # type: Hardware

	@hardware.setter
	def hardware(self, value):
		self._hardware = value  # type: Hardware

	@property
	def message_api(self):
		return self._message_api  # type: MessageAPI

	@message_api.setter
	def message_api(self, value):
		self._message_api = value  # type: MessageAPI

	@property
	def status(self):
		return self._status  # type: Status

	@status.setter
	def status(self, value):
		self._status = value  # type: Status

	def __init__(self):
		self.hardware = Hardware()  # type: Hardware
		self.session = Session()  # type: Session
		self.message_api = MessageAPI()  # type: MessageAPI
		self.status = Status()  # type: Status

	#########################################
	############ PUBLIC METHODS #############
	#########################################

	def start(self, serial_port, workspace_path, protocol_name, baudrate=115200, sync_channel=255, sync_mode=1):
		"""
		Starts Bpod.

		Connect to Bpod board through serial port, test handshake, retrieve firmware version,
		retrieve hardware description, enable input ports and configure channel synchronization.
		
		Example: 
		
		.. code-block:: python
		
			my_bpod = Bpod().start("/dev/tty.usbmodem1293", "/Users/John/Desktop/bpod_workspace", "2afc_protocol")

		:param str serial_port: serial port to connect
		:param str workspace_path: path for bpod output files (no folders will be created)
		:param str protocol_name: this name will be used for output files
		:param int baudrate [optional]: baudrate for serial connection
		:param int sync_channel [optional]: Serial synchronization channel: 255 = no sync, otherwise set to a hardware channel number
		:param int sync_mode [optional]: Serial synchronization mode: 0 = flip logic every trial, 1 = every state
		:return: Bpod object created
		:rtype: pybpodapi.model.bpod
		"""

		logger.info("Starting Bpod")

		self.message_api.connect(serial_port, baudrate)

		if not self.message_api.handshake():
			raise BpodError('Error: Bpod failed to confirm connectivity. Please reset Bpod and try again.')

		self.hardware.firmware_version, self.hardware.machine_type = self.message_api.firmware_version()
		if self.hardware.firmware_version < int(bpod_settings.BPOD_FIRMWARE_VERSION):
			raise BpodError('Error: Old firmware detected. Please update Bpod 0.7+ firmware and try again.')

		hw_info = HardwareInfoContainer()
		hw_info.sync_channel = sync_channel
		hw_info.sync_mode = sync_mode
		self.message_api.hardware_description(hw_info)
		self.hardware.set_up(hw_info)

		if not self.message_api.enable_ports(self.hardware.inputs_enabled):
			raise BpodError('Error: Failed to enable Bpod inputs.')

		if not self.message_api.set_sync_channel_and_mode(sync_channel=sync_channel,
		                                                  sync_mode=sync_mode):
			raise BpodError('Error: Failed to configure syncronization.')

		return self

	def send_state_machine(self, sma):
		"""
		Builds message and sends state machine to Bpod

		:param pybpodapi.model.state_machine sma: initialized state machine
		"""

		logger.info("Sending state machine")

		sma.update_state_numbers()

		message = sma.build_message()

		message32 = sma.build_message_32_bits()

		self.status.new_sma_sent = True

		self.message_api.send_state_machine(message, message32)

	def run_state_machine(self, sma):
		"""

		Adds a new trial to current session and runs state machine on Bpod box.
		
		While state machine is running, messages are processed accordingly.
		
		When state machine stops, timestamps are updated and trial events are processed.
		
		Finally, data is released for registered data consumers / exporters.
		
		.. seealso::
			
			Add trial: :meth:`pybpodapi.model.session.Session.add_trial`.
			
			Send command "run state machine": :meth:`pybpodapi.com.message_api.MessageAPI.run_state_machine`.
			
			Process opcode: :meth:`pybpodapi.model.bpod.bpod_base.BpodBase._BpodBase__process_opcode`.
			
			Update timestamps: :meth:`pybpodapi.model.bpod.bpod_base.BpodBase._BpodBase__update_timestamps`.
			
			Add trial events: :meth:`pybpodapi.model.bpod.bpod_base.BpodBase._BpodBase__add_trial_events`.
		
			Publish data: :meth:`pybpodapi.model.bpod.bpod_base.BpodBase._publish_data`.
	
		:param pybpodapi.mode.state_machine sma: initialized state machine
		"""

		self.session.add_trial(sma)

		logger.info("Running state machine, trial %s", len(self.session.trials))

		state_change_indexes = []

		self.message_api.run_state_machine()
		if self.status.new_sma_sent:
			if not self.message_api.state_machine_installation_status():
				raise BpodError('Error: The last state machine sent was not acknowledged by the Bpod device.')
			self.status.new_sma_sent = False

		sma.is_running = True
		while sma.is_running:
			if self.message_api.data_available():
				opcode, data = self.message_api.read_opcode_message()
				self.__process_opcode(sma, opcode, data, state_change_indexes)

		self.__update_timestamps(sma, state_change_indexes)

		self.__add_trial_events()

		logger.info("Publishing Bpod trial")

		self._publish_data(self.session.current_trial())

	def manual_override(self, channel_type, channel_name, channel_number, value):
		"""
		Manually override a Bpod channel

		:param ChannelType channel_type: channel type input or output
		:param ChannelName channel_name: channel name like PWM, Valve, etc.
		:param channel_number:
		:param int value: value to write on channel
		"""
		if channel_type == ChannelType.INPUT:
			raise BpodError('Manually overriding a Bpod input channel is not yet supported in Python.')
		elif channel_type == ChannelType.OUTPUT:
			if channel_name == ChannelName.VALVE:
				if value > 0:
					value = math.pow(2, channel_number - 1)
				channel_number = self.hardware.channels.events_positions.output_SPI
				self.message_api.override_digital_hardware_state(channel_number, value)
			elif channel_name == 'Serial':
				self.message_api.send_byte_to_hardware_serial(channel_number, value)
			else:
				try:
					channel_number = self.hardware.channels.output_channel_names.index(
						channel_name + str(channel_number))
					self.message_api.override_digital_hardware_state(channel_number, value)
				except:
					raise BpodError('Error using manual_override: ' + channel_name + ' is not a valid channel name.')
		else:
			raise BpodError('Error using manualOverride: first argument must be "Input" or "Output".')

	def load_serial_message(self, serial_channel, message_ID, serial_message, n_messages=1):
		"""
		Load serial message on Bpod

		:param serial_channel:
		:param message_ID:
		:param serial_message:
		:param n_messages:
		:return:
		"""

		message_container = SerialMessageContainer(serial_channel, message_ID, serial_message,
		                                           n_messages)  # type: SerialMessageContainer

		response = self.message_api.load_serial_message(message_container.format_for_sending());

		if not response:
			raise BpodError('Error: Failed to set serial message.')

	def reset_serial_messages(self):
		"""
		Reset serial messages to equivalent byte codes (i.e. message# 4 = one byte, 0x4)
		"""
		response = self.message_api.reset_serial_messages()

		if not response:
			raise BpodError('Error: Failed to reset serial message library.')

	def stop(self):
		"""
		Close connection with Bpod
		"""
		self.message_api.disconnect()

	def _publish_data(self, data):
		"""
		Publish data from current trial.
		This method can be overwritten from other projects that use pybpod-api libraries to export data in a customized way.

		.. seealso::
			:py:meth:`pybpodapi.model.bpod.bpod_io.BpodIO._publish_data`.


		:param data: data to be published (data type varies)
		"""
		pass

	def softcode_handler_function(self, data):
		"""
		Users can override this function directly on the protocol to handle a softcode from Bpod

		:param int data: soft code number
		"""
		pass

	#########################################
	############ PRIVATE METHODS ############
	#########################################

	def __add_trial_events(self):
		"""
		Fill current trial with latest information
		"""

		self.session.add_trial_events()

	def __add_event_occurrence(self, sma, event_index):

		event_name = self.hardware.channels.get_event_name(event_index)  # type: str

		# TODO: Timestamp implementation on Bpod firmware
		# type: EventOccurrence
		event_occurrence = sma.raw_data.add_event_occurrence(event_index=event_index, event_name=event_name,
		                                                     timestamp=None)

		self._publish_data(data=event_occurrence)

		logger.debug("Event fired: %s", str(event_occurrence))

	def __add_softcode_occurrence(self, sma, data):

		# TODO: Timestamp implementation on Bpod firmware
		# type: SoftCodeOccurrence
		softcode_occurrence = sma.raw_data.add_softcode_occurrence(softcode_number=data, timestamp=None)

		self._publish_data(data=softcode_occurrence)

		logger.debug("Softcode received: %s", str(softcode_occurrence))

	def __process_opcode(self, sma, opcode, data, state_change_indexes):
		"""
		Process data from bpod board given an opcode

		In original bpod, sma.raw_data == raw_events

		:param sma: state machine object
		:param int opcode: opcode number
		:param data: data from bpod board
		:param state_change_indexes:
		:return:
		"""

		if opcode == 1:  # Read events
			n_current_events = data
			current_events = self.message_api.read_current_events(n_current_events)
			transition_event_found = False

			for event in current_events:

				if event == 255:
					sma.is_running = False
				else:
					self.__add_event_occurrence(sma, event)

					# input matrix
					if not transition_event_found:
						logger.debug("transition event not found")
						logger.debug("Current state: %s", sma.current_state)
						for transition in sma.input_matrix[sma.current_state]:
							logger.debug("Transition: %s", transition)
							if transition[0] == event:
								sma.current_state = transition[1]
								if not math.isnan(sma.current_state):
									logger.debug("adding states input matrix")
									sma.raw_data.states.append(sma.current_state)
									state_change_indexes.append(len(sma.raw_data.events_occurrences) - 1)
								transition_event_found = True

					# state timer matrix
					if not transition_event_found:
						this_state_timer_transition = sma.state_timer_matrix[sma.current_state]
						if event == sma.channels.events_positions.Tup:
							if not (this_state_timer_transition == sma.current_state):
								sma.current_state = this_state_timer_transition
								if not math.isnan(sma.current_state):
									logger.debug("adding states state timer matrix")
									sma.raw_data.states.append(sma.current_state)
									state_change_indexes.append(len(sma.raw_data.events_occurrences) - 1)
								transition_event_found = True

					# global timers start matrix
					if not transition_event_found:
						for transition in sma.global_timers.start_matrix[sma.current_state]:
							if transition[0] == event:
								sma.current_state = transition[1]
								if not math.isnan(sma.current_state):
									logger.debug("adding states global timers start matrix")
									sma.raw_data.states.append(sma.current_state)
									state_change_indexes.append(len(sma.raw_data.events_occurrences) - 1)
								transition_event_found = True

					# global timers end matrix
					if not transition_event_found:
						for transition in sma.global_timers.end_matrix[sma.current_state]:
							if transition[0] == event:
								sma.current_state = transition[1]
								if not math.isnan(sma.current_state):
									logger.debug("adding states global timers end matrix")
									sma.raw_data.states.append(sma.current_state)
									state_change_indexes.append(len(sma.raw_data.events_occurrences) - 1)
								transition_event_found = True
				logger.debug("States indexes: %s", sma.raw_data.states)

		elif opcode == 2:  # Handle soft code
			self.softcode_handler_function(data)
			self.__add_softcode_occurrence(sma, data)

		logger.debug("Raw data: %s", sma.raw_data)

	def __update_timestamps(self, sma, state_change_indexes):
		"""
		Read timestamps from Bpod and update state machine info

		:param StateMachine sma:
		:param list state_change_indexes:
		"""
		sma.raw_data.trial_start_timestamp = self.message_api.read_trial_start_timestamp_seconds()  # start timestamp of first trial

		timestamps = self.message_api.read_timestamps()

		sma.raw_data.event_timestamps = [i / float(self.hardware.cycle_frequency) for i in timestamps]

		for event, timestamp in zip(sma.raw_data.events_occurrences, sma.raw_data.event_timestamps):
			event.timestamp = timestamp

		logger.debug("Events with timestamps: %s", [str(event) for event in sma.raw_data.events_occurrences])

		logger.debug("state_change_indexes: %s", state_change_indexes)

		for i in range(len(state_change_indexes)):
			sma.raw_data.state_timestamps.append(sma.raw_data.event_timestamps[i])
		sma.raw_data.state_timestamps.append(sma.raw_data.event_timestamps[-1])


class BpodError(Exception):
	pass
