from ..common import commonlib as clib
import os

def create_env(sim_env: str):
    if os.path.exists(sim_env):
        raise Exception(f"{sim_env} already exists")
    
    os.mkdir(sim_env)

def create_run_queue():
    pass

