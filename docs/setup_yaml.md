# How to use the setup file (yaml)
The setup file is used to easily create an working environment to each experiment made with VTM software.

## Contents
The setup file contains information about the VVC environment, such as where is the VTM folder, where is the configuration files to the videos and where the output files must be stored.

## Structure
The file must begin with `---`, after this, each line represents the path to a folder needed to the environment. The file is organized as follows:
 
 * **cfg**: Folder with the configuration files to the videos
 * **out**: Folder where the framework must store the output
 * **vtm**: Folder with VTM software

Below there's a example of a yaml setup file to the framework:

``` yaml
---
  cfg: /home/cfg-files
  out: /home/output
  vtm: /home/VVCSoftware_VTM
```
## Using in the framework
The setup file can be used to initialize the environment at a ```vvcpy.sim.Simulation()``` object by using the method ```vvcpy.sim.Simulation.read_yaml(file : str)```

``` python
from vvcpy import sim 
s = sim.Simulation()
s.read_yaml('setup.yaml')

s.get_exec_info(display=True)
```

The software must return something like this, depending on the videos on the `cfg` folder
```
---------------------------------------------- 
out directory     /home/output
vtm directory     /home/VVCSoftware_VTM
cfg directory     /home/cfg-files
---------------------------------------------- 

version :         Precise 
qps :             [22, 27, 32, 37] 
encoder :         ['AI', 'RA', 'LB'] 
n_frames :        32 
background exec : False 
videos :          [ 
                       0. BasketballDrive.cfg
                       1. BasketballPass.cfg
                       2. BQMall.cfg
                       3. Campfire.cfg
                       4. FoodMarket4.cfg
                       5. FourPeople.cfg
                       6. Johnny.cfg
                       7. RaceHorses.cfg
                       8. RitualDance.cfg
                  ] 
---------------------------------------------- 
Total execution 9 x 4 x 3 = 108 simulations
---------------------------------------------- 
```