import time
from pybpodapi.protocol import Bpod, StateMachine
from concurrent.futures import ThreadPoolExecutor
my_bpod = Bpod(emulator_mode=True)
sma = StateMachine(my_bpod)
sma.set_global_counter(counter_number=1, target_event='Port1In', threshold=5)
sma.add_state(
    state_name='InitialDelay',
    state_timer=2,
    state_change_conditions={Bpod.Events.Tup: 'ResetGlobalCounter1'},
    output_actions=[(Bpod.OutputChannels.PWM2, 255)])
sma.add_state(
    state_name='ResetGlobalCounter1',
    state_timer=0,
    state_change_conditions={Bpod.Events.Tup: 'Port1Lit'},
    output_actions=[(Bpod.OutputChannels.GlobalCounterReset, 1)])
sma.add_state(
    # Infinite loop (with next state). Only a global counter can save us.
    state_name='Port1Lit',
    state_timer=.25,
    state_change_conditions={
        Bpod.Events.Tup: 'Port3Lit', 'GlobalCounter1_End': 'exit'},
    output_actions=[(Bpod.OutputChannels.PWM1, 255)])
sma.add_state(
    state_name='Port3Lit',
    state_timer=.25,
    state_change_conditions={
        Bpod.Events.Tup: 'Port1Lit', 'GlobalCounter1_End': 'exit'},
    output_actions=[(Bpod.OutputChannels.PWM3, 255)])
my_bpod.send_state_machine(sma)


def mouse(data):
    time.sleep(1)
    for _ in range(5):
        time.sleep(1)
        my_bpod.manual_override(Bpod.ChannelTypes.INPUT, 'Port',
                                channel_number=1, value=12)


executor = ThreadPoolExecutor(max_workers=1)
executor.submit(mouse, None)

my_bpod.run_state_machine(sma)
print("Current trial info: {0}".format(my_bpod.session.current_trial))
my_bpod.close()
