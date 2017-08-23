# !/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime

from pybpodapi.trial import Trial
from pybpodapi.session import Session


class SessionDataJSONExporter(object):
	"""

	"""
	FILE_EXT = 'json'

	def __init__(self, workspace_path, protocol_name):
		self.filename = "{timestamp}_{protocol}.{ext}".format(timestamp=datetime.now().strftime('%Y%m%d_%H%M%S'),
		                                                      protocol=protocol_name,
		                                                      ext=self.FILE_EXT)

		self.path = os.path.join(workspace_path, self.filename)

		with open(self.path, "w"):
			pass

	def save_trial(self, trial, trial_number):
		"""

		:param Trial trial:
		:return:
		"""

		data2save = trial.export()

		with open(self.path, "a+") as json_file:
			json.dump(data2save, json_file, sort_keys=False, indent=4, separators=(',', ':'))

	def add_session_metadata(self, session):
		"""

		:param Session session:
		:return:
		"""
		pass
