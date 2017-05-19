************************
Bpod output action codes
************************

Overview
========

Solenoid valve control
----------------------

=================  =============  =================================================
Byte code          Action syntax  Example 'OutputActions' for state matrix
=================  =============  =================================================
8 Bits = 8 valves  ValveState     (OutputChannel.ValveState, 128) # Set valve 7 set to "open"
=================  =============  =================================================

BNC output logic control
------------------------

===================  =============  ===================================================
Byte code            Action syntax  Example 'OutputActions' for state matrix
===================  =============  ===================================================
2 Bits = 2 channels  BNCState       (OutputChannel.BNCState, 3) # Set BNC outputs 1 and 2 to "high"
===================  =============  ===================================================

Wire output logic control
-------------------------

===================  =============  ===================================================
Byte code            Action syntax  Example 'OutputActions' for state matrix
===================  =============  ===================================================
4 Bits = 4 channels  WireState      (OutputChannel.WireState, 5) # Set wire outputs 1 and 3 to "high"
===================  =============  ===================================================

..
   Hardware serial ports 1 and 2
   Byte code	Action syntax	Example 'OutputActions' for state matrix
   Byte to send	Serial1Code	{'Serial1Code', 129} % Send byte 129 to serial port 1
   Byte to send	Serial2Code	{'Serial2Code', 129} % Send byte 129 to serial port 2
   USB serial port byte
   Byte code	Action syntax	Example 'OutputActions' for state matrix
   Byte to send	SoftCode
   {'SoftCode', 129} % Send byte 129 to be handled by the governing computer
   Global timer control
   Byte code	Action syntax	Example 'OutputActions' for state matrix
   Timer# to start (of 5)	GlobalTimerTrig	{'GlobalTimerTrig', 2} % Start global timer 2
   Timer# to cancel (of 5)
   GlobalTimerCancel	{'GlobalTimerCancel', 2} % Cancel global timer 2
   Global counter control
   Byte code	Action syntax	Example 'OutputActions' for state matrix
   Counter# to reset (of 5)
   GlobalCounterReset
   {'GlobalCounterReset', 3} % Reset global counter 3
   Pulse width modulated output line control (LED in standard port setup)
   Byte code	Action syntax	Example 'OutputActions' for state matrix
   Byte ~ duty cycle %	PWM1
   {'PWM1', 255} % Set PWM 1 to 100% duty cycle / Port 1 LED to full brightness
   ... PWM8
   {'PWM8', 128} % Set PWM 8 to 50% duty cycle / Port 8 LED to half brightness