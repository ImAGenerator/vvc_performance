import os

def cd(dir):
    return f'cd \"{dir}\"'

def gprof(enc, bin, out):
    inp = os.path.join(bin, 'gmon.out')
    return f'gprof \"{enc}\" \"{inp}\" >> \"{out}\"'

def join(commands):
    command = ''
    try:
        for cmd in commands[:-1]:
            command = command + cmd + ' && '
        command = command + commands[-1]
    except TypeError:
        raise Exception("The object must be iterable")
    except:
        raise Exception()
    return command
    
def vvc(encoder, cfg_enc:str, cfg_vid, bin_vid, qp, frames, output=None):
    if cfg_enc.endswith('encoder_intra_vtm.cfg'):
        ts = '-ts 1'
    else:
        ts = ''

    if output != None:
        output = '>> \"' + output + '\"'
    else:
        output = ''

    return f'/\"{encoder}\" ' + \
    f'-c \"{cfg_enc}\" ' + \
    f'-c \"{cfg_vid}\" ' + \
    f'-b \"{bin_vid}\" ' + \
    f'-q {qp} '+ \
    f'-f {frames} ' + \
    f'{ts} ' + \
    f'--SIMD=SCALAR ' + \
    f'{output}'
    
def mkdir_r(dir_list):
    c_dir = ''
    for d in dir_list:
        c_dir = os.path.join(c_dir, d)

        if not os.path.isdir(c_dir):
            os.mkdir(c_dir)

