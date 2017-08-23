*********************
:mod:`trial`--- Trial
*********************

.. module:: trial
    :synopsis: A session trial

Overview
========

Every time Bpod starts running, a new session is created. One session can have multiple trials.

Each trial stores:
    * the session start timestamp
    * timestamps corresponding to all states occurrences (start and end)
    * timestamps corresponding to all events occurrences

Example of a trial pretty-print output:

.. code-block:: python

    {
        'Bpod start timestamp': 0.007,
        'States timestamps': {
            'TimerTrig': [(0, 0.0001)],
            'Port1Lit': [(0.0001, 0.2501), (0.5001, 0.7501), (1.0001, 1.0003), (1.0004, 1.2501), (1.5001, 1.7501), (2.0001, 2.2501)],
            'Port3Lit': [(0.2501, 0.5001), (0.7501, 1.0001), (1.0003, 1.0004), (1.2501, 1.5001), (1.7501, 2.0001), (2.2501, 3.0)]
        },
        'Events timestamps': {
            'Tup': [0.0001, 0.2501, 0.5001, 0.7501, 1.0001, 1.2501, 1.5001, 1.7501, 2.0001, 2.2501, 2.5001, 2.7501],
            'Port2In': [1.0003],
            'Port2Out': [1.0004],
            'GlobalTimer1_End': [3.0]
        }
    }

Implementation
==============


.. automodule:: pybpodapi.trial
    :members:
    :private-members:
