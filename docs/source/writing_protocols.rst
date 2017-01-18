***************************
Writing a protocol for Bpod
***************************

What is a protocol?
===================



What is pybpod-api?
===================
Python is one of the most popular programming languages today `[1] <https://pypl.github.io/PYPL.html>`_. This is special true for the science research community because it is an open language, easy to learn, with a strong support community and with a lot of libraries available.

**pybpod-api** is a Python library that enables communication with the latest `Bpod device <https://sanworks.io/shop/viewproduct?productID=1011>`_ version.

You can use it directly as a CLI (Command Line Interface) or use your favorite GUI to interact with it.

Installation
============

1. Clone project from Bitbucket:

::

    git clone https://bitbucket.org/fchampalimaud/pybpod-api

2. On the project root folder run (where *'setup.py'* is located):

::

    pip3 install -r requirements.txt --upgrade # installs dependencies
    pip3 install . # installs this API

Running examples
================

1. Duplicate *'user_settings.py.template'* and save it as *'user_settings.py'*
2. Define the *SERIAL_PORT* attribute with your machine serial port where Bpod is connected to
3. Define the *API_LOG_LEVEL* with *logging.DEBUG* if you want detailed logging for the API
4. Change dir to the examples folder and run example:

::

        cd PROJECT_FOLDER/examples/function_examples
        python3 add_trial_events.py # run example


Example of  *'user_settings.py'*  file:

::

    # -*- coding: utf-8 -*-

    import logging

    API_LOG_LEVEL = logging.INFO
    EXAMPLE_SCRIPT_LOG_LEVEL = logging.INFO

    SERIAL_PORT = '/dev/tty.usbmodem1411'