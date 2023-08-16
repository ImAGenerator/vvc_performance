import os 
import re
from ..common.commonlib import file_subs, compile_VTM
from ..common import vvc_exec
from pathlib import Path
import yaml

class Simulation:
    cfg_dir = None
    vtm_dir = None
    out_dir = None

    version = 'Precise'
    qps = [22, 27, 32, 37]
    encoder = ['AI', 'RA', 'LB']

    n_frames = 32
    bg_exec = False

    videos = []

    def __init__(self, n_frames = 32, version = 'Precise', qps = [22, 27, 32, 37], encoder = ['AI', 'RA', 'LB']):
        self.set_n_frames(n_frames)
        self.set_version(version)
        self.set_qps(qps)
        self.set_encoder(encoder)
        self.enable_bg_exec()

    def read_yaml(self, yaml_file):
        with open(yaml_file) as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)

        cfg = data['cfg']
        vtm = data['vtm']
        out = data['out']
        self.set_paths(out, vtm, cfg)

    def run_exec(self):
        print('Execution running')
        self.get_exec_info()

        _exec = vvc_exec.vvc_executer(
            vtm_path    =   self.vtm_dir,
            version     =   self.version,
            n_frames    =   self.n_frames
        )
        _exec.bg_exec = self.bg_exec
        _exec.enable_display()
        _exec.set_output_path(self.out_dir)

        for video in self.videos:
            _exec.set_video_cfg(os.path.join(self.cfg_dir, video), Path(video).stem)
            for cfg in self.encoder:
                _exec.set_cfg(cfg)
                for qp in self.qps:
                    _exec.set_qp(qp)
                    _exec.run_exec()

        print('Simulation done')

    def get_exec_info(self, display=False):
        info = \
            f'---------------------------------------------- \n' + \
            f'out directory     {self.out_dir} \n'\
            f'vtm directory     {self.vtm_dir} \n'\
            f'cfg directory     {self.cfg_dir} \n'\
            f'---------------------------------------------- \n' + \
            f'\n' + \
            f'version :         {self.version} \n' + \
            f'qps :             {self.qps} \n' + \
            f'encoder :         {self.encoder} \n' + \
            f'n_frames :        {self.n_frames} \n' + \
            f'background exec : {self.bg_exec} \n' + \
            f'videos :          [ \n'
        for i, video in enumerate(self.videos):
            info += \
            f'                      {i:2}. {video}\n'
        info += f'                  ] \n' + \
                f'---------------------------------------------- \n'

        info += f'Total execution {len(self.videos)} x {len(self.qps)} x {len(self.encoder)} = {len(self.videos) * len(self.qps) * len(self.encoder)} simulations\n---------------------------------------------- \n'
        
        data = {
            'out_dir'   :self.out_dir,
            'vtm_dir'   :self.vtm_dir,
            'cfg_dir'   :self.cfg_dir,
            'version'   :self.version,
            'qps'       :self.qps,
            'encoder'   :self.encoder,
            'n_frames'  :self.n_frames,
            'bg_exec'   :self.bg_exec,
            'videos'    :self.videos[:],
        }

        if display:
            print(info)
        return data

    def append_video_to_buffer(self, file_name:str):
        if not file_name.endswith('.cfg'):
            raise Exception("file name must end with .cfg")
        
        if not os.path.isfile(file_name): 
            raise Exception("File not found")

        self.videos.append(file_name)

    def remove_video_from_buffer(self, file_index):
        try:
            del self.videos[file_index]
        except:
            raise Exception("invalid index type")
        
    def remove_video_from_buffer_by_name(self, file_name):
        try:
            i = self.videos.index(file_name)
            del self.videos[i]
        except :
            raise Exception("invalid index type")

    def change_version(self, new_version, old_file, new_file):
        self.set_version(new_version)
        self.replace_file(new_file, old_file)
       
    def set_paths(self, out_dir, vtm_dir, cfg_dir):
        self.set_out_dir(out_dir)
        self.set_vtm_dir(vtm_dir)
        self.set_cfg_dir(cfg_dir)

    def replace_file(self, new_file, old_file):
        file_subs(new_file, os.path.dirname(old_file), os.path.basename(old_file))
        compile_VTM(self.vtm_dir)

    def set_n_frames(self, n_frames):
        self.n_frames = n_frames
    
    def set_out_dir(self, out_dir):
        self.out_dir = self.__create_output_dir__(out_dir)

    def set_vtm_dir(self, vtm_dir):
        self.vtm_dir = vtm_dir

    def set_cfg_dir(self, cfg_dir):
        self.cfg_dir = cfg_dir
        self.videos = self.__config_files_in_dir__(cfg_dir)

    def set_version(self, version):
        self.version = version

    def set_qps(self, qps):
        self.qps = qps
    
    def set_encoder(self, encoder):
        self.encoder = encoder

    def enable_bg_exec(self):
        self.bg_exec = True
    
    def disable_bg_exec(self):
        self.bg_exec = False

    def __create_output_dir__(self, output_dir):
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        return output_dir

    def __config_files_in_dir__(self, cfg_vid_dir):
        if not os.path.isdir(cfg_vid_dir):
            raise Exception("Video config directory not exists")
        
        return [
            f 
            for f in os.listdir(cfg_vid_dir) 
            if os.path.isfile(os.path.join(cfg_vid_dir, f)) and 
            f[-4:] == '.cfg'
        ]
    
