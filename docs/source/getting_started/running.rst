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

In order to run protocols you need to specify a bpod *'user_settings.py'*
file that should be located at the execution folder.

Example of *'examples/user_settings.py'*  file:

::

    # -*- coding: utf-8-*-

    PYBPOD_API_LOG_LEVEL = None

    PYBPOD_SESSION_PATH  = 'SESSION-WORKSPACE'

    # if you do not define the next variable, the PYBPOD_SESSION
    # will assume the current datetime value.
    PYBPOD_SESSION = 'SESSION-NAME'

    SERIAL_PORT   = '/dev/ttyACM0'



Running protocol examples
=====================================================

Example for running the *'add_trial_events.py'*:

::

    cd PROJECT_FOLDER/examples
    python -m function_examples.add_trial_events


Available examples
==================

Obtain Bpod Info
----------------
Basic example demonstrating how to initialize Bpod and read version,
firmware version and machine type version.

.. literalinclude:: ../../../examples/function_examples/bpod_info.py

Run the example with:

::

    python -m function_examples.bpod_info

One state example
-----------------

Simple example of adding a state to the state machine and run it.
A timer is used to change state.

.. literalinclude:: ../../../examples/state_machine_examples/one_state.py

Run the example with:

::

    python -m state_machine_examples.one_state

Light chasing example (3 pokes)
-------------------------------

Simulation of a light chasing scenario. Follow the light on 3 pokes.

Connect noseports to ports 1-3.

.. literalinclude:: ../../../examples/state_machine_examples/light_chasing.py

Run the example with:

::

    python -m state_machine_examples.light_chasing

Light chasing example (2 pokes)
-------------------------------

Simulation of a light chasing scenario. Follow the light on 2 pokes.

Connect noseports to ports 1-2.

.. literalinclude:: ../../../examples/state_machine_examples/light_chasing_2_pokes.py

Run the example with:

::

    python -m state_machine_examples.light_chasing_2_pokes

Add trial events
----------------
Demonstration of AddTrialEvents used in a simple visual 2AFC session.

AddTrialEvents formats each trial's data in a human-readable struct,
and adds to myBpod.data (to save to disk later)

Connect noseports to ports 1-3.

.. literalinclude:: ../../../examples/function_examples/add_trial_events.py

Run the example with:

::

    python -m function_examples.add_trial_events

Add trial events 2
------------------
Similiar to previous example but using a global timer and adding more states.

Connect noseports to ports 1-3.

.. literalinclude:: ../../../examples/function_examples/add_trial_events2.py

Run the example with:

::

    python -m function_examples.add_trial_events2


Manual override
---------------
Manually interact with Bpod hardware. For a detailed explanation,
please refer to :ref:`Manual control of Bpod <manual-label>`.

.. literalinclude:: ../../../examples/function_examples/manual_override.py

Run the example with:

::

    python -m function_examples.manual_override

Serial messages
---------------
Example on how to use serial capabilities of Bpod.

.. literalinclude:: ../../../examples/function_examples/serial_messages.py

Run the example with:
::

    python -m function_examples.serial_messages

Global timers examples
----------------------
Several examples demonstrating how to interact with Bpod timers.

.. literalinclude:: ../../../examples/state_machine_examples/global_timer_example.py

Run the example with:

::

    python -m state_machine_examples.global_timer_example

.. literalinclude:: ../../../examples/state_machine_examples/global_timer_example_digital.py

Run the example with:

::

   python -m state_machine_examples.global_timer_example_digital

.. literalinclude:: ../../../examples/state_machine_examples/global_timer_start_and_end_events.py

Run the example with:

::

   python -m state_machine_examples.global_timer_start_and_end_events

Global counter example
----------------------
After poke2 (PWM2) LED turns off, one will have an infinite loop between LED
of poke1 (PWM1) and LED of poke3 (PWM1).

To interrupt the infinite loop one have to interrupt poke1 or poke3 a number
of times equal to threshold (in this case is 5 times).

.. literalinclude:: ../../../examples/state_machine_examples/global_counter_example.py

Run the example with:

::

    python -m state_machine_examples.global_counter_example

Setting a condition example
---------------------------

Example on how to set a condition.

.. literalinclude:: ../../../examples/state_machine_examples/condition_example.py

Run the example with:

::

    python -m state_machine_examples.condition_example


UART triggered state example
----------------------------

Example on how a UART event can trigger a state change.

.. literalinclude:: ../../../examples/state_machine_examples/uart_triggered_state_change.py

Run the example with:

::

    python -m state_machine_examples.uart_triggered_state_change

