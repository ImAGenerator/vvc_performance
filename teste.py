import vvcpy as vp 

cfg = '/mnt/c/Users/dudup/OneDrive/Documentos/GitHub/VVC_research/database/input_analyser/cfg-files/'
vtm = '/mnt/c/Users/dudup/OneDrive/Documentos/GitHub/VVCSoftware_VTM/'
out = '/mnt/c/Users/dudup/OneDrive/Documentos/GitHub/vvc_performance/test_output/'

sim = vp.sim.Simulation(
    n_frames=32, 
    encoder=['RA'], 
    qps=[37], 
    bg_exec=True
)

sim.set_paths(out, vtm, cfg)

for i in range(8):
    sim.remove_video_from_buffer(0)

sim.get_exec_info()
sim.run_exec()

