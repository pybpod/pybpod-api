import sys, io
from pybpodapi.com.messaging.base_message import BaseMessage
from pybpodapi.com.messaging.stderr import StderrMessage


class StderrBuffer(io.StringIO):

	def __init__(self, session):
		self.session = session

	def write(self, msg):
		self.session += StderrMessage(msg)

	def flush(self):
		sys.__stdout__.flush()