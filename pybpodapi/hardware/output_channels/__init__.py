from pybpodapi.settings import TARGET_BPOD_FIRMWARE_VERSION

if TARGET_BPOD_FIRMWARE_VERSION == '13':
	from pybpodapi.hardware.output_channels.bpod0_7_9_fw13 import OutputChannel
if TARGET_BPOD_FIRMWARE_VERSION == '9':
	from pybpodapi.hardware.output_channels.bpod0_7_5_fw9 import OutputChannel
else:
	from pybpodapi.hardware.output_channels.bpod0_7_5_fw9 import OutputChannel
