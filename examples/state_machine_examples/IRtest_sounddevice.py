# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Demonstration of AddTrialEvents used in a simple visual 2AFC session.
AddTrialEvents formats each trial's data in a human-readable struct, and adds to myBpod.data (to save to disk later)
Connect noseports to ports 1-3.

Example adapted from Josh Sanders' original version on Sanworks Bpod repository
"""

import timeit, multiprocessing, random, numpy as np, examples.settings as settings, time

from pybpodapi.model.bpod import Bpod
from pybpodapi.model.state_machine import StateMachine
from pybpodapi.hardware.events import EventName
from pybpodapi.hardware.output_channels import OutputChannel


START_APP = timeit.default_timer()

def run():
	"""
	Run this protocol now
	"""

	my_bpod = Bpod().start(settings.SERIAL_PORT, settings.WORKSPACE_PATH, "test_soft_codes")  # Start bpod

	my_bpod.softcode_handler_function = my_softcode_handler

	nTrials = 20
	trialTypes = [1, 2]  # 1 (rewarded left) or 2 (rewarded right)

	for i in range(nTrials):  # Main loop
		print('Trial: ', i + 1)

		thisTrialType = random.choice(trialTypes)  # Randomly choose trial type
		if thisTrialType == 1:
			stimulus = OutputChannel.PWM1  # set stimulus channel for trial type 1
			leftAction = 'Reward'
			rightAction = 'Punish'
			rewardValve = 1
		elif thisTrialType == 2:
			stimulus = OutputChannel.PWM3  # set stimulus channel for trial type 1
			leftAction = 'Punish'
			rightAction = 'Reward'
			rewardValve = 3

		sma = StateMachine(my_bpod.hardware)

		sma.add_state(
			state_name='WaitForPort2Poke',
			state_timer=1,
			state_change_conditions={EventName.Port1In: 'PlaySound'},
			output_actions=[(OutputChannel.PWM1, 255)])
		sma.add_state(
			state_name='PlaySound',
			state_timer=1,
			state_change_conditions={EventName.Port1Out: 'StopSound'},
			output_actions=[(OutputChannel.SoftCode, 55)])
		sma.add_state(
			state_name='StopSound',
			state_timer=0.1,
			state_change_conditions={EventName.Tup: 'Exit'},
			output_actions=[(OutputChannel.SoftCode, 66)])
		sma.add_state(
			state_name='Exit',
			state_timer=0.1,
			state_change_conditions={EventName.Tup: 'exit'},
			output_actions=[(OutputChannel.PWM1, 255)])  # Stop the sound

		my_bpod.send_state_machine(sma)  # Send state machine description to Bpod device

		print("Waiting for poke. Reward: ", 'left' if thisTrialType == 1 else 'right')

		my_bpod.run_state_machine(sma)  # Run state machine

		print("Current trial info: {0}".format(my_bpod.session.current_trial()))

	my_bpod.stop()  # Disconnect Bpod
	print('EXECUTION TIME', timeit.default_timer()- START_APP)


# --------------- code to trig the sound
#import sounddevice as sd
#import numpy as np

#fs = 44100
#data = np.random.uniform(-1, 1, 44100*5)
#sound = np.int16(data / np.max(np.abs(data)) * 32767)
#sd.default.samplerate = fs
#sd.default.latency = ('low', 'low')
#sd.default.clip_off = True
#sd.default.dither_off = True
#sd.default.never_drop_input = True
#sd.default.prime_output_buffers_using_stream_callback = True
start = 0


class Consumer(multiprocessing.Process):
	
	def __init__(self, task_queue):
		multiprocessing.Process.__init__(self)
		self.task_queue   = task_queue
		
	def run(self):
		import sounddevice as sd

		fs = 44100
		data = np.random.uniform(-1, 1, 44100*5)
		sound = np.int16(data / np.max(np.abs(data)) * 32767)
		sd.default.samplerate = fs

		while True:
			next_task = self.task_queue.get()
			if next_task == 1:
				sd.play(sound, blocking=False) #the state has a duration of 0.1s so in this case the sound stops quickly 
			elif next_task == 0:
				sd.stop(ignore_errors=False)
			elif next_task == None:
				break
		return


tasks_queue = multiprocessing.JoinableQueue()

def my_softcode_handler(data):
	global start, sd, tasks_queue
	print(data)
	if data == 55:
		print("----PLAY-----")
		tasks_queue.put(1)
		start = timeit.default_timer()
	elif data == 66:
		tasks_queue.put(0)		
		print(':::::::::Time to stop:::::::::',timeit.default_timer() - start)


if __name__ == '__main__':
	consumer = Consumer(tasks_queue)
	consumer.start()
	settings.run_this_protocol(run)
	tasks_queue.put(None)
	time.sleep(1)
	#tasks_queue.join()
