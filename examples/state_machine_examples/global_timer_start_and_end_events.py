# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Example state machine: A global timer triggers passage through two infinite loops. It is
triggered in the first state, but begins measuring its 3-second Duration
after a 1.5s onset delay. During the onset delay, an infinite loop
toggles two port LEDs (Port1, Port3) at low intensity. When the timer begins measuring,
it sets port 2 LED to maximum brightness, and triggers transition to a second infinite loop with brighter port 1+3 LEDs.
When the timer's 3 second duration elapses, Port2LED is returned low,
and a GlobalTimer1_End event occurs (handled by exiting the state machine).


Example adapted from Josh Sanders' original version on Sanworks Bpod repository
"""

import examples.settings as settings

from pybpodapi.model.bpod import Bpod
from pybpodapi.model.state_machine import StateMachine
from pybpodapi.hardware.events import EventName
from pybpodapi.hardware.output_channels import OutputChannel


def run():
	"""
	Run this protocol now
	"""

	my_bpod = Bpod().start(settings.SERIAL_PORT, settings.WORKSPACE_PATH, "global_timer_start_and_end_events")

	sma = StateMachine(my_bpod.hardware)

	# Set global timer 1 for 3 seconds, following a 1.5 second onset delay after trigger. Link to LED of port 2.
	sma.set_global_timer(timer_ID=1, timer_duration=3, on_set_delay=1.5, channel=OutputChannel.PWM2, on_message=255)

	sma.add_state(
		state_name='TimerTrig',  # Trigger global timer
		state_timer=0,
		state_change_conditions={EventName.Tup: 'Port1Lit_Pre'},
		output_actions=[('GlobalTimerTrig', 1)])

	sma.add_state(
		state_name='Port1Lit_Pre',
		state_timer=.25,
		state_change_conditions={EventName.Tup: 'Port3Lit_Pre', EventName.GlobalTimer1_Start: 'Port1Lit_Post'},
		output_actions=[(OutputChannel.PWM1, 16)])

	sma.add_state(
		state_name='Port3Lit_Pre',
		state_timer=.25,
		state_change_conditions={EventName.Tup: 'Port1Lit_Pre', EventName.GlobalTimer1_Start: 'Port3Lit_Post'},
		output_actions=[(OutputChannel.PWM3, 16)])

	sma.add_state(
		state_name='Port1Lit_Post',
		state_timer=.25,
		state_change_conditions={EventName.Tup: 'Port3Lit_Post', EventName.GlobalTimer1_End: 'exit'},
		output_actions=[(OutputChannel.PWM1, 255)])

	sma.add_state(
		state_name='Port3Lit_Post',
		state_timer=.25,
		state_change_conditions={EventName.Tup: 'Port1Lit_Post', EventName.GlobalTimer1_End: 'exit'},
		output_actions=[(OutputChannel.PWM3, 255)])

	my_bpod.send_state_machine(sma)

	my_bpod.run_state_machine(sma)

	print("Current trial info: {0}".format(my_bpod.session.current_trial()))

	my_bpod.stop()


if __name__ == '__main__':
	settings.run_this_protocol(run)
