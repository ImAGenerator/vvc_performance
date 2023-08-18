from . import commonlib as clib
import os
import yaml


class Vvc_environment():
    __queue_name__ = '.__execution_queue'
    __cache_name__ = '.__vvcpycache.yaml'
    __queue_on__ = False
    __setup_set__ = False

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
        self.__make_cache()
        self.__init_cache()

    def read_setup_file(self, setup_file : str):
        if not os.path.isfile(setup_file):
            raise Exception(f'File {setup_file} not found')
        elif not setup_file.endswith('.yaml'):
            raise Exception(f'{setup_file} is not a \'.yaml\' file')
        
        self.__setup_set__ = True
        self.setup = setup_file
        self.write_cache('setup_set', 'True')
        self.write_cache('setup', setup_file)
        
    def create_run_queue(self, modifs_path: str):
        self.__make_queue()
        self.queue = clib.create_exec_buffer(self.sim_env, self.queue, dir_path=modifs_path)
        self.__queue_on__ = True
        self.write_cache('queue_on', 'True')
        self.write_cache('queue', self.queue)

    def __make_cache(self):
        self.cache = os.path.join(self.sim_env, self.__cache_name__)
    
    def __make_queue(self):
        self.queue = os.path.join(self.sim_env, self.__queue_name__)
    
    def __load_setup(self):
        data = self.read_cache()
        if data['setup_set'] == 'True':
            self.setup = self.read_cache()['setup']

    def __load_queue(self):
        data = self.read_cache()
        if data['queue_on'] == 'True':
            self.read_cache('queue')

    def load_env(self, sim_env):
        self.sim_env = sim_env
        self.__make_cache()
        self.__load_queue()
        self.__load_setup()
        
    def get_next_execution(self):
        return clib.get_next_file(self.queue)
    
    def read_cache(self, key=''):
        data = clib.yaml_reader(self.cache)
        if key == '':
            return data
        else:
            try:
                return data[key]
            except:
                raise Exception()

    def write_cache(self, key, data):
        yaml_string = yaml.dump()
        yaml_string[key] = data
        with open(self.cache, 'r') as f:
            f.write(yaml_string)
            f.close()
        
    def __init_cache(self):
        self.__queue_on__ = False
        self.write_cache('queue_on', 'False')
        self.__setup_set__ = False
        self.write_cache('setup_set', 'False')





    
        

