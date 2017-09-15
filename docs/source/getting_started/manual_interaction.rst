.. _manual-label:

**********************
Manual control of Bpod
**********************

Using pybpod-api, you can directly interact with Bpod hardware. This may be useful for testing and debug purposes.

After :ref:`installing <installing-label>` pybpod-api, open a python terminal and run the following commands:

.. code-block:: python

    from pybpodapi.bpod import Bpod # import Bpod main class
    from pybpodapi.bpod.hardware.channels import ChannelType # import available types of channels
    from pybpodapi.bpod.hardware.channels import ChannelName # import available names of channels

    # connect to bpod

    my_bpod = Bpod() # Start bpod

    # set poke led connected on port 1 to maximum intensity
    my_bpod.manual_override(ChannelType.OUTPUT, ChannelName.PWM, channel_number=1, value=255)

    # set poke led connected on port 1 to half intensity
    my_bpod.manual_override(ChannelType.OUTPUT, ChannelName.PWM, channel_number=1, value=128)

    # turn off poke led connected on port 1
    my_bpod.manual_override(ChannelType.OUTPUT, ChannelName.PWM, channel_number=1, value=128)

    # disconnect from bpod
    my_bpod.stop()


.. seealso::
    For more available commands, please refer to:

        * :meth:`pybpodapi.bpod.bpod_base.BpodBase.manual_override`

        * :class:`pybpodapi.bpod.hardware.channels.ChannelType`

        * :class:`pybpodapi.bpod.hardware.channels.ChannelName`