# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, os

from pysettings import conf as settings
from pybpodapi.bpod.bpod_com_protocol_modules import BpodCOMProtocolModules
from pybpodapi.bpod.com.messaging.trial import Trial
from pybpodapi.session import Session

from pybpodapi.plugins import CSVExporter
from pybpodapi.plugins import JSONExporter

logger = logging.getLogger(__name__)


class BpodIO(BpodCOMProtocolModules):
	"""
	Bpod I/O logic.
	"""

	def __init__(self, serial_port=None, workspace_path=None, protocol_name=None, sync_channel=None, sync_mode=None):
		super(BpodIO,self).__init__(serial_port, sync_channel, sync_mode)

		self.workspace_path = workspace_path if workspace_path 	is not None else settings.WORKSPACE_PATH
		self.protocol_name	= protocol_name  if protocol_name 	is not None else settings.PROTOCOL_NAME

		if self.workspace_path:
			self._session = Session(os.path.join(self.workspace_path, self.protocol_name))  	# type: Session
		else:
			self._session = Session()
		

	@property
	def workspace_path(self):
		return self._workspace_path  # type: str

	@workspace_path.setter
	def workspace_path(self, value):
		self._workspace_path = value  # type: str

	@property
	def protocol_name(self):
		return self._protocol_name  # type: str

	@protocol_name.setter
	def protocol_name(self, value):
		self._protocol_name = value  # type: str