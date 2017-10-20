# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Demonstration of AddTrialEvents used in a simple visual 2AFC session.
AddTrialEvents formats each trial's data in a human-readable struct, and adds to myBpod.data (to save to disk later)
Connect noseports to ports 1-3.

Example adapted from Josh Sanders' original version on Sanworks Bpod repository
"""
import random

from pybpodapi.bpod import Bpod
from pybpodapi.state_machine import StateMachine
from pybpodapi.bpod.hardware.events import EventName
from pybpodapi.bpod.hardware.output_channels import OutputChannel

import timeit, random, numpy as np, time
from toolsR import SoundR, VideoRP

# ---- camera ----
cam = VideoRP(0, path='/home/')
camOK = False
cam.play()

# Generate your sound arrays
toneDuration = 1  # sec
amplitude = 1.
FsOut = 44100  # sample rate, depend on the sound card
tvec = np.linspace(0, toneDuration, toneDuration * FsOut)
fs = 1000
s1 = amplitude * np.sin(2 * np.pi * fs * tvec)  # sound vector
s2 = np.zeros(s1.size)  # empty sound

# Create the sound server
soundStream = SoundR(sampleRate=FsOut, deviceOut=0)

# ------------------------------------------------------------------
# --------------- code to trig the sound
start = 0


def my_softcode_handler(data):
    global start, soundStream, timeit, cam, camOK
    print(data)
    if data == 55:
        print("----PLAY-----")
        soundStream.playSound()
        start = timeit.default_timer()
        if not camOK:
            cam.record()
            camOK = True
    elif data == 66:
        soundStream.stopSound()
        print(':::::::::Time to stop:::::::::', timeit.default_timer() - start)


# ------------------------------------------------------------------

START_APP = timeit.default_timer()

my_bpod = Bpod()

my_bpod.softcode_handler_function = my_softcode_handler

nTrials = 2

for i in range(nTrials):  # Main loop
    print('Trial: ', i + 1)

    sma = StateMachine(my_bpod)
    soundStream.load(s1)  # load the sound <-----------------

    sma.add_state(
        state_name='WaitForPort2Poke',
        state_timer=1,
        state_change_conditions={EventName.Tup: 'PlaySound'},
        output_actions=[(OutputChannel.PWM1, 255)])
    sma.add_state(
        state_name='PlaySound',
        state_timer=0.5,
        state_change_conditions={EventName.Tup: 'StopSound'},
        output_actions=[(OutputChannel.SoftCode, 55), (OutputChannel.Wire1, 5)])
    sma.add_state(
        state_name='StopSound',
        state_timer=1,
        state_change_conditions={EventName.Tup: 'Exit'},
        output_actions=[(OutputChannel.SoftCode, 66)])
    sma.add_state(
        state_name='Exit',
        state_timer=1,
        state_change_conditions={EventName.Tup: 'exit'},
        output_actions=[(OutputChannel.PWM1, 255)])  # Stop the sound

    my_bpod.send_state_machine(sma)  # Send state machine description to Bpod device

    my_bpod.run_state_machine(sma)  # Run state machine

    print("Current trial info: {0}".format(my_bpod.session.current_trial))

my_bpod.stop()
cam.stop()
print('EXECUTION TIME', timeit.default_timer() - START_APP)