.. _api_output_action_codes-label:

*******************
Output action codes
*******************

Overview
========
Output actions are specified via string labels. Although you can manually specify these values, **we strongly advise to use the API available labels instead** (:py:class:`pybpodapi.hardware.output_channels.OutputChannel`).

Standard port setup LED control
-------------------------------

For ease of use and convenience, you can use 'LED' label to control LEDs. This is equivalent to control PWM channels.

======================  ===========================  =========================================================================
Action label            Action value                 Example 'OutputActions' for state matrix
======================  ===========================  =========================================================================
LED                     LED Port number (1-8)        (OutputChannel.LED, 1) # Port 1 LED to full brightness (Equivalent to (OutputChannel.PWM1, 255))
======================  ===========================  =========================================================================


Solenoid valve control
----------------------

You can control one valve per each standard port setup.

======================  ===========================  =========================================================================
Action label            Action value                 Example 'OutputActions' for state matrix
======================  ===========================  =========================================================================
ValveState or Valve     8 Bits = 8 valves            (OutputChannel.ValveState, 128) # Set valve 7 set to "open"
======================  ===========================  =========================================================================


Pulse width modulated output line control (LED in standard port setup)
----------------------------------------------------------------------

======================  ===========================  =========================================================================
Action label            Action value                 Example 'OutputActions' for state matrix
======================  ===========================  =========================================================================
PWM1                    Byte ~ duty cycle            (OutputChannel.PWM1, 255) # Set PWM 1 to 100% duty cycle / Port 1 LED to full brightness
...                     ...                          ...
PWM8                    Byte ~ duty cycle            (OutputChannel.PWM8, 128) # Set PWM 8 to 50% duty cycle / Port 8 LED to half brightness
======================  ===========================  =========================================================================


BNC output logic control
------------------------

======================  ===========================  =========================================================================
Action label            Action value                 Example 'OutputActions' for state matrix
======================  ===========================  =========================================================================
BNC1                    2 Bits = 2 channels          (OutputChannel.BNC1, 3) # TODO:
BNC2                    2 Bits = 2 channels          (OutputChannel.BNC2, 3) # TODO:
======================  ===========================  =========================================================================


Wire output logic control
-------------------------

======================  ===========================  =========================================================================
Action label            Action value                 Example 'OutputActions' for state matrix
======================  ===========================  =========================================================================
Wire1                   4 Bits = 4 channels          (OutputChannel.Wire1, 5) # TODO:
Wire2                   4 Bits = 4 channels          (OutputChannel.Wire2, 5) # TODO:
Wire3                   4 Bits = 4 channels          (OutputChannel.Wire3, 5) # TODO:
Wire4                   4 Bits = 4 channels          (OutputChannel.Wire4, 5) # TODO:
======================  ===========================  =========================================================================


Hardware serial ports 1, 2 and 3
--------------------------------

======================  ===========================  =========================================================================
Action label            Action value                 Example 'OutputActions' for state matrix
======================  ===========================  =========================================================================
Serial1                 Byte to send                 (OutputChannel.Serial1, 129) # Send byte 129 to serial port 1
Serial2                 Byte to send                 (OutputChannel.Serial2, 129) # Send byte 129 to serial port 2
Serial3                 Byte to send                 (OutputChannel.Serial3, 129) # Send byte 129 to serial port 3
======================  ===========================  =========================================================================


USB serial port byte
--------------------

======================  ===========================  =========================================================================
Action label            Action value                 Example 'OutputActions' for state matrix
======================  ===========================  =========================================================================
SoftCode                Byte to send                 (OutputChannel.SoftCode, 129) # Send byte 129 to be handled by the governing computer
======================  ===========================  =========================================================================


Global timer control
--------------------

======================  ===========================  =========================================================================
Action label            Action value                 Example 'OutputActions' for state matrix
======================  ===========================  =========================================================================
GlobalTimerTrig         Timer# to start (of 5)       (OutputChannel.GlobalTimerTrig, 2) # Start global timer 2
GlobalTimerCancel       Timer# to cancel (of 5)      (OutputChannel.GlobalTimerCancel, 2) # Start global timer 2
======================  ===========================  =========================================================================


Global counter control
----------------------

======================  ===========================  =========================================================================
Action label            Action value                 Example 'OutputActions' for state matrix
======================  ===========================  =========================================================================
GlobalCounterReset      Counter# to reset (of 5)     (OutputChannel.GlobalCounterReset, 3) # Reset global counter 3
======================  ===========================  =========================================================================

