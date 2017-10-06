# !/usr/bin/python3
# -*- coding: utf-8 -*-
import dateutil
from pybpodapi.bpod.com.messaging.base_message import BaseMessage

class SessionInfo(BaseMessage):
	"""
	Stderr message from the server process

	.. seealso::

		:py:class:`pybpodgui_plugin.com.messaging.board_message.BoardMessage`

	"""
	MESSAGE_TYPE_ALIAS = 'INFO'
	MESSAGE_COLOR 	   = (150,150,255)

	def __init__(self, infoname, infovalue):
		super(SessionInfo, self).__init__(infoname)
		self._infovalue = infovalue

	def tolist(self):
		return [
			self.MESSAGE_TYPE_ALIAS, 
			self.pc_timestamp,
			self.host_timestamp,
			self.content,
			self._infovalue
		]

	@classmethod
	def fromlist(cls, row):
		"""
		Returns True if the typestr represents the class
		"""
		obj = cls(row[3],float(row[2]) if row[2] else None)
		obj.pc_timestamp = dateutil.parser.parse(row[1])
		obj._infovalue = row[4] if len(row)>4 else None
		return obj
	
	
	@property
	def infoname(self): return self.content

	@property
	def infovalue(self):return self._infovalue