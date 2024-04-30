import vvcpy as vp 

vtm_dir = '/home/ebbosel/TCC/TCC/' #'/home/dudabosel/TCC/TCC/'
cfg_dir = '/home/ebbosel/TCC/configs/' #'/home/dudabosel/TCC/configs/'
out_dir = '/home/ebbosel/TCC/output' #'/home/dudabosel/TCC/output'

encoder = ['AI']
qps = [32]

sim = vp.sim.Simulation(n_frames=60, qps=qps, encoder=encoder, bg_exec=True)
sim.set_paths(out_dir, vtm_dir, cfg_dir)

#new_file = '/home/ebbosel/TCC/aproximacoes/RdCost(8x8)-3.cpp'
#old_file = '/home/ebbosel/TCC/TCC/source/Lib/CommonLib/RdCost.cpp'

#sim.change_version("RdCost(8x8)-3", old_file, new_file)

sim.run_exec()
