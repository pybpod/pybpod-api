 .. pybpodapi documentation master file, created by
   sphinx-quickstart on Wed Jan 18 09:35:10 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _installing-label:

**********
Installing
**********

.. note::
    
    To install the **full pybpod package**, please follow the instructions located @ `Pybpod <http://pybpod.readthedocs.org>`_.


.. warning::
   This project uses Python 3!

Clone the project from Bitbucket
================================

::

    git clone https://bitbucket.org/fchampalimaud/pybpod-api

Install files
=============

On the project root folder (where *'setup.py'* is located) run the following commands:

::

    pip3 install -r requirements.txt --upgrade # installs dependencies
    pip3 install . --upgrade # installs this API


Settings file
=============

::

    # list of python libraries to interfaces bpod modules. 
    PYBPOD_API_MODULES = [
        'pybpod_rotaryencoder_module'
    ]

    PYBPOD_SERIAL_PORT = '/dev/ttyACM0'  # serial port settings
    PYBPOD_NET_PORT    = '' # network port to receive remote commands like softcodes.

    # enable or disable bpod ports
    BPOD_BNC_PORTS_ENABLED      = [True, True]
    BPOD_WIRED_PORTS_ENABLED    = [True, True]
    BPOD_BEHAVIOR_PORTS_ENABLED = [True, True, True, True, True, True, True, True]

    PYBPOD_PROTOCOL     = '' # Executed protocol
    PYBPOD_CREATOR      = '' # Name of the user
    PYBPOD_PROJECT      = '' # Name of the project
    PYBPOD_EXPERIMENT   = '' # Name of the experiment
    PYBPOD_BOARD        = '' # Board name
    PYBPOD_SETUP        = '' # Setup name
    PYBPOD_SESSION      = '' # Name of the session file
    PYBPOD_SESSION_PATH = '' # Folder where the bpod output files are be saved
    PYBPOD_SUBJECTS     = [] # List of subjects to be saved in the session file.
