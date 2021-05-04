import time
from pybpodapi.protocol import Bpod, StateMachine
from concurrent.futures import ThreadPoolExecutor
my_bpod = Bpod(emulator_mode=True)
sma = StateMachine(my_bpod)
sma.add_state(
    state_name='Port1Light',
    state_timer=0,
    # Go to Port2Light when byte 0x3 arrives on UART port 2
    state_change_conditions={Bpod.Events.Serial2_3: 'Port2Light'},
    output_actions=[(Bpod.OutputChannels.PWM1, 255)])
sma.add_state(
    state_name='Port2Light',
    state_timer=0,
    state_change_conditions={Bpod.Events.Tup: 'exit'},
    output_actions=[(Bpod.OutputChannels.PWM2, 255)])
my_bpod.send_state_machine(sma)


def worker(data):
    time.sleep(5)
    my_bpod.trigger_event_by_name(Bpod.Events.Serial2_3)


executor = ThreadPoolExecutor(max_workers=1)
executor.submit(worker, None)

my_bpod.run_state_machine(sma)
print("Current trial info: ", my_bpod.session.current_trial)
my_bpod.close()
