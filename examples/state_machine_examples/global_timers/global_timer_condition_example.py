
# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Example adapted from Josh Sanders' original version on Sanworks Bpod repository
"""
from pybpodapi.protocol import Bpod, StateMachine

bpod = Bpod()

bpod.manual_override(2, 'Valve', 1, 0)

"""
sma = StateMachine(bpod)

sma.set_global_timer(
    timer_id=1, timer_duration=1.5, on_set_delay=0,
    channel=Bpod.OutputChannels.PWM1,
    #PulseWidthByte=255
)

sma.set_condition(2, 'GlobalTimer1', 1)

sma.add_state(
    state_name='Port2Light',
    state_timer=1,
    state_change_conditions={
        Bpod.Events.Tup:     'Port2Off', 
        Bpod.Events.Port1In: 'TriggerGlobalTimer'
    },
    output_actions=[(Bpod.OutputChannels.PWM2, 255)]
)

sma.add_state(
    state_name='Port2Off',
    state_timer=1,
    state_change_conditions={
        Bpod.Events.Tup: 'Port3Light', 
        'Condition2':    'Port3Light'
    }
)

sma.add_state(
    state_name='Port3Light',
    state_timer=1,
    state_change_conditions={
        Bpod.Events.Tup:     'exit', 
        Bpod.Events.Port1In: 'TriggerGlobalTimer'
    },
    output_actions=[(Bpod.OutputChannels.PWM3, 255)]
)

sma.add_state(
    state_name='TriggerGlobalTimer',
    state_timer=0,
    state_change_conditions={
        Bpod.Events.Tup:     'Port2Light',
    },
    output_actions=[('GlobalTimerTrig', 1)]
)

bpod.send_state_machine(sma)
bpod.run_state_machine(sma)

print("Current trial info: {0}".format(bpod.session.current_trial))
"""
bpod.close()
