*********************************************
:mod:`state_occurrences`--- State occurrences
*********************************************

.. module:: state_occurrences
   :synopsis: stores timestamps for a specific state occurrence of the state machine

Overview
--------

During trial run, the state machine will progress through different states.
We call each state change, a state occurrence.
A specific state may occur several times, thus there is a list of timestamps associated with the state occurrence.
The state occurrence has a start timestamp (when an event fired this state) and an end timestamp (when an event fired the change for another state). This is called the state duration.

Unlike event occurrences where there is one instance created for each event (thus one instance per timestamp), there is only one instance for a state occurrence. This instance then stores all related timestamps. This is due to historical compatibility.

Implementation
--------------

.. autoclass:: pybpodapi.model.state_occurrences.StateOccurrences
    :members:
    :private-members:

.. autoclass:: pybpodapi.model.state_occurrences.StateDuration
    :members:
    :private-members:
