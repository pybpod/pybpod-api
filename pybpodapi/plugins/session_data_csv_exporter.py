# !/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import csv
from datetime import datetime

from pybpodapi.model.trial import Trial
from pybpodapi.model.session import Session


class SessionDataCSVExporter(object):
	"""

	"""
	FILE_EXT = 'csv'

	def __init__(self, workspace_path, protocol_name):
		self.filename = "{timestamp}_{protocol}.{ext}".format(timestamp=datetime.now().strftime('%Y%m%d_%H%M%S'),
		                                                      protocol=protocol_name,
		                                                      ext=self.FILE_EXT)

		self.path = os.path.join(workspace_path, self.filename)

		with open(self.path, "w"):
			pass

	def save_trial(self, trial):
		"""

		:param Trial trial:
		:return:
		"""

		with open(self.path, "a+", newline='') as csvfile:
			csv_writer = csv.writer(csvfile, delimiter=',')

			csv_writer.writerow(["Trial number", 1])
			csv_writer.writerow(["States"])

			states_names = trial.states_timestamps.keys()
			for state_name in states_names:
				csv_writer.writerow([state_name])
				csv_writer.writerow(trial.states_timestamps[state_name])

			# csv_writer.writerow("states")

			#			csvfile.write(str(trial))
			#			fd.write('\n')

	def add_session_metadata(self, session):
		"""

		:param Session session:
		:return:
		"""
		with open(self.path, "a+") as csvfile:
			csv_writer = csv.writer(csvfile, delimiter=',')

			csv_writer.writerow(["Trial start timestamp", session.current_trial().bpod_start_timestamp])
