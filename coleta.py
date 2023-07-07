import vvcpy as vp 

vtm_dir = '/home/dudabosel/TCC/TCC/'
cfg_dir = '/home/dudabosel/TCC/configs/'
out_dir = '/home/dudabosel/TCC/output'

encoder = ['AI']
qps = [22,27,32,37]

sim = vp.sim.Simulation(n_frames=60, qps=qps, encoder=encoder, bg_exec=False)
sim.set_paths(out_dir, vtm_dir, cfg_dir)

sim.run_exec()