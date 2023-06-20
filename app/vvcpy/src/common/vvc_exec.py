import os
from . import csys
from .commonlib import verify_vtm_path
from .log_path import vvc_log_path, gprof_log_path, bin_folder_path, create_path_to_log, get_video_identifier

class vvc_executer:
    def __init__(self, vtm_path=None, video=None, video_cfg=None, cfg='AI', qp=22, version='Precise', n_frames=32):
        self.ts_status = ''
        
        self.set_cfg(cfg)
        self.set_qp(qp)
        self.set_version(version)
        
        if video_cfg != None and video != None:
            self.set_video_cfg(video_cfg, video)
        if vtm_path != None:
            self.set_vtm_path(vtm_path)

        self.n_frames = n_frames
        self.display = True
        self.bg_exec = False

    def run_exec(self):
        self.bin_encoder_path = os.path.join(self.bin_dir, 'EncoderAppStatic')
        self.cfg_encoder_path = os.path.join(self.cfg_dir, self.cfg_enc)

        self.update_config()
        self.update_paths()

        self.bin_videos_path  = os.path.join(self.output_bin_video_path, self.video+'.bin')

        cmd = self.__create_command__()
        os.system(cmd)
        print(cmd)

        if self.display:
            self.__display_info__()

    def set_video_params(self, video, cfg, qp, version):
        self.__set_video_identifier__(video, cfg, qp, version)
        self.video = video
        self.set_cfg(cfg)
        self.qp = qp
        self.version = version

    def set_vtm_path(self, vtm_path:str):
        verify_vtm_path(vtm_path)
        self.vtm_path = vtm_path
        self.cfg_dir = os.path.join(vtm_path, 'cfg')
        self.bin_dir = os.path.join(vtm_path, 'bin')
    
    def set_version(self, version:str):
        self.version = version

    def set_output_path(self, output_path:str):
        self.output_path = output_path
        
    def __enable_output_in_ext_file__(self):
        
        try:
            create_path_to_log(self.output_path, self.version, self.video, self.cfg, self.qp)
            
            self.output_vvc_log_path = vvc_log_path(
                self.output_path, self.cfg, self.video, self.version, self.qp, False
            )
            
            self.output_gprof_log_path = gprof_log_path(
                self.output_path, self.cfg, self.video, self.version, self.qp, False
            )

            self.output_bin_video_path = bin_folder_path(
                self.output_path, self.cfg, self.video, self.version, self.qp, False
            )

        except AttributeError:
            raise Exception("Output path not defined")        

    def set_video_cfg(self, video_cfg:str, video_name:str):
        self.video_cfg = video_cfg
        self.video = video_name

    def set_cfg(self, cfg):
        cfg_dict = {
            'AI': 'encoder_intra_vtm.cfg',
            'LB': 'encoder_lowdelay_vtm.cfg',
            'RA': 'encoder_randomaccess_vtm.cfg',
        }
        self.cfg = cfg
        self.cfg_enc = cfg_dict[cfg]
        if cfg == 'AI':
            self.ts_status = '-ts 1'

    def set_qp(self, qp):
        self.qp = qp

    def update_config(self):
        self.__set_video_identifier__(self.video, self.cfg, self.qp, self.version)
    
    def update_paths(self):
        self.__enable_output_in_ext_file__()

    def enable_display(self):
        self.display = True

    def disable_display(self):
        self.display = False

    def enable_bg_exec(self):
        self.bg_exec = True

    def disable_bg_exec(self):
        self.bg_exec = False
    
    def __create_command__(self):
        command = csys.vvc(
            self.bin_encoder_path,
            self.cfg_encoder_path,
            self.video_cfg,
            self.bin_videos_path,
            self.qp,
            self.n_frames,
            output=self.output_vvc_log_path
        )
        command = csys.join([
            csys.cd(self.output_bin_video_path),
            command, 
            csys.cd(self.bin_dir),
            csys.gprof(self.bin_encoder_path, self.output_bin_video_path, self.output_gprof_log_path)
        ])
            
        if self.bg_exec:
            command = command + ' & '
        return command
            
    def __set_video_identifier__(self, video, cfg, qp, version):
        self.video_identifier = get_video_identifier(video, cfg, qp, version)

    def __display_info__(self):
        print()
        print(f'Encoding: ........... {self.video}')
        print()
        print(f'Video identifier: ... {self.video_identifier}')
        print(f'Video config: ....... {self.video_cfg}')
        print(f'Encoder: ............ {self.cfg}')
        print(f'QP: ................. {self.qp}')
        print(f'VTM version used: ... {self.version}')
        print(f'frames encoded: ..... {self.n_frames}')
        print()

