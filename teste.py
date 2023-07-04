import vvcpy as vp 

sim = vp.sim.Simulation(
    n_frames=32, 
    encoder=['RA'], 
    qps=[37], 
    bg_exec=True
)

yaml_file = 'setuphome.yaml'
sim.read_yaml(yaml_file)

sim.get_exec_info()