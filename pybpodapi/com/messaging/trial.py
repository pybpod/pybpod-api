# !/usr/bin/python3
# -*- coding: utf-8 -*-
import ciso8601
import logging, pprint, dateutil

from pybpodapi.com.messaging.event_occurrence import EventOccurrence
from pybpodapi.com.messaging.state_occurrence import StateOccurrence
from pybpodapi.com.messaging.base_message import BaseMessage

logger = logging.getLogger(__name__)


class Trial(BaseMessage):
    """
    :ivar float trial_start_timestamp: None
    :ivar StateMachine sma: sma
    :ivar list(StateOccurrence) states_occurrences: list of state occurrences
    :ivar list(EventOccurrence) events_occurrences: list of event occurrences
    """
    MESSAGE_TYPE_ALIAS = 'TRIAL'
    MESSAGE_COLOR = (0, 0, 255)

    def __init__(self, sma=None):
        super(Trial, self).__init__('New trial')
        self.trial_start_timestamp = None
        self.sma = sma  # type: StateMachine
        self.states_occurrences = []  # type: list(StateOccurrence)
        self.events_occurrences = []  # type: list(EventOccurrence)

        self.states = [0]
        self.state_timestamps = [0]
        self.event_timestamps = []  	# see also BpodBase.__update_timestamps

        self.states_durations = {}

    def __add__(self, msg):
        if isinstance(msg, EventOccurrence):
            self.events_occurrences.append(msg)
        elif isinstance(msg, StateOccurrence):
            self.states_occurrences.append(msg)
            if msg.state_name not in self.states_durations:
                self.states_durations[msg.state_name] = []
            self.states_durations[msg.state_name].append((msg.start_timestamp, msg.end_timestamp))

        return self

    def get_timestamps_by_event_name(self, event_name):
        """
        Get timestamps by event name

        :param event_name: name of the event to get timestamps
        :rtype: list(float)
        """
        event_timestamps = []  # type: list(float)

        for event in self.events_occurrences:
            name = self.sma.hardware.channels.get_event_name(event.event_id)
            if name == event_name:
                event_timestamps.append(event.host_timestamp)

        return event_timestamps

    def get_events_names(self):
        """
        Get events names without repetitions

        :rtype: list(str)
        """
        events_names = []  # type: list(str)

        for event in self.events_occurrences:
            event_name = self.sma.hardware.channels.get_event_name(event.event_id)
            if event_name not in events_names:
                events_names.append(event_name)

        return events_names

    def get_all_timestamps_by_event(self):
        """
        Create a dictionary whose keys are events names and values are corresponding timestamps

        Example:

	@classmethod
	def fromlist(cls, row):
		"""
		Returns True if the typestr represents the class
		"""
		obj = cls()
		obj.pc_timestamp = ciso8601.parse_datetime(row[1])
		return obj