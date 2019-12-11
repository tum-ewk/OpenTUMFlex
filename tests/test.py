
import pandas as pd

from ems.ems_mod import ems as ems_loc
from ems.devices.devices import devices as dev
from ems.devices.devices import device_write as dev_write
from tests.fcst import load_data as input_data
from ems.optim.opt_test import run_hp_opt as opt
# from ems.flex.flexhp import flexhp as flexhp
from ems.ems_mod import ems_write as ems_loc_write
from ems.plot.flex_draw import plot_flex as plot
from ems.plot.flex_draw import save_results as save_results
from ems.flex.flexhp import calc_flex_hp

# load the predefined ems data, initialization by user input is also possible:
# my_ems = ems_loc(userpref='type1', flexprodtype='type2', timeintervall=15, path='C:/...')
# my_ems = ems_loc(initialize=True, path='C:/Users/ge57vam/emsflex/ems/test_time.txt')
my_ems = ems_loc(initialize=True, path='C:/Users/ge57vam/emsflex/ems/test_time_60min.txt')

# change the time interval
my_ems['time_data']['nsteps'] = 24
my_ems['time_data']['ntsteps'] = 1
my_ems['time_data']['t_inval'] = 60
my_ems['time_data']['d_inval'] = 15
my_ems['time_data']['days'] = 1

# load the weather and price data
my_ems['fcst'] = input_data(my_ems)

# add or change the utility/devices
# if deleting one specific device please use
# del my_ems['devices']['hp']
# my_ems['devices'].update(dev(device_name='hp', minpow=3, maxpow=6))

my_ems['devices'].update(dev(device_name='hp', minpow=0, maxpow=2))
my_ems['devices']['sto']['stocap'] = 24
my_ems['devices']['boiler']['maxpow'] = 20
my_ems['devices']['chp']['maxpow'] = 2
my_ems['devices']['pv']['maxpow'] = 5
my_ems['devices']['bat']['stocap'] = 10
my_ems['devices']['bat']['maxpow'] = 5
my_ems['devices']['ev']['maxpow'] = 0

# write the device parameter data in JSON file for reuse,
# dev_write(my_ems, 'pv', 'C:/Users/ge57vam/emsflex/ems/pv_test.txt')
# dev_write(my_ems, 'ev', 'C:/Users/ge57vam/emsflex/ems/ev_test.txt')

# calculate the timetable for all the devices
my_ems['optplan'] = opt(my_ems, plot_fig=True, result_folder='C:/Optimierung/')

# calculate the flexibility of one device
my_ems['flexopts']['hp'] = calc_flex_hp(my_ems)

# plot the results
plot(my_ems, "hp")

# store the data of the whole ems for reuse
# ems_loc_write(my_ems, path='C:/Users/ge57vam/emsflex/tests/test_Nr_01.txt')
