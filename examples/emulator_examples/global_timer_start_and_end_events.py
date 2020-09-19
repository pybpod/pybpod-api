from pybpodapi.protocol import Bpod, StateMachine
my_bpod = Bpod(emulator_mode=True)
sma = StateMachine(my_bpod)
# Set global timer 1 for 3 seconds, following a 1.5 second onset delay after
# trigger. Link to LED of port 2.
sma.set_global_timer(timer_id=1, timer_duration=3, on_set_delay=1.5,
                     channel=Bpod.OutputChannels.PWM2, on_message=255)
sma.add_state(
    state_name='TimerTrig',  # Trigger global timer
    state_timer=0,
    state_change_conditions={Bpod.Events.Tup: 'Port1Lit_Pre'},
    output_actions=[('GlobalTimerTrig', 1)])
sma.add_state(
    state_name='Port1Lit_Pre',
    state_timer=.25,
    state_change_conditions={Bpod.Events.Tup: 'Port3Lit_Pre',
                             Bpod.Events.GlobalTimer1_Start: 'Port1Lit_Post'},
    output_actions=[(Bpod.OutputChannels.PWM1, 16)])
sma.add_state(
    state_name='Port3Lit_Pre',
    state_timer=.25,
    state_change_conditions={Bpod.Events.Tup: 'Port1Lit_Pre',
                             Bpod.Events.GlobalTimer1_Start: 'Port3Lit_Post'},
    output_actions=[(Bpod.OutputChannels.PWM3, 16)])
sma.add_state(
    state_name='Port1Lit_Post',
    state_timer=.25,
    state_change_conditions={
        Bpod.Events.Tup: 'Port3Lit_Post',
        Bpod.Events.GlobalTimer1_End: 'exit'},
    output_actions=[(Bpod.OutputChannels.PWM1, 255)])
sma.add_state(
    state_name='Port3Lit_Post',
    state_timer=.25,
    state_change_conditions={
        Bpod.Events.Tup: 'Port1Lit_Post',
        Bpod.Events.GlobalTimer1_End: 'exit'},
    output_actions=[(Bpod.OutputChannels.PWM3, 255)])
my_bpod.send_state_machine(sma)
my_bpod.run_state_machine(sma)
print("Current trial info: {0}".format(my_bpod.session.current_trial))
my_bpod.close()
