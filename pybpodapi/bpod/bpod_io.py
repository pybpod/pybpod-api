# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging, os

from pysettings import conf as settings
from pybpodapi.bpod.bpod_com_protocol_modules import BpodCOMProtocolModules
from pybpodapi.trial import Trial

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
		

	def start(self):
		super(BpodIO,self).start()
		
		if self.protocol_name and self.protocol_name:
			if not os.path.exists(self.workspace_path): os.makedirs(self.workspace_path)
			self.csv_exporter  = CSVExporter(self.workspace_path, self.protocol_name)
			self.json_exporter = JSONExporter(self.workspace_path, self.protocol_name)
		else:
			self.csv_exporter = self.json_exporter = None

		return self

	
	def stop(self):
		"""

		"""
		super(BpodIO,self).stop()

		if len(self.session.trials) and self.csv_exporter:
			self.csv_exporter.add_session_metadata(self.session)


	def _publish_data(self, data):
		"""
		Publish data from current trial as CSV and JSON.
		This method can be overwritten from other projects that use pybpod-api libraries to export data in a customized way.

		.. seealso::
			:py:meth:`pybpodapi.model.bpod.bpod_base.BpodBase._publish_data`.


		:param data: data to be published (data type varies)
		"""
		super(BpodIO, self)._publish_data(data)

		if isinstance(data, Trial) and self.csv_exporter:
			self.csv_exporter.save_trial(data, len(self.session.trials))

		if isinstance(data, Trial) and self.json_exporter:
			self.json_exporter.save_trial(data, len(self.session.trials))


	#########################################
	############## PROPERTIES ###############
	#########################################

	@property
	def csv_exporter(self):
		return self._csv_exporter  # type: CSVExporter

	@csv_exporter.setter
	def csv_exporter(self, value):
		self._csv_exporter = value  # type: CSVExporter

	@property
	def json_exporter(self):
		return self._json_exporter  # type: JSONExporter

	@json_exporter.setter
	def json_exporter(self, value):
		self._json_exporter = value  # type: JSONExporter

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