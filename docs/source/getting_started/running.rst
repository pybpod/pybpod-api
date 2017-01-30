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


Running protocol examples using script (easy way)
=================================================

The pybpod-api library provides a simple script that allows you to choose and run a protocol example.

To run this script execute the following commands:

::

   cd PROJECT_FOLDER/
   python3 -m examples


Screenshot:

.. image:: /_images/running_bpod_script.png
   :scale: 100 %

Running protocol examples individually (advanced way)
=====================================================

Alternatively, you can run a specific protocol.

Example for running the *'add_trial_events.py'*:

::

   cd PROJECT_FOLDER/
   python3 -m examples.function_examples.add_trial_events





Available examples
==================

Obtain Bpod Info
----------------
Basic example demonstrating how to initialize Bpod and read version, firmware version and machine type version.

::

   python3 -m examples.function_examples.bpod_info

One state example
-----------------

Simple example of adding a state to the state machine and run it. A timer is used to change state.

::

   python3 -m examples.state_machine_examples.one_state

Light chasing example
---------------------

Simulation of a light chasing scenario. Follow the light on 3 pokes.

Connect noseports to ports 1-3.

::

   python3 -m examples.state_machine_examples.light_chasing

Add trial events
----------------
Demonstration of AddTrialEvents used in a simple visual 2AFC session.

AddTrialEvents formats each trial's data in a human-readable struct, and adds to myBpod.data (to save to disk later)

Connect noseports to ports 1-3.

::

   python3 -m examples.function_examples.add_trial_events

Add trial events 2
------------------
Similiar to previous example but using a global timer and adding more states.

Connect noseports to ports 1-3.

::

   python3 -m examples.function_examples.add_trial_events2


Manual override
---------------
Manually interact with Bpod hardware. For a detailed explanation, please refer to :ref:`Manual control of Bpod <manual-label>`.

::

   python3 -m examples.function_examples.manual_override

Serial messages
---------------
Example on how to use serial capabilities of Bpod.

::

   python3 -m examples.function_examples.serial_message

Global timers and counters examples
-----------------------------------
Several examples demonstrating how to interact with Bpod timers.

::

   python3 -m examples.state_machine_examples.global_timer_example
   python3 -m examples.state_machine_examples.global_timer_example_digital
   python3 -m examples.state_machine_examples.global_timer_start_and_end_events
   python3 -m examples.state_machine_examples.global_counter_example

Setting a condition example
---------------------------

Example on how to set a condition.

::

   python3 -m examples.state_machine_examples.condition_example


UART triggered state example
----------------------------

Example on how a UART event can trigger a state change.

::

   python3 -m examples.state_machine_examples.uart_triggered_state_change




