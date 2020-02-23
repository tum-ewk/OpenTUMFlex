import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ems.ems_mod import ems as ems_loc
from ems.ems_mod import ems_write
from ems.ems_mod import update_time_data
from ems.devices.devices import devices

from forecast.fcst import load_data

from ems.optim.opt_test import run_hp_opt as opt
from ems.optim.optimize_EV_charging import create_ev_model

from pyomo.opt import SolverFactory
# import flex devices modules
from ems.flex.flex_ev import  calc_flex_ev
from ems.plot.flex_draw import plot_flex as plot

# Read home availabilities from file
veh_availability = pd.read_csv('data/chts_veh_availability.csv')

# Total number of home availabilities with trips conducted before and afterwards
n_avail = len(veh_availability)
n_veh = len(veh_availability['vehID'].unique())

mil2km_conversion = 1.61            # Miles to kilometer conversion rate
electr_consumption_per_km = 0.2     # electricity consumption per km (e.g. 0.2 equals 20kWh/100km

# load the predefined ems data, initialization by user input is also possible:
my_ems = ems_loc(initialize=True, path='data/test_Nr_01.txt')

# Go through all vehicle availabilities
for i in range(1):
    print(veh_availability['t_arrival'][i])

    # change the time interval
    my_ems['time_data']['t_inval'] = 15
    my_ems['time_data']['d_inval'] = 15
    my_ems['time_data']['start_time'] = veh_availability['t_arrival'][i][:-3]
    my_ems['time_data']['end_time'] = veh_availability['t_departure'][i][:-3]
    my_ems['time_data']['days'] = 1
    print(veh_availability['t_arrival'][i])
    my_ems.update(update_time_data(my_ems))
    print(veh_availability['t_arrival'][i])

    # load the weather and price data
    ### very slow!!!
    my_ems['fcst'] = load_data(my_ems)

    print(veh_availability['t_arrival'][i])
    # Update EV parameters
    my_ems['devices'].update(devices(device_name='ev', minpow=0, maxpow=11,
                                     stocap=veh_availability['d_travelled']*mil2km_conversion*electr_consumption_per_km,
                                     init_soc=[0], end_soc=[100], eta=0.98,
                                     ev_aval=[veh_availability['t_arrival'][i][:-3], veh_availability['t_departure'][i][:-3]],
                                     timesetting=my_ems['time_data']))

    # # calculate the timetable for all the devices
    # my_ems['optplan'] = opt(my_ems, plot_fig=True, result_folder='data/')

    ev_model = create_ev_model(init_soc_bat=0, desired_soc=100, soc_max=100, soc_min=0, p_bat_min=0, p_bat_max=11,
                               price_forecast=my_ems['fcst']['ele_price_in'], battery_cap=50, efficiency=0.98,
                               n_time_steps=my_ems['time_data']['nsteps'], availability=my_ems['devices']['ev']['aval'],
                               total_hours=veh_availability['delta_t_sec'][i]/3600)

    optim = SolverFactory('glpk')
    result = optim.solve(ev_model)
    print(result)

    for i in range(my_ems['time_data']['nsteps']):
        my_ems['optplan']['EV_power'][i] = ev_model.p_bat_charge[i].value
