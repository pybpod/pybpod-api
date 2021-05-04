import random
import time
from pybpodapi.protocol import Bpod, StateMachine
from concurrent.futures import ThreadPoolExecutor
my_bpod = Bpod(emulator_mode=True)
nTrials = 5
graceTime = 5
port_numbers = [1, 2, 3]
trialTypes = [1, 2]  # 1 (rewarded left) or 2 (rewarded right)
for i in range(nTrials):  # Main loop
    print('Trial: ', i + 1)
    thisTrialType = random.choice(trialTypes)  # Randomly choose trial type
    if thisTrialType == 1:
        # set stimulus channel for trial type 1
        stimulus = Bpod.OutputChannels.PWM1
        leftAction = 'Reward'
        rightAction = 'Punish'
        rewardValve = 1
    elif thisTrialType == 2:
        # set stimulus channel for trial type 1
        stimulus = Bpod.OutputChannels.PWM3
        leftAction = 'Punish'
        rightAction = 'Reward'
        rewardValve = 3
    sma = StateMachine(my_bpod)
    sma.set_global_timer_legacy(
        timer_id=1, timer_duration=graceTime)  # Set timeout
    sma.add_state(
        state_name='WaitForPort2Poke',
        state_timer=1,
        state_change_conditions={Bpod.Events.Port2In: 'FlashStimulus'},
        output_actions=[('PWM2', 255)])
    sma.add_state(
        state_name='FlashStimulus',
        state_timer=0.1,
        state_change_conditions={Bpod.Events.Tup: 'WaitForResponse'},
        output_actions=[(stimulus, 255),
                        (Bpod.OutputChannels.GlobalTimerTrig, 1)])
    sma.add_state(
        state_name='WaitForResponse',
        state_timer=1,
        state_change_conditions={Bpod.Events.Port1In: leftAction,
                                 Bpod.Events.Port3In: rightAction,
                                 Bpod.Events.Port2In: 'Warning',
                                 Bpod.Events.GlobalTimer1_End: 'MiniPunish'},
        output_actions=[])
    sma.add_state(
        state_name='Warning',
        state_timer=0.1,
        state_change_conditions={Bpod.Events.Tup: 'WaitForResponse',
                                 Bpod.Events.GlobalTimer1_End: 'MiniPunish'},
        output_actions=[(Bpod.OutputChannels.LED, 1),
                        (Bpod.OutputChannels.LED, 2),
                        (Bpod.OutputChannels.LED, 3)])  # Reward correct choice
    sma.add_state(
        state_name='Reward',
        state_timer=0.1,
        state_change_conditions={Bpod.Events.Tup: 'exit'},
        # Reward correct choice
        output_actions=[(Bpod.OutputChannels.Valve, rewardValve)])
    sma.add_state(
        state_name='Punish',
        state_timer=3,
        state_change_conditions={Bpod.Events.Tup: 'exit'},
        # Signal incorrect choice
        output_actions=[(Bpod.OutputChannels.LED, 1),
                        (Bpod.OutputChannels.LED, 2),
                        (Bpod.OutputChannels.LED, 3)])
    sma.add_state(
        state_name='MiniPunish',
        state_timer=1,
        state_change_conditions={Bpod.Events.Tup: 'exit'},
        # Signal incorrect choice
        output_actions=[(Bpod.OutputChannels.LED, 1),
                        (Bpod.OutputChannels.LED, 2),
                        (Bpod.OutputChannels.LED, 3)])
    # Send state machine description to Bpod device
    my_bpod.send_state_machine(sma)
    print("Waiting for poke. Reward: ",
          'left' if thisTrialType == 1 else 'right')

    def mouse(data):
        time.sleep(3)
        my_bpod.manual_override(Bpod.ChannelTypes.INPUT, 'Port',
                                channel_number=2,
                                value=12)
        time.sleep(2)
        my_bpod.manual_override(Bpod.ChannelTypes.INPUT, 'Port',
                                channel_number=random.choice(port_numbers),
                                value=12)

    executor = ThreadPoolExecutor(max_workers=1)
    executor.submit(mouse, None)

    my_bpod.run_state_machine(sma)  # Run state machine
    print("Current trial info: {0}".format(my_bpod.session.current_trial))
my_bpod.close()  # Disconnect Bpod
