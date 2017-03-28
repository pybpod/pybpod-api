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

	def save_trial(self, trial, trial_number):
		"""

		:param Trial trial:
		:return:
		"""

		with open(self.path, "a+", newline='') as csvfile:
			csv_writer = csv.writer(csvfile, delimiter=',')

			csv_writer.writerow(["Trial number", trial_number])
			csv_writer.writerow([])
			csv_writer.writerow(["State name", "Start", "End"])

			for state in trial.states:
				for state_dur in state.timestamps:
					csv_writer.writerow([state.name, state_dur.start, state_dur.end])

			csv_writer.writerow([])
			csv_writer.writerow(["Event name", "Start", "End"])

			for event in trial.events:
				csv_writer.writerow([event.name] + event.timestamps)

			csv_writer.writerow([])

	def add_session_metadata(self, session):
		"""

		:param Session session:
		:return:
		"""
		with open(self.path, "a+") as csvfile:
			csv_writer = csv.writer(csvfile, delimiter=',')

			csv_writer.writerow([])

			csv_writer.writerow(["Trial start timestamp", session.current_trial().bpod_start_timestamp])
