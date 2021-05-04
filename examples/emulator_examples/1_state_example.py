from pybpodapi.protocol import Bpod, StateMachine
my_bpod = Bpod(emulator_mode=True)
sma = StateMachine(my_bpod)
sma.add_state(
    state_name='myState',
    state_timer=1,
    state_change_conditions={Bpod.Events.Tup: 'exit'},
    output_actions=[])
my_bpod.send_state_machine(sma)
my_bpod.run_state_machine(sma)
