from vvc_performance import Simulation

sim = Simulation(
    n_frames=32, 
    encoder=['RA', 'AI'], 
    qps=[22, 27, 32, 37], 
    bg_exec=True
)

sim.get_exec_info()