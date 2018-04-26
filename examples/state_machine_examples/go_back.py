# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Example adapted from Josh Sanders' original version on Sanworks Bpod repository
"""
from pybpodapi.protocol import Bpod, StateMachine


"""
Run this protocol now
"""

my_bpod = Bpod()

sma = StateMachine(my_bpod)

sma.add_state(
	state_name='WaitForChoice',
	state_timer=0,
	state_change_conditions={Bpod.Events.Port1In: 'FlashPort1', Bpod.Events.Port2In: 'FlashPort2'},
	output_actions=[]
)

sma.add_state(
	state_name='FlashPort1',
	state_timer=0.5,
	state_change_conditions={Bpod.Events.Tup: 'WaitForExit'},
	output_actions=[(Bpod.OutputChannels.LED, 1)]
)

sma.add_state(
	state_name='FlashPort2',
	state_timer=0.5,
	state_change_conditions={Bpod.Events.Tup: 'WaitForExit'},
	output_actions=[(Bpod.OutputChannels.LED, 2)]
)

sma.add_state(
	state_name='WaitForExit',
	state_timer=0,
	state_change_conditions={Bpod.Events.Port1In: 'exit', Bpod.Events.Port2In: 'exit', Bpod.Events.Port3In: 'back'},
	output_actions=[]
)

my_bpod.send_state_machine(sma)

my_bpod.run_state_machine(sma)

print("Current trial info: {0}".format(my_bpod.session.current_trial))

my_bpod.close()




