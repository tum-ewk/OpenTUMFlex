"""
The "example_2.py" module demonstrates an example to calculate flexibility assuming 
the house to have all pv, battery and hp. 
"""

__author__ = "Zhengjie You"
__copyright__ = "2020 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "1.0"
__maintainer__ = "Zhengjie You"
__email__ = "zhengjie.you@tum.de"
__status__ = "Development"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# import ems and devices modules
from ems.ems_mod import ems as ems_loc
from ems.ems_mod import ems_write
from ems.ems_mod import update_time_data
from ems.devices.devices import devices
from ems.devices.devices import device_write

# Get data
from ems.ems_mod import read_data

# import optimization module
from ems.optim.opt import run_opentumflex

# import flex devices modules
from ems.flex.flexhp import calc_flex_hp
from ems.flex.flexchp import calc_flex_chp
from ems.flex.flex_bat import calc_flex_bat
from ems.flex.flex_pv import calc_flex_pv
from ems.flex.flex_ev import calc_flex_ev

# import plot module
from ems.plot.flex_draw import plot_flex
from ems.plot.flex_draw import save_results
from ems.plot.reopt_draw import plot_reopt as plot_reopt
from ems.plot.reopt_draw import plot_reopt_compare as plot_com
from ems.plot.reopt_draw import plot_reopt_price as plot_reopt_price

# fix the time setup
my_ems = {'time_data': {}}
my_ems['time_data']['t_inval'] = 15  # set the time interval in OpenTUMFlex
my_ems['time_data']['d_inval'] = 15  # set the t ime interval of the input data (load profiles, prices, weather..)
my_ems['time_data']['start_time'] = '2019-12-18 00:00'  # set the start time of simulation
my_ems['time_data']['end_time'] = '2019-12-18 23:45'  # set the end time of simulation
my_ems['time_data']['days'] = 1  # set the total days of simulation
my_ems.update(update_time_data(my_ems))  # use built-in function "update_time_data" to obtain other time settings

# Initialize ems and forecasting data
base_dir = os.path.abspath(os.getcwd())  # get the current working directory
sub_dir = r'data\input_data.csv'  # file name of input data
path_input_data = os.path.join(base_dir, sub_dir)  # combine the path and file name
read_data(my_ems, path=path_input_data)  # load predefined device parameters and forecasting data to ems

# add or change the utility/devices parameters
my_ems['devices'].update(devices(device_name='boiler', maxpow=4))  # change the boiler power from 2 kW to 4 kW
my_ems['devices'].update(devices(device_name='hp', minpow=0, maxpow=2, supply_temp=45))  # add heat pump

# calculate the timetable for all the devices
my_ems['optplan'] = run_opentumflex(my_ems, plot_fig=True, result_folder='data/')  # obtain the optimal plans

# calculate the flexibility of one device
my_ems['flexopts']['bat'] = calc_flex_bat(my_ems, reopt=False)  # calculate the flexibility of ev, no reoptimization
my_ems['flexopts']['hp'] = calc_flex_hp(my_ems, reopt=False)  # calculate the flexibility of hp, no reoptimization

# plot the flexibility results
plot_flex(my_ems, "bat")  # flexibility of battery
plot_flex(my_ems, "hp")  # flexibility of heat pump
