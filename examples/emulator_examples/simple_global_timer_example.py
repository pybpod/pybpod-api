from pybpodapi.protocol import Bpod, StateMachine
my_bpod = Bpod(emulator_mode=True)
sma = StateMachine(my_bpod)
# Set global timer 1 for 5 seconds
sma.set_global_timer(timer_id=1, timer_duration=5)
sma.add_state(
    state_name='state1',
    state_timer=1,
    state_change_conditions={Bpod.Events.Tup: 'state2'},
    output_actions=[(Bpod.OutputChannels.GlobalTimerTrig, 1)])
for i in range(2, 10):
    sma.add_state(
        state_name=f'state{i}',
        state_timer=0.2,
        state_change_conditions={Bpod.Events.Tup: f'state{i+1}'},
        output_actions=[])
# The next one shouldn't fire except after 15 seconds
sma.add_state(
    state_name='state10',
    state_timer=0,
    state_change_conditions={Bpod.Events.GlobalTimer1_End: 'exit'},
    output_actions=[])
my_bpod.send_state_machine(sma)
my_bpod.run_state_machine(sma)
my_bpod.close()
