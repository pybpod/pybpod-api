*************************
:mod:`session`--- Session
*************************

.. module:: session
   :synopsis: session to run on bpod

Overview
--------

Everytime a :py:class:`pybpodapi.bpod` object is created, a new session is instantiated which stores information about the new experiment being run.
There is only one session per Bpod. This session contains the list of trials (see :py:class:`pybpodapi.trial.Trial`).

Besides storing trials, the session is also responsible for processing :py:class:`pybpodapi.state_occurrences.StateOccurrences` and :py:class:`pybpodapi.event_occurrence.EventOccurrence` when trial has finished.
At this point, the information collected temporarily on the :py:class:`pybpodapi.state_machine.raw_data.RawData` object is then persisted on the trial.

Implementation
--------------

.. autoclass:: pybpodapi.session.Session
    :members:
    :private-members:

