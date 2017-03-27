# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging

from pybpodapi.model.bpod.bpod_base import Bpod as BpodBase

from pybpodapi.plugins import CSVExporter

logger = logging.getLogger(__name__)


class BpodIO(BpodBase):
	"""
	Bpod I/O logic.
	"""

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

	def __init__(self):
		BpodBase.__init__(self)

	def start(self, serial_port, workspace_path, protocol_name, baudrate=115200, sync_channel=255, sync_mode=1):
		BpodBase.start(self, serial_port, workspace_path, baudrate, sync_channel, sync_mode)

		self.workspace_path = workspace_path

		self.protocol_name = protocol_name

		# logger.debug("Workspace path: %s", self.workspace_path)

		self.csv_exporter = CSVExporter(self.workspace_path, protocol_name)

		return self

	def _publish_data(self, trial):
		"""

		:param Trial trial:
		:return:
		"""
		self.csv_exporter.save_trial(trial)

	def stop(self):
		"""

		"""
		BpodBase.stop(self)

		self.csv_exporter.add_session_metadata(self.session)
