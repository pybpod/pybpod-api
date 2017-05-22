.. _api_input_event_codes-label:

*****************
Input event codes
*****************

Overview
========
Input events are specified via string labels. Although you can manually specify these values, **we strongly advise to use the API available labels instead** (:py:class:`pybpodapi.hardware.events.EventName`).

Port IR sensor events
---------------------

=========  ============
Byte code  Event syntax
=========  ============
1          Port1In
2          Port1Out
3          Port2In
4          Port2Out
5          Port3In
6          Port3Out
7          Port4In
8          Port4Out
9          Port5In
10         Port5Out
11         Port6In
12         Port6Out
13         Port7In
14         Port7Out
15         Port8In
16         Port8Out
=========  ============


BNC input channel logic
-----------------------

=========  ============
Byte code  Event syntax
=========  ============
17         BNC1High
18         BNC1Low
19         BNC2High
20         BNC2Low
=========  ============


Wire input channel logic
------------------------

=========  ============
Byte code  Event syntax
=========  ============
21         Wire1High
22         Wire1Low
23         Wire2High
24         Wire2Low
25         Wire3High
26         Wire3Low
27         Wire4High
28         Wire4Low
=========  ============


USB soft codes
--------------

=========  ============
29         SoftCode1
30         SoftCode2
31         SoftCode3
32         SoftCode4
33         SoftCode5
34         SoftCode6
35         SoftCode7
36         SoftCode8
37         SoftCode9
38         SoftCode10
=========  ============


State timer elapsed
-------------------

=========  ============
40         Tup
=========  ============


Global timer elapsed
--------------------

=========  ================
41         GlobalTimer1_End
42         GlobalTimer2_End
43         GlobalTimer3_End
44         GlobalTimer4_End
45         GlobalTimer5_End
=========  ================


Global counter threshold exceeded
---------------------------------

=========  ==================
46         GlobalCounter1_End
47         GlobalCounter2_End
48         GlobalCounter3_End
49         GlobalCounter4_End
50         GlobalCounter5_End
=========  ==================