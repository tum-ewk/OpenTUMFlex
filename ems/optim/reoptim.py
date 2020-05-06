# -*- coding: utf-8 -*-
"""
Created on Tue May  5 10:30:42 2020

@author: ga47jes
"""


# import pandas as pd

# import optimization module
from ems.optim.opt_test import run_hp_opt as opt

# import flex devices modules
from ems.flex.PV import calc_flex_pv
from ems.flex.Bat import calc_flex_bat

# import plot module
from ems.plot.flex_draw import plot_flex as plot

def reoptimize(my_ems):
    device = my_ems['reoptim']['device']
    rstep = my_ems['reoptim']['timestep']
    f_type = my_ems['reoptim']['flextype']
    ntsteps = my_ems['time_data']['ntsteps']
    
    f_pow = my_ems['flexopts'][device].loc[rstep, f_type+'_P']
    f_ene = my_ems['flexopts'][device].loc[rstep, f_type+'_E']
    if f_pow != 0:
        f_steps = int(round(f_ene*ntsteps/f_pow))
    else:
        f_steps = 0
        print('No flexibility found')    
    my_ems['time_data']['isteps'] = rstep+f_steps+1
    
    print('Reoptimization')
    my_ems['reoptim']['optplan'] = opt(my_ems, plot_fig=False, result_folder='data/')
    my_ems['reoptim']['flexopts'] = {}
    my_ems['reoptim']['flexopts']['pv'] = calc_flex_pv(my_ems, reopt=1)
    my_ems['reoptim']['flexopts']['bat'] = calc_flex_bat(my_ems, reopt=1)
    return my_ems

if __name__ == '__main__':
    print('update myems')
    # my_ems = reoptimize(my_ems)