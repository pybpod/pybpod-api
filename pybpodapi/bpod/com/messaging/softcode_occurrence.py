# !/usr/bin/python3from pybpodapi.bpod.com.messaging.base_message import BaseMessage
# -*- coding: utf-8 -*-
import dateutil
from pybpodapi.bpod.com.messaging.base_message import BaseMessage


class SoftcodeOccurrence(BaseMessage):
	"""
	Message from board that represents state change (an event)

	:ivar str event_name: name of the event
	:ivar int event_id: index of the event
	:ivar float board_timestamp: timestamp associated with this event (from bpod)

	"""
	MESSAGE_TYPE_ALIAS = 'SOFTCODE'
	MESSAGE_COLOR = (40,30,30)
	
	def __init__(self, event_id, host_timestamp=None):
		"""

		:param event_id:
		:param event_name:
		:param host_timestamp:
		"""		
		super(SoftcodeOccurrence, self).__init__(event_id, host_timestamp)


	
	@property
	def softcode(self): return self.content


	def tolist(self):
		return [
			self.MESSAGE_TYPE_ALIAS, 
			str(self.pc_timestamp), 
			self.host_timestamp,
			self.event_id,
			self.content
		]

	@classmethod
	def fromlist(cls, row):
		"""
		Returns True if the typestr represents the class
		"""
		obj = cls(
			int(row[3]),
			row[4]
		)
		obj.pc_timestamp = dateutil.parser.parse(row[1])

		return obj