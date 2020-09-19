from pybpodapi.protocol import Bpod, StateMachine
my_bpod = Bpod(emulator_mode=True)
sma = StateMachine(my_bpod)
# Set global timer 1 for 3 seconds, following a 1.5 second onset delay after
# trigger. Link to channel BNC2.
sma.set_global_timer(timer_id=1, timer_duration=3,
                     on_set_delay=1.5, channel='BNC2')
sma.add_state(
    state_name='TimerTrig',  # Trigger global timer
    state_timer=0,
    state_change_conditions={Bpod.Events.Tup: 'Port1Lit'},
    output_actions=[(Bpod.OutputChannels.GlobalTimerTrig, 1)])
sma.add_state(
    # Infinite loop (with next state). Only a global timer can save us.
    state_name='Port1Lit',
    state_timer=.25,
    state_change_conditions={
        Bpod.Events.Tup: 'Port3Lit', 'GlobalTimer1_End': 'exit'},
    output_actions=[(Bpod.OutputChannels.PWM1, 255)])
sma.add_state(
    state_name='Port3Lit',
    state_timer=.25,
    state_change_conditions={
        Bpod.Events.Tup: 'Port1Lit', 'GlobalTimer1_End': 'exit'},
    output_actions=[(Bpod.OutputChannels.PWM3, 255)])
my_bpod.send_state_machine(sma)
my_bpod.run_state_machine(sma)
print("Current trial info: {0}".format(my_bpod.session.current_trial))
my_bpod.close()
