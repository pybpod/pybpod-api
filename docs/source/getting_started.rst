.. _getting-started-label:

***************
Getting started
***************

What is pybpod-api?
===================
**pybpod-api** is a Python library that enables communication with the latest `Bpod device <https://sanworks.io/shop/viewproduct?productID=1011>`_ version. You can use it directly as a CLI (Command Line Interface) or use your favorite GUI to interact with it.

What is Bpod?
-------------

**Bpod** is a system from `Sanworks <https://sanworks.io/index.php>`_ for precise measurement of small animal behavior.
It is a family of open source hardware devices which includes also software and firmware to control these devices. The software was originally developed in Matlab providing retro-compatibility with the `BControl <http://brodywiki.princeton.edu/bcontrol/index.php/Main_Page>`_ system.

.. seealso::

    Bpod device: https://sanworks.io/shop/viewproduct?productID=1011

    Bpod on Github: https://github.com/sanworks/Bpod

    Bpod Wiki: https://sites.google.com/site/bpoddocumentation/

    BControl project: http://brodywiki.princeton.edu/bcontrol/index.php/Main_Page/


Why a Python port?
------------------
Python is one of the most popular programming languages today `[1] <https://pypl.github.io/PYPL.html>`_. This is special true for the science research community because it is an open language, easy to learn, with a strong support community and with a lot of libraries available.


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