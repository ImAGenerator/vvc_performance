# Introduction:

This software will help researchers that want to make changes in the VVC Software and run the simulation for a set of videos using a set of different parameters.

# Parameters:

`n_frames` : represent the number of frames that must be encoded for each situation

`version` : the name of the VVC Software version. It is used to distinguish different executions of the simulations.

_example:_ if you want to change some of the Affine methods, you could call `version = "affineModified"`.

`qps` : represent the quantization parameters that will be used to encode the video.

_example:_ will repeat the simulation using each of this quantization parameters.

```py
qp = [22, 27, 32, 37]
```

`encoder` : indicates the encoder configurations that will be used on the encoding process. The encoder configurations available are:

| mnemonic | encoder       |
| -------- | ------------- |
| `AI`   | All Intra     |
| `RA`   | Random Access |
| `LB`   | Low Delay B   |

_example:_ will repeat the simulation using each of this configuration parameters.

```py
qp = ['AI', 'RA', 'LB']
```

`bg_exec` : if it is on, then the simulation will run in background

`cfg_dir` : is the location to the videos configuration files, that must contain informations about the video that should be encoded.

`vtm_dir` : is the location to the vtm main directory.

`out_dir` : is the location where the output files will be generated, such as vvc logs and gprof logs.

# Usage examples

## Creating a simple "Precise" version simulation

```py
import vvcpy as vs

vtm_dir = '/home/VVCSoftware_VTM/'
cfg_dir = '/home/cfg-files'
out_dir = '/home/output'

encoder = ['RA']
qps = [22, 37]

sim = vs.sim.Simulation(n_frames=32, qps=qps, encoder=encoder, bg_exec=False)
sim.set_paths(out_dir, vtm_dir, out_dir)

sim.run_exec()
```

in this example, the software will execute each of the videos in the `'/home/cfg-files'` directory for each of the encoders `'RA', 'AI', 'LB'` for each qp in the default qps `22, 27, 32, 37` for 32 frames of the video. The software will run in background and will not generate a gprof file. The output files will be stored at the `'/home/output'` directory. If this directory not exists, then it will be created.

_output of the software in the console_:

```
Execution running
---------------------------------------------- 
out directory     /home/output/
vtm directory     /home/VVCSoftware_VTM/
cfg directory     /home/cfg-files/
---------------------------------------------- 

version :         Precise 
qps :             [22, 37] 
encoder :         ['RA'] 
n_frames :        32 
background exec : False 
gprof :           False 
videos :          [ 
                       0. RaceHorses.cfg
                  ] 
---------------------------------------------- 
Total execution 1 x 2 x 1 = 2 simulations
---------------------------------------------- 


Encoding: ........... RaceHorses

Video config: ....... /home/cfg-files/RaceHorses.cfg
Encoder: ............ RA
QP: ................. 22
VTM version used: ... Precise
frames encoded: ..... 32

Encoding: ........... RaceHorses

Video config: ....... /home/cfg-files/RaceHorses.cfg
Encoder: ............ RA
QP: ................. 37
VTM version used: ... Precise
frames encoded: ..... 32

Simulation done
```

## Making changes in VTM

To replace a file in VTM for an alternative version, the method `simulation.replace_file(old_file, new_file)` can be used. It will replace the file and then will recompile the VTM.

```py
new_file = '/home/RdCostModified.cpp'
old_file = '/home/VVCSoftware_VTM/source/Common/CommonLib/RdCost.cpp'

sim.change_version("RdCostModified", old_file, new_file)

sim.run_exec()
```

## Simulation output

The files will be stored in such way that the `vvc_log` package can interpret. It can be represented in a file tree like above.

### file structure representation:

> output
>
>> gprof_log
>>
>>> AI
>>>
>>>> log_video1_qp22_AI_Precise.gplog
>>>> log_video1_qp27_AI_Precise.gplog
>>>> log_video2_qp22_AI_Precise.gplog
>>>> log_video2_qp27_AI_Precise.gplog
>>>>
>>>
>>

>>> LB
>>> RA
>>>
>>

>> videos_bin
>>
>>> videos.bin
>>>
>>

>> vvc_log
>>
>>> AI
>>> LB
>>> RA
>>>
>>
