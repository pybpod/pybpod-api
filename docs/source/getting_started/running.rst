.. pybpodapi documentation master file, created by
   sphinx-quickstart on Wed Jan 18 09:35:10 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _running-label:

****************
Running examples
****************

Configure settings
==================

In order to run protocols you need to specify bpod serial port on the file *'user_settings.py'*.

Example of  *'user_settings.py'*  file:

::

    # -*- coding: utf-8 -*-

    SERIAL_PORT = '/dev/tty.usbmodem1411'



You can duplicate the *'user_settings.py.template'* and save it as *'user_settings.py'*


Running protocol examples (the easy way)
========================================

This library provides a simple script that allows you to choose and run a protocol example.

To run this script execute the following commands:

::

   cd PROJECT_FOLDER/
   python3 -m examples


Screenshot:

.. image:: /_images/running_bpod_script.png
   :scale: 100 %

Running protocol examples (advanced way)
========================================

Alternatively, you can run a specific protocol directly from the command-line interface.

Example for running the *'add_trial_events.py'*:

::

   cd PROJECT_FOLDER/
   python3 -m examples.function_examples.add_trial_events





