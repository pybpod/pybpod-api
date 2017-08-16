

class BpodModule(object):

	def __init__(self, connected=False, module_name='', firmware_version=0, events_names=[]):
		self.name 				= module_name
		self.connected 			= connected
		self.firmware_version 	= firmware_version
		self.event_names 		= events_names
		
		self.n_serial_events 	= 0
		self.relay_active 		= False

		self.bpod_modules 		= None


	def start_module_relay(self, module_index):
		if self.bpod_modules.relay_is_active:
			self.bpod_modules.activate_module_relay(self)
			self.relay_active = True
		else:
			raise BpodError('Error: You must disable the active module relay before starting another one.')


	def stop_module_relay(self):
		self.bpod_modules.deactivate_module_relay(self)
		self.relay_active = False



	def write(self, message):
		self.bpod_modules.module_write(self, message)

	def read(self, size):
		if not self.relay_active:
			raise BpodError('Error: you must start the module relay with start_moule_relay() before you can read bytes from a module')
		return self.bpod_modules.module_read(self, size)
		