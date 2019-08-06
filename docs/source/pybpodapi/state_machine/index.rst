.. _api_state_machine-label:

*************************************
:mod:`state_machine`--- State Machine
*************************************

.. module:: pybpodapi.state_machine
   :synopsis: state machine logic

.. toctree::
   :titlesonly:

   state_machine
   builder
   runner

Overview
--------
Each Bpod trial is programmed as a virtual finite state machine. This ensures precise timing of events - for any state machine you program, state transitions will be completed in less than 250 microseconds - so inefficient coding won't reduce the precision of events in your data.

For more information, please see https://sites.google.com/site/bpoddocumentation/bpod-user-guide/using-state-matrices .

Inheritance
~~~~~~~~~~~~~~~~

.. inheritance-diagram:: pybpodapi.state_machine.StateMachine 
   :parts: 1

|
|
