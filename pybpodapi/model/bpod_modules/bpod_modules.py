import time
from pybpodapi.model.bpod_modules.bpod_module import BpodModule

class BpodModules(object):
	

	def __init__(self, message_api):
		self.modules 	 = []
		self.message_api = message_api
		
		
	def __add__(self, module):
		module.bpod_modules = self
		self.modules.append(module)

	def __get__(self, index):
		return self.modules[index]

	def __len__(self):
		return len(self.modules)

	def __iter__(self):
		return self.modules

	def activate_module_relay(self, module):
		index = self.modules.index(module)
		self.message_api.activate_module_relay(index)

	def deactivate_module_relay(self, module):
		index = self.modules.index(module)
		self.message_api.deactivate_module_relay(index)

	def stop_modules_relay(self):
		for m in self.modules:
			m.deactivate_module_relay()

		time.sleep(0.1)
		self.message_api.clean_any_data_in_the_buffer()


	def module_write(self, module, message):
		index = self.modules.index(module)
		self.message_api.module_write(index, message)


	def module_read(self, module, size):
		index = self.modules.index(module)
		return self.message_api.module_read(index, size)


	@property
	def relay_is_active(self):
		for m in self.modules:
			if m.relay_active: 
				return True

		return False
