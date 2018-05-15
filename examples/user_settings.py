import datetime, time, logging

PYBPOD_API_LOG_LEVEL = logging.INFO
PYBPOD_API_LOG_LEVEL = logging.DEBUG #logging.WARNING; logging.DEBUG
PYBPOD_API_LOG_FILE  = 'pybpod-api.log'


PYBPOD_SESSION_PATH = 'PYBPOD_SESSION_PATH'
PYBPOD_SESSION 		= datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

PYBPOD_SERIAL_PORT 	= '/dev/ttyACM0'

BPOD_BNC_PORTS_ENABLED 		= [True, True]
BPOD_WIRED_PORTS_ENABLED 	= [True, True]
BPOD_BEHAVIOR_PORTS_ENABLED = [True, True, True, False, False, False, False, False]