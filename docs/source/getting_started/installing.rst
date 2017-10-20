.. pybpodapi documentation master file, created by
   sphinx-quickstart on Wed Jan 18 09:35:10 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _installing-label:

**********
Installing
**********

.. warning::
   This project uses Python 3!

Download project
================


Option A. Clone project from Bitbucket:
---------------------------------------

::

    git clone https://bitbucket.org/fchampalimaud/pybpod-api


Option B. Download zip
----------------------

https://bitbucket.org/fchampalimaud/pybpod-api/get/master.zip

Install files
=============

On the project root folder (where *'setup.py'* is located) run the following commands:

::

    pip3 install -r requirements.txt --upgrade # installs dependencies
    pip3 install . --upgrade # installs this API


Settings file
=============

::

	# list of python libraries that interfaces with a specific bpod modules. 
	PYBPOD_API_MODULES = [
		'bpod_rotaryencoder_module'
	]

	# folder where the bpod output files will be saved
	WORKSPACE_PATH 	= 'BPOD-WORKSPACE'

	# name of the session file
	PROTOCOL_NAME	= now()  

	# serial port settings
	BAUDRATE 		= 1312500
	SYNC_CHANNEL	= 255
	SYNC_MODE		= 1
	SERIAL_PORT = '/dev/ttyACM0'

	# enable or disable bpod ports
	BPOD_BNC_PORTS_ENABLED 		= [True, True]
	BPOD_WIRED_PORTS_ENABLED 	= [True, True]
	BPOD_BEHAVIOR_PORTS_ENABLED	= [True, True, True, True, True, True, True, True]



