from vvcpy import sim

vsim = sim.Simulation(
    n_frames=2,
    qps=[37],
    encoder=['RA'],
    bg_exec=True
)
vsim.read_yaml('setup.yaml')

videos = vsim.get_exec_info()['videos']
videos.remove('RaceHorses.cfg')

for video in videos:
    vsim.remove_video_from_buffer_by_name(video)

vsim.run_exec()