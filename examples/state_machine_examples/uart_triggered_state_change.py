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

	my_bpod = Bpod().start(settings.SERIAL_PORT, settings.WORKSPACE_PATH, "uart_triggered_state_change")

	sma = StateMachine(my_bpod.hardware)

	sma.add_state(
		state_name='Port1Light',
		state_timer=0,
		state_change_conditions={'Serial2_3': 'Port2Light'},  # Go to Port2Light when byte 0x3 arrives on UART port 2
		output_actions=[('PWM1', 255)])

	sma.add_state(
		state_name='Port2Light',
		state_timer=0,
		state_change_conditions={'Tup': 'exit'},
		output_actions=[('PWM2', 255)])

	my_bpod.send_state_machine(sma)

	my_bpod.run_state_machine(sma)

	print("Current trial info: ", my_bpod.session.current_trial())

	my_bpod.stop()


if __name__ == '__main__':
	settings.run_this_protocol(run)
