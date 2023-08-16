from ..common import commonlib as clib
import os


class Execution_environment():
    __queue_name__ = '.__execution_queue'
    __cache_name__ = '.__vvcpycache'

    def __init__(self, sim_env:str):
        if not os.path.isabs(sim_env):
            sim_env = os.path.join(os.getcwd(), sim_env)
        
        if not os.path.exists(self.cache):
            self.create_env(sim_env)
        else:
            self.load_env(sim_env)

    def create_env(self, sim_env: str):
        if os.path.exists(sim_env):
            raise Exception(f"{sim_env} already exists")
        
        os.mkdir(sim_env)
        self.sim_env = sim_env
        
    def create_run_queue(self, modifs_path: str):
        self.queue = clib.create_exec_buffer(self.sim_env, self.queue_name, dir_path=modifs_path)

    def __make_cache(self):
        self.cache = os.path.join(sim_env, self.__cache_name__)
    def __make_cache(self):
        self.queue = os.path.join(sim_env, self.__queue_name__)

    def load_env(self, sim_env):
        self.sim_env = sim_env
        self.__make_cache()
        self.__make_queue()

    def get_next_execution(self):
        return clib.get_next_file(self.queue)

    
        

