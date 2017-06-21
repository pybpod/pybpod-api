.. _writing-protocols-label:

***************************
Writing a protocol for Bpod
***************************

What is a Bpod protocol?
========================

To use Bpod, you must first program a behavioral protocol. The following guide is based on the original version for `Bpod Matlab <https://sites.google.com/site/bpoddocumentation/bpod-user-guide/protocol-writing>`_.


Protocol example explained
==========================

First, you will need to import Bpod modules.

.. code-block:: python
    :linenos:
    :lineno-start: 1

    from pybpodapi.model.bpod import Bpod # Bpod main module
    from pybpodapi.model.state_machine import StateMachine # State machine module
    from pybpodapi.hardware.events import EventName # Input events labels
    from pybpodapi.hardware.output_channels import OutputChannel # Output action labels

Then, initialize Bpod and provide serial connection, workspace path (where bpod output will show up) and provide the protocol name (this is needed for internal configurations and GUI compatibility).

.. code-block:: python
    :linenos:
    :lineno-start: 5

    my_bpod = Bpod().start(settings.SERIAL_PORT, settings.WORKSPACE_PATH, "add_trial_events")

You can run several trials for each Bpod execution. In this example, we will use 5 trials. Each trial can be of type1 (rewarded left) or type2 (rewarded right).

.. code-block:: python
    :linenos:
    :lineno-start: 6

    nTrials = 5
    trialTypes = [1, 2]  # 1 (rewarded left) or 2 (rewarded right)

    for i in range(nTrials):  # Main loop
        print('Trial: ', i+1)
        thisTrialType = random.choice(trialTypes)  # Randomly choose trial type =
        if thisTrialType == 1:
            stimulus = OutputChannel.PWM1  # set stimulus channel for trial type 1
            leftAction = 'Reward'
            rightAction = 'Punish'
            rewardValve = 1
        elif thisTrialType == 2:
            stimulus = OutputChannel.PWM3  # set stimulus channel for trial type 1
            leftAction = 'Punish'
            rightAction = 'Reward'
            rewardValve = 3

Now, inside the loop, we will create and configure a state machine for each trial.
A state machine has *state name*, *state timer*, *names of states to enter if certain events occur* and *output actions*.
Please see :ref:`State Machine API <api_state_machine-label>` for detailed information about state machine design.

.. warning::
    We strongly advise to use the API available labels as  described on the examples :ref:`output actions <api_output_action_codes-label>` and :ref:`input events <api_input_event_codes-label>`.


.. code-block:: python
    :linenos:
    :lineno-start: 22

        sma = StateMachine(my_bpod.hardware)

        sma.add_state(
            state_name='WaitForPort2Poke',
            state_timer=1,
            state_change_conditions={EventName.Port2In: 'FlashStimulus'},
            output_actions=[(OutputChannel.PWM2, 255)])
        sma.add_state(
            state_name='FlashStimulus',
            state_timer=0.1,
            state_change_conditions={EventName.Tup: 'WaitForResponse'},
            output_actions=[(stimulus, 255)])
        sma.add_state(
            state_name='WaitForResponse',
            state_timer=1,
            state_change_conditions={EventName.Port1In: leftAction, EventName.Port3In: rightAction},
            output_actions=[])
        sma.add_state(
            state_name='Reward',
            state_timer=0.1,
            state_change_conditions={EventName.Tup: 'exit'},
            output_actions=[(OutputChannel.Valve, rewardValve)])  # Reward correct choice
        sma.add_state(
            state_name='Punish',
            state_timer=3,
            state_change_conditions={EventName.Tup: 'exit'},
            output_actions=[(OutputChannel.LED, 1), (OutputChannel.LED, 2), (OutputChannel.LED, 3)])  # Signal incorrect choice


After configuring the state machine, we send it to the Bpod device by calling the method *send_state_machine*. We are then ready to run the next trial, by calling the *run_state_machine* method.
On run completion, we can print the data available for the current trial including events and states.

.. code-block:: python
    :linenos:
    :lineno-start: 49

        my_bpod.send_state_machine(sma)  # Send state machine description to Bpod device

        print("Waiting for poke. Reward: ", 'left' if thisTrialType == 1 else 'right')

        my_bpod.run_state_machine(sma)  # Run state machine

        print("Current trial info: ", my_bpod.session.current_trial())



Finally, after the loop finishes, we can stop Bpod execution.

.. code-block:: python
    :linenos:
    :lineno-start: 56

    my_bpod.stop()  # Disconnect Bpod and perform post-run actions

.. seealso::

    :py:class:`pybpodapi.model.bpod.bpod_base.BpodBase`

    :py:meth:`pybpodapi.model.bpod.bpod_base.BpodBase.start`

    :py:class:`pybpodapi.model.state_machine.state_machine_base.StateMachineBase`

    :py:meth:`pybpodapi.model.state_machine.state_machine_base.StateMachineBase.add_state`

    :py:class:`pybpodapi.hardware.output_channels.OutputChannel`

    :py:class:`pybpodapi.hardware.events.EventName`

    :py:meth:`pybpodapi.model.bpod.bpod_base.BpodBase.send_state_machine`

    :py:meth:`pybpodapi.model.bpod.bpod_base.BpodBase.run_state_machine`

    :py:meth:`pybpodapi.model.bpod.bpod_base.BpodBase.stop`


Try the example
===============

You can try the full example by :ref:`installing <installing-label>` and :ref:`running <running-label>` this library.