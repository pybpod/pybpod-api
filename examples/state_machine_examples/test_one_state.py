

class Cenas(object):
	def run(self):
		protocol_path = "/Users/carlos/Dropbox/Projects/champalimaud-projects/bpod/pybpod-api/examples/state_machine_examples/light_chasing.py"
		SERIAL_PORT = "/dev/tty.usbmodem1461"
		ldict = locals()
		exec(open(protocol_path).read(), globals(), ldict)
		print(ldict)

Cenas().run(


from pybpodgui.model.bpod import Bpod
BPOD_CLASS_WRAPPER = Bpod