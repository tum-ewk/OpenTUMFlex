
import pandas as pd
import numpy as np

# import ems and devices modules
from ems.ems_mod import ems as ems_loc
from ems.ems_mod import ems_write
from ems.devices.devices import devices
from ems.devices.devices import device_write

# import forecast model for weather and price data
from forecast.fcst import load_data

# import optimization module
from ems.optim.opt_test import run_hp_opt as opt

# import flex devices modules
from ems.flex.flexhp import calc_flex_hp
from ems.flex.flexchp import calc_flex_chp
from ems.flex.Bat import Batflex
from ems.flex.PV import PVflex

# import plot module
from ems.plot.flex_draw import plot_flex as plot
from ems.plot.flex_draw import save_results

# load the predefined ems data, initialization by user input is also possible:
my_ems = ems_loc(initialize=True, path='data/test_Nr_01.txt')

# change the time interval
my_ems['time_data']['t_inval'] = 15
my_ems['time_data']['d_inval'] = 15
my_ems['time_data']['ntsteps'] = int(60 / my_ems['time_data']['t_inval'])
my_ems['time_data']['nsteps'] = my_ems['time_data']['ntsteps'] * 24
my_ems['time_data']['days'] = 1

# load the weather and price data
my_ems['fcst'] = load_data(my_ems)

# add or change the utility/devices
# if deleting one specific device please use del my_ems['devices']['hp']
# my_ems['devices'].update(dev(device_name='hp', minpow=3, maxpow=6))
my_ems['devices'].update(devices(device_name='hp', minpow=0, maxpow=2))
my_ems['devices']['sto']['stocap'] = 15
my_ems['devices']['boiler']['maxpow'] = 20
my_ems['devices']['chp']['maxpow'] = 3
# my_ems['devices'].update(dev(device_name='chp', path="C:/Users/ge57vam/emsflex/ems/chp01_ems.txt"))
my_ems['devices']['pv']['maxpow'] = 5
my_ems['devices']['bat']['stocap'] = 10
my_ems['devices']['bat']['maxpow'] = 10
my_ems['devices'].update(devices(device_name='ev', minpow=0, maxpow=8, stocap=40, init_soc=20, end_soc=90, eta=0.98,
                                 ev_aval=["4:00", "7:00", "17:45", "19:15", "21:30", "23:15"], _timesteps=96))
# my_ems['devices']['ev']['maxpow'] = 5

# write the device parameter data in JSON file for reuse,
# dev_write(my_ems, 'pv', 'C:/Users/ge57vam/emsflex/ems/pv_test.txt')
# dev_write(my_ems, 'ev', 'C:/Users/ge57vam/emsflex/ems/ev_test.txt')

# calculate the timetable for all the devices
my_ems['optplan'] = opt(my_ems, plot_fig=True, result_folder='C:/Users/ge57vam/emsflex/tests/')

# calculate the flexibility of one device
# my_ems['flexopts']['hp'] = calc_flex_hp(my_ems)
# my_ems['flexopts']['chp'] = calc_flex_chp(my_ems)
# my_ems['flexopts']['bat'] = Batflex(my_ems)
# my_ems['flexopts']['pv'] = PVflex(my_ems)

# plot the results
# plot(my_ems, "hp")

# store the data of the whole ems for reuse
# ems_write(my_ems, path='C:/Users/ge57vam/emsflex/tests/data/test_Nr_02.txt')
