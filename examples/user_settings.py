import datetime, time, logging

PYBPOD_API_LOG_LEVEL = logging.INFO #logging.WARNING; logging.DEBUG
PYBPOD_API_LOG_FILE  = 'pybpod-api.log'


WORKSPACE_PATH 	= 'BPOD-WORKSPACE'

PROTOCOL_NAME 	= datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

SERIAL_PORT 	= '/dev/ttyACM0'





