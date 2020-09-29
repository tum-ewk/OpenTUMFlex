"""
Created on Tue Oct 29 17:08:47 2019
@author: Babu Kumaran Nalini, M.Sc. Technical University Munich
Strictly not for ciruculation. Personal file. 
"""

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
from ems.optim.opt_test import run_hp_opt as opt

# import flex devices modules
from ems.flex.flexhp import calc_flex_hp
from ems.flex.flexchp import calc_flex_chp
from ems.flex.flex_bat import calc_flex_bat
from ems.flex.flex_pv import calc_flex_pv
from ems.flex.flex_ev import  calc_flex_ev

# import plot module
from ems.plot.flex_draw import plot_flex as plot
from ems.plot.flex_draw import save_results
from ems.plot.reopt_draw import plot_reopt as plot_reopt
from ems.plot.reopt_draw import plot_reopt_compare as plot_com
from ems.plot.reopt_draw import plot_reopt_price as plot_reopt_price

# import reoptimization
from ems.optim.reoptim import reoptimize

# import offers
from ems.offers.gen_offers import alf_markt

# Close all figures
plt.close('all')

def run_ems(path= None):
    
    # Change the time interval
    my_ems = {'time_data': {}}
    my_ems['time_data']['t_inval'] = 15
    my_ems['time_data']['d_inval'] = 15
    my_ems['time_data']['start_time'] = '2019-12-18 00:00'
    my_ems['time_data']['end_time'] = '2019-12-18 23:45'
    my_ems['time_data']['days'] = 1
    my_ems.update(update_time_data(my_ems))    
    
    # Initialize EMS and load data
    read_data(my_ems, path, to_csv=1) 
       
    # add or change the utility/devices
    my_ems['devices']['boiler']['maxpow'] = 4
    # my_ems['devices']['chp']['maxpow'] = 0
    # my_ems['devices'].update(devices(device_name='hp', minpow=0, maxpow=2, supply_temp=45))   
    
    # calculate the timetable for all the devices    
    my_ems['optplan'] = opt(my_ems, plot_fig=False, prnt_pgr=False, result_folder='data/')
        
    # # calculate the flexibility of one device
    my_ems['flexopts']['pv'] = calc_flex_pv(my_ems, reopt=0)
    my_ems['flexopts']['bat'] = calc_flex_bat(my_ems, reopt=0)
    my_ems['flexopts']['ev'] = calc_flex_ev(my_ems)
    my_ems['flexopts']['hp'] = calc_flex_hp(my_ems, reopt=0)
    my_ems['flexopts']['chp'] = calc_flex_chp(my_ems)
        
    # plot the results
    # plot(my_ems, "ev")
    # plot(my_ems, "pv")
    # plot(my_ems, "bat")
    # plot(my_ems, "hp")
    # plot(my_ems, "chp")
    
    # Reoptimization
    # Selected offer - Device and timestep
    my_ems['reoptim']['device'] = 'bat'  # Ues pv/bat
    my_ems['reoptim']['timestep'] = 20
    my_ems['reoptim']['flextype'] = 'Neg' # Use Neg/Pos
    my_ems = reoptimize(my_ems, plot_fig=False)
    
    # Plot reoptimization
    # if my_ems['reoptim']['status'] == 1:
    #     plot_reopt(my_ems)
    #     plot_com(my_ems)
    #     plot_reopt_price(my_ems)

    return my_ems

if __name__ == "__main__":
    base_dir = os.path.abspath(os.getcwd())
    sub_dir = r'data\input_data.csv'    
    directory = os.path.join(base_dir, sub_dir)
    my_ems = run_ems(path=directory)
    print('Completed')
