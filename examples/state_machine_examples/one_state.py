# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Example adapted from Josh Sanders' original version on Sanworks Bpod repository
"""

import examples.settings as settings

from pybpodapi.model.bpod import Bpod
from pybpodapi.model.state_machine import StateMachine


def run():
	"""
	Run this protocol now
	"""

	my_bpod = Bpod().start(settings.SERIAL_PORT)

	sma = StateMachine(my_bpod.hardware)

	sma.add_state(
		state_name='myState',
		state_timer=1,
		state_change_conditions={'Tup': 'exit'},
		output_actions=[])

	my_bpod.send_state_machine(sma)

	raw_events = my_bpod.run_state_machine(sma)

	print(raw_events)

	my_bpod.disconnect()


if __name__ == '__main__':
	settings.run_this_protocol(run)
