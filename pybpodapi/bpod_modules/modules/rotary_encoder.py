from pybpodapi.bpod_modules.bpod_module import BpodModule


class RotaryEncoder(BpodModule):

	COM_TOGGLEOUTPUTSTREAM 		= ord('O')
	COM_STOP_STREAMANDLOGGING 	= ord('X')
	COM_ENABLE_ALLTHRESHOLDS 	= ord('E')
	COM_SETZEROPOS 		 		= ord('Z')
	COM_START_LOGGING 			= ord('L')
	COM_STOP_LOGGING 			= ord('F')

	def activate_outputstream(self):
		self.write_char_array([self.COM_TOGGLEOUTPUTSTREAM,1])

	def deactivate_outputstream(self):
		self.write_char_array([self.COM_TOGGLEOUTPUTSTREAM,0])

	def stop_streaming_and_logging(self):
		self.write_char_array([self.COM_STOP_STREAMANDLOGGING])

	def enable_positions_threshold(self):
		self.write_char_array([self.COM_ENABLE_ALLTHRESHOLDS])

	def set_position_zero(self):
		self.write_char_array([self.COM_SETZEROPOS])

	def starts_logging(self):
		self.write_char_array([self.COM_START_LOGGING])

	def stops_logging(self):
		self.write_char_array([self.COM_STOP_LOGGING])