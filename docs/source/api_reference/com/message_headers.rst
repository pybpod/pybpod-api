========================
Protocol Message Headers
========================

.. contents:: Contents
    :local:

--------
Overview
--------

The protocol to talk with Bpod device is defined by the Arduino firmware version installed.

Each message sent or received from Bpod contains a header which is the first byte (character). This header defines the type of action that should be executed.

--------------
Implementation
--------------


.. automodule:: pybpodapi.com.message_headers
    :members:
    :private-members: