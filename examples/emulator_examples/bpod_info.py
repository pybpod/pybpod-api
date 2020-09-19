from pybpodapi.protocol import Bpod
from confapp import conf
my_bpod = Bpod(emulator_mode=True)
my_bpod.close()
print("Target Bpod firmware version: ", conf.TARGET_BPOD_FIRMWARE_VERSION)
print("Firmware version (read from device): ",
      my_bpod.hardware.firmware_version)
print("Machine type version (read from device): ",
      my_bpod.hardware.machine_type)
