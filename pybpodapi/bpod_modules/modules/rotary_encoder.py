from pybpodapi.bpod_modules.bpod_module import BpodModule


class RotaryEncoder(BpodModule):

	def activate_outputstream(self):
		self.write_char_array([ord('O'),1])

	def deactivate_outputstream(self):
		self.write_char_array([ord('O'),0])

	def stop_streaming_and_logging(self):
		self.write_char_array([ord('X')])

	def enable_positions_threshold(self):
		self.write_char_array([ord('E')])

	def set_position_zero(self):
		self.write_char_array([ord('Z')])

	def starts_logging(self):
		self.write_char_array([ord('L')])

	def stops_logging(self):
		self.write_char_array([ord('F')])