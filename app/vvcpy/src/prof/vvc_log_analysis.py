import pandas as pd
from pprint import pprint
import os
from .vvc_output import VVC_Output
from .vvc_bd_rate import BD_Rate
from ..common import log_path
from ..common.commonlib import (
    find_all_versions_in_path,
    find_all_videos_in_version
)

def bd_rate_calculation(path:str, cfgs=['AI', 'LB', 'RA'], qps=[22, 27, 32, 37], all_frames=False) -> BD_Rate:
    if not os.path.isdir(path):
        raise Exception(f"{path} is not a directory")
    
    versions = find_all_versions_in_path(path)
    if not 'Precise' in versions:
        raise Exception(f"There is no Precise version in path")
    versions.remove('Precise')
    
    videos = find_all_videos_in_version(path, 'Precise')

    return vvc_frame_analysis(
        versions=versions, 
        file_names=videos,
        path=path,
        cfgs=cfgs,
        qps=qps,
        all_frames=all_frames
    )

def vvc_frame_analysis(versions, file_names, path, cfgs, qps, all_frames = False):
    
    files = file_names

    df = BD_Rate()
    df.index.names=['version','video','cfg','frame']
    for version in versions:
        for file in files:    
            for cfg in cfgs:
                skip = False
                path_logs = log_path.vvc_log_path(path, cfg, file, version, qps, multiqp=True)
                for p in path_logs:
                    if not os.path.isfile(p):
                        print('file not found = {}'.format(p))
                        skip = True
                
                path_refs = log_path.vvc_log_path(path, cfg, file, 'Precise', qps, multiqp=True)
                for p in path_refs:
                    if not os.path.isfile(p):
                        print('file not found = {}'.format(p))
                        skip = True

                if skip:
                    continue

                log = VVC_Output()
                log = log.read_multifile(path_logs, qps, all_frames)
                log = (VVC_Output(data=log.sort_values(by=['frame', 'qp'])))
                
                ref = VVC_Output()
                ref = ref.read_multifile(path_refs, qps, all_frames)
                ref = (VVC_Output(data=ref.sort_values(by=['frame', 'qp'])))

                tmp_df = BD_Rate(version=version, video=file, cfg=cfg)
                tmp_df.calc_bdbr(log, ref)

                df.append_bd(tmp_df)
    return df
    
