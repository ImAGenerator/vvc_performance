import os
import re
from os.path import isfile, isdir, join
from pathlib import Path
import numpy as np
from scipy import integrate, interpolate
import math
import yaml

def file_subs(file_path, destiny_dir, rename_like) -> None:
    if isfile(file_path):
        source_path = f'{file_path}'
    else:   
        raise Exception("invalid file path!")
    
    if isdir(destiny_dir):
        destiny_path = f'{destiny_dir}'
    else:   
        raise Exception("Destiny is not a directory!")

    os.system(f"cp \"{source_path}\" \"{os.path.join(destiny_path, rename_like)}\"") 


def get_next_file(exec_buffer, erase = True):
    # reads the first line, then, if erase is on, erases the line read
    if not os.path.isfile(exec_buffer):
        raise FileNotFoundError()

    with open(exec_buffer, 'r') as f:
        file = f.readline()
        if file.endswith('\n'):
            file = file[:-1]
        if erase:
            with open(exec_buffer + 'temp', 'w') as out:
                for line in f:
                    out.write(line)
                out.close()
        f.close()
    
    if erase:
        os.remove(exec_buffer)
        os.system(f"mv {exec_buffer + 'temp'} {exec_buffer}")

    return file

def compile_VTM(vtm_path):
    build_dir = join(vtm_path, "build")
    if not os.path.isdir(build_dir):
        os.mkdir(build_dir)

    cmake_file = join(build_dir, 'CMakeCache.txt')

    os.system(f'cd \"{build_dir}\" && cmake \"{vtm_path}\" -DCMAKE_BUILD_TYPE=Release')
    turn_on_profiling_in_makefile(cmake_file)

    os.system(f'cd \"{build_dir}\" && make')
    

def create_exec_buffer(output_dir='.',output_name='.execution_buffer', dir_path='.', extension:str='.cpp'):
    files_list = [str(f) for f in Path(dir_path).rglob('*'+extension)]

    with open(os.path.join(output_dir, output_name), 'w') as f:
        for file in files_list:
            f.write(file + '\n')
        f.close()

def change_expression_in_file(file, expression, change_to):
    temp_file_name = ".swp_" + file
    while os.path.isfile(temp_file_name):
        temp_file_name = temp_file_name + '_'
    
    t = open (temp_file_name, 'w') 
    f = open(file, 'r')
    
    line = f.read()
    if len(re.findall(expression, line)) > 0:
        matches = re.finditer(expression, line, re.M)
        for match in matches:
            t.write(f'{line[:match.start()]}{change_to}{line[match.end():]}')
    else:
        t.write(line)                
    f.close()
    t.close()

    os.remove(file)
    os.rename(temp_file_name, file)


def turn_on_profiling_in_makefile(file):   
    if not os.path.isfile(file):
        raise Exception(f"File {file} does not exists")
    with open(file) as f:
        txt = f.read()
        f.close()

    src = 'CMAKE_CXX_FLAGS_RELEASE:STRING=-O3 -DNDEBUG'
    dst = 'CMAKE_CXX_FLAGS_RELEASE:STRING=-O3 -DNDEBUG -pg'

    txt = re.sub(src, dst, txt)

    src = 'CMAKE_CXX_FLAGS_RELWITHDEBINFO:STRING=-O2 -g -DNDEBUG'
    dst = 'CMAKE_CXX_FLAGS_RELWITHDEBINFO:STRING=-O2 -g -DNDEBUG -pg'

    txt = re.sub(src, dst, txt)

    with open(file, 'w') as f:
        f.write(txt)
        f.close()

def read_config_file(filename: str):
    with open(filename, 'r') as f:
        data = {
            "vtm_dir": f.readline().replace('\n', ''),
            "cfg_dir": f.readline().replace('\n', ''),
            "out_dir": f.readline().replace('\n', '')
        }
        f.close()
    print(data)
    
    if not os.path.isdir(data['vtm_dir']):
        raise Exception("vtm_dir is not a directory")
    elif not os.path.isdir(data['cfg_videos_dir']):
        raise Exception("cfg_videos_dir is not a directory")
    else:
        return data
    
def list_gprof_logs_in_dir(dir:str)->list:
    return [str(f) for f in Path(dir).rglob('*.gplog')]

def list_vtm_logs_in_dir(dir:str)->list:
    return [str(f) for f in Path(dir).rglob('*.vvclog')]

def verify_vtm_path(vtm_path):
    if not os.path.isdir(vtm_path):
        raise FileNotFoundError("VTM path is not a directory")
    if not os.path.isdir(os.path.join(vtm_path, 'bin')):
        raise FileNotFoundError("bin folder not found at VTM folder")
    if not os.path.isdir(os.path.join(vtm_path, 'source')):
        raise FileNotFoundError("source folder not found at VTM folder")
    if not os.path.isdir(os.path.join(vtm_path, 'cfg')):
        raise FileNotFoundError("cfg folder not found at VTM folder")

def find_all_versions_in_path(path):
    vvc_log_path = os.path.join(path, 'vvc_log')
    if os.path.isdir(vvc_log_path):
        return list(os.listdir(vvc_log_path))
    else:
        return []
    
def find_all_videos_in_version(path, version):
    vvc_log_path = os.path.join(path, 'vvc_log', version)

    if os.path.isdir(vvc_log_path):
        return list(os.listdir(vvc_log_path))
    else:
        return []
    
def yaml_reader(yaml_file, key=''):
    with open(yaml_file) as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        f.close()
    if key == '':
        return data
    else:
        try:
            return data[key]
        except:
            raise Exception(f'Key \"{key}\" not found')
        
def bdr_calc(cmp, ref):
    if len(cmp['bitrate']) != len(ref['bitrate']):
        return None

    cmp = np.asarray(cmp.loc[:,'bitrate':'YUV_PSNR'])
    ref = np.asarray(ref.loc[:,'bitrate':'YUV_PSNR'])

    ref = ref[ref[:,0].argsort()]
    cmp = cmp[cmp[:,0].argsort()]

    xa, ya = np.log10(ref[:,0]), ref[:,4]
    xb, yb = np.log10(cmp[:,0]), cmp[:,4]
    
    max_i = len(ya)
    i = 1
    while(i < max_i):
        if ya[i] < ya[i-1] or yb[i] <  yb[i-1]:
            ya = np.delete( ya,i)
            yb = np.delete( yb,i)
            xa = np.delete( xa,i)
            xb = np.delete( xb,i)
            max_i = len(ya)
        else:
            i += 1

    x_interp = [max(min(xa), min(xb)), min(max(xa),max(xb))]
    y_interp = [max(min(ya), min(yb)), min(max(ya),max(yb))]

    interp_br_a = interpolate.PchipInterpolator(ya,xa)
    interp_br_b = interpolate.PchipInterpolator(yb,xb)

    bdbr_a = integrate.quad(interp_br_a, y_interp[0], y_interp[1])[0]
    bdbr_b = integrate.quad(interp_br_b, y_interp[0], y_interp[1])[0]

    bdbr = (bdbr_b - bdbr_a) / (y_interp[1] - y_interp[0])
    bdbr = (math.pow(10., bdbr)-1)*100

    return bdbr
