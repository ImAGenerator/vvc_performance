from .app import vvc_performance as vp 

sim = vp.Simulation(
    n_frames=32, 
    encoder=['RA', 'AI'], 
    qps=[22, 27, 32, 37], 
    bg_exec=True
)

sim.get_exec_info()