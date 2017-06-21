==========================================================
:mod:`hardware_info_container` --- Hardware Info Container
==========================================================

--------
Overview
--------

This container is used to store hardware description received from Bpod device.
After, this info will be used to fill the :class:`pybpodapi.hardware.hardware.Hardware` object.
The reason to use this container is because :class:`pybpodapi.hardware.hardware.Hardware` does some initializations that depend on information collected from several protocol commands.

--------------
Implementation
--------------


.. automodule:: pybpodapi.com.hardware_info_container
    :members:
    :private-members: