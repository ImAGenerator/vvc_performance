import pandas as pd
from pprint import pprint
import os
from .vvc_output import VVC_Output
from .vvc_bd_rate import BD_Rate
from ..common import log_path

def vvc_frame_analysis(versions, file_names, path, cfgs, qps, all_frames = False):
    
    files = file_names

    df = BD_Rate()
    df.index.names=['version','video','cfg','frame']
    for version in versions:
        for file in files:    
            for cfg in cfgs:
                path_logs = log_path.vvc_log_path(path, cfg, file, version, qps, multiqp=True)
                for p in path_logs:
                    if not os.path.isfile(p):
                        continue
                
                path_refs = log_path.vvc_log_path(path, cfg, file, 'Precise', qps, multiqp=True)
                for p in path_refs:
                    if not os.path.isfile(p):
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
    
