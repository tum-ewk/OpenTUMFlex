# -*- coding: utf-8 -*-
"""
main script to run the flexibility model

@author: ge57vam
"""



import pandas as pd
import json as js

import ems.devices as dev
import forecast as fcst
import ems.optm as opt_test
import ems.flex as flex
import ems.plot as flexplot




#create the DataFrame of ems using ems module

my_ems = ems(initialize=True, path='C:/Users/ge57vam/emsflex/ems/755552222_ems.txt')

# if the fcst DataFrame in the dict is empty, the fcst module should be used to initialize it
if my_ems['fcst'] is None:
    my_ ems['fcst'] = fcst(path);

# add new devices in ems, either from file or user inout
if my_ems['devices'] is None:
    my_ems['devices'].update(dev(path, device_name));

# if the optimal plan is not available, then use the opt module to get the plans of all available devices
if my_ems['optplan'] is None:
    my_ems['optplan'] = opt_test.run_hp_opt(my_ems);

# calculate the flexibility options for one specific device
if my_ems['flexopts'] is None:
    my_ems['flexopts'] = flex(my_ems, device_name);

# visualize the results and store the diagramms in the path
flexplot(my_ems)

#write the ems data in .js .xlsx or .txt file
write_results(my_ems, path)


    

    

