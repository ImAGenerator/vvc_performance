import os
from . import csys

decod_log_type = {
    'gprof': {'ext': '.gplog', 'folder': 'gprof_log'},
    'vvc': {'ext': '.vvclog', 'folder': 'vvc_log'},
    'bin': {'ext': '', 'folder': 'video_bin'}
}

def create_path_to_log(path, version, video, cfg, qp):
    csys.mkdir_r([path, 'vvc_log',   version, video, cfg])
    csys.mkdir_r([path, 'gprof_log', version, video, cfg])
    csys.mkdir_r([path, 'video_bin', version, video, cfg, f'QP{qp}'])

def get_video_identifier(video, cfg, qp, version):
    return f'{video}_qp{qp}_{cfg}_{version}'

def gprof_log_path(path, cfg, file, version, qps, multiqp=False):
    return __ext_make_path__(path, cfg, file, version, qps, 'gprof', multiqp)

def vvc_log_path(path, cfg, file, version, qps, multiqp=False):
    return __ext_make_path__(path, cfg, file, version, qps, 'vvc', multiqp)

def bin_folder_path(path, cfg, file, version, qps, multiqp=False):
    f = __ext_make_folder__(path, cfg, file, version, 'bin')
    if multiqp:
        return [f+str(qp) for qp in qps]
    else:
        return f+str(qps)

def __ext_make_path__(path, cfg, file, version, qps, log_type, multiqp=False):
    if multiqp:
        return __ext_make_path_multifile__(path, cfg, file, version, qps, log_type)
    else:
        return __ext_make_path_file__(path, cfg, file, version, qps, log_type)
    
def __ext_make_folder__(path, cfg, file, version, log_type):
    return __ext_make_path_folder__(path, cfg, file, version, log_type)
        
def __ext_make_path_multifile__(path, cfg, file, version, qps, log_type):
    f = []
    for qp in qps:
        temp_file = __ext_make_path_file__(path, cfg, file, version, qp, log_type)
        f.append(temp_file)
    return f

def __ext_make_path_folder__(path, cfg, file, version, log_type):
    return os.path.join(
        path, 
        f'{decod_log_type[log_type]["folder"]}',
        version, 
        file, 
        cfg,
    )

def __ext_make_path_file__(path, cfg, file, version, qp, log_type):

    return os.path.join(
        __ext_make_path_folder__(path, cfg, file, version, log_type),
        'log_' + get_video_identifier(file, cfg, qp, version) + decod_log_type[log_type]["ext"]
    )
