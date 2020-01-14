# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 17:08:47 2019
@author: ga47jes
"""

from ems.ems_mod import ems as ems_loc
# from ems.flex.flex_draw import plot_flex as plot_flex
from ems.optim.opt_test import run_hp_opt as opt
from ems.flex.Bat import Batflex
import pandas as pd

def PVflex(my_ems):
    nsteps = my_ems['time_data']['nsteps']
    ntsteps = my_ems['time_data']['ntsteps']
    PV_flex = pd.DataFrame(0, index=range(nsteps), columns=range(7))
    PV_flex.columns = ['Sch_P', 'Neg_P', 'Pos_P', 'Neg_E', 'Pos_E', 'Neg_Pr', 'Pos_Pr']
    dat1 = my_ems['optplan']['pv_pv2grid'] 
    dat2 = my_ems['optplan']['PV_power']
    
    # PV negative flexibility
    for i in range(nsteps):
        PV_flex.iloc[i,0] = dat1[i]
        if dat2[i] > 0.1:
            j = i
            while dat2[i] <= dat2[j]:
                j = j+1
            PV_flex.iloc[i, 1] = -1*dat2[i]
            PV_flex.iloc[i, 3] = PV_flex.iloc[i, 1]*(j-i)/ntsteps  
    
    # PV negative flexibility pricing
    for i in range(nsteps):
        if dat2[i] > 0.1:
            PV_flex.iloc[i, 5] = -0.11
    return PV_flex

if __name__ == '__main__':
    my_ems = ems_loc(initialize=True, path='C:/Users/ge57vam/emsflex/ems/test_chp.txt')
    my_ems['fcst'] =  input_data(my_ems)
    # my_ems['flexopts']['pv'] = PVflex(my_ems)
    # my_ems['time_data']['nsteps'] = 24
    # my_ems['time_data']['ntsteps'] = 1
    # my_ems['time_data']['t_inval'] = 60
    # my_ems['time_data']['d_inval'] = 15
    # my_ems['time_data']['days'] = 1
    my_ems['devices']['pv']['maxpow'] = 15
   #  my_ems['optplan'] = opt(my_ems, plot_fig=False, result_folder='C:/Optimierung/')
   #  my_ems['flexopts']['pv'] = PVflex(my_ems)
   #  my_ems['flexopts']['bat'] = Batflex(my_ems)
   #  plot_flex(my_ems, 'bat')
   # # save_results(my_ems['flexopts']['hp'])
