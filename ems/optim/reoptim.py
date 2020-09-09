# -*- coding: utf-8 -*-
"""
Created on Tue May  5 10:30:42 2020

@author: ga47jes
"""


# import pandas as pd

# import optimization module
from ems.optim.opt_test import run_hp_opt as opt

# import flex devices modules
from ems.flex.flex_pv import calc_flex_pv
from ems.flex.flex_bat import calc_flex_bat
from ems.flex.flexhp import calc_flex_hp

# import plot module
from ems.plot.flex_draw import plot_flex as plot

def reoptimize(my_ems):    
    device = my_ems['reoptim']['device']
    # Make relevant changes for flexibility
    if device == 'pv':
        my_ems = reflex_pv(my_ems)    
    elif device == 'bat':
        my_ems = reflex_bat(my_ems)
    elif device == 'ev':
        my_ems = reflex_ev(my_ems)
    elif device == 'hp':
        my_ems = reflex_hp(my_ems)
        
    if my_ems['reoptim']['status'] == 1:        
        print('Reoptimization')
        my_ems['reoptim']['optplan'] = opt(my_ems, plot_fig=True, result_folder='data/')
        my_ems['reoptim']['flexopts'] = {}
        my_ems['reoptim']['flexopts']['pv'] = calc_flex_pv(my_ems, reopt=1)
        my_ems['reoptim']['flexopts']['bat'] = calc_flex_bat(my_ems, reopt=1)
        # my_ems['reoptim']['flexopts']['ev'] = calc_flex_ev(my_ems, reopt=1)
        my_ems['reoptim']['flexopts']['hp'] = calc_flex_hp(my_ems, reopt=1)
        
    return my_ems

def reflex_pv(my_ems):
    device = my_ems['reoptim']['device']
    rstep = my_ems['reoptim']['timestep']
    f_type = my_ems['reoptim']['flextype']
    ntsteps = my_ems['time_data']['ntsteps']
    
    if f_type == 'Neg':
        # Flexibility information    
        f_pow = my_ems['flexopts'][device].loc[rstep, f_type+'_P']
        f_ene = my_ems['flexopts'][device].loc[rstep, f_type+'_E']
        if f_pow != 0:
            f_steps = int(round(f_ene*ntsteps/f_pow))
            my_ems['reoptim']['status'] = 1
        else:
            f_steps = 0
            print('No flexibility found')    
            my_ems['reoptim']['status'] = 0
            
        if my_ems['reoptim']['status'] == 1:            
            # Update initial steps for reoptimization
            my_ems['time_data']['isteps'] = rstep+f_steps+1
            
            # Battery SOC at flexibility time step
            s_bSOC = my_ems['optplan']['bat_SOC'][rstep]
            e_bSOC = my_ems['optplan']['bat_SOC'][rstep+f_steps]    
            bat_max_e = my_ems['devices']['bat']['stocap']
        
            if s_bSOC >= e_bSOC:
                # print('Scheduled battery discharging or none during flexibility \n')
                tot_dis = 0
                for i in range(rstep,rstep+f_steps):
                    tot_dis = tot_dis + my_ems['optplan']['bat_output_power'][i]
                tot_dis = tot_dis*f_steps/ntsteps
                if abs(f_ene) >= tot_dis:
                    e_bal = abs(f_ene) - tot_dis
                    e_bal_soc = e_bal*100/bat_max_e
                    if s_bSOC + e_bal_soc <= 100 :
                        my_ems['devices']['bat']['initSOC'] = s_bSOC + e_bal_soc
                    else:
                        my_ems['devices']['bat']['initSOC'] = 100
                        # rest_e = (s_bSOC+e_bal_soc-90)*bat_max_e/100
                else:
                    soc_red = tot_dis - abs(f_ene)
                    soc_red = soc_red*100/bat_max_e    #in %
                    my_ems['devices']['bat']['initSOC'] = s_bSOC - soc_red      
            else:
                # print('Scheduled battery charging during flexibility \n')    
                SOC_added = abs(f_ene*100/bat_max_e)
                if e_bSOC + SOC_added > 100: # Include SOC limits
                    my_ems['devices']['bat']['initSOC'] = 100
                else: 
                    my_ems['devices']['bat']['initSOC'] = e_bSOC + SOC_added     
    
    elif f_type == 'Pos':
        my_ems['reoptim']['status'] = 0
        print('No positive flexibility for PV')   
    
    return my_ems

def reflex_bat(my_ems):
    device = my_ems['reoptim']['device']
    rstep = my_ems['reoptim']['timestep']
    f_type = my_ems['reoptim']['flextype']
    ntsteps = my_ems['time_data']['ntsteps']
    
    # Flexibility information    
    f_pow = my_ems['flexopts'][device].loc[rstep, f_type+'_P']
    f_ene = my_ems['flexopts'][device].loc[rstep, f_type+'_E']
    if f_pow != 0:
        f_steps = int(round(f_ene*ntsteps/f_pow))
        my_ems['reoptim']['status'] = 1
    else:
        f_steps = 0
        print('No flexibility found \n')    
        my_ems['reoptim']['status'] = 0
            
    if my_ems['reoptim']['status'] == 1:         
        # Update initial steps for reoptimization
        my_ems['time_data']['isteps'] = rstep+f_steps+1
        
        # Battery SOC at flexibility time step
        # s_bSOC = my_ems['optplan']['bat_SOC'][rstep]
        e_bSOC = my_ems['optplan']['bat_SOC'][rstep+f_steps]    
        bat_max_e = my_ems['devices']['bat']['stocap']
        
        if f_type == 'Neg':
           SOC_added = abs(f_ene*100/bat_max_e)
           if e_bSOC + SOC_added > 100:
               my_ems['devices']['bat']['initSOC'] = 100
           else:
               my_ems['devices']['bat']['initSOC'] = e_bSOC + SOC_added
           
        elif f_type == 'Pos':
            SOC_rem = abs(f_ene*100/bat_max_e)
            if e_bSOC - SOC_rem < 0:
                my_ems['devices']['bat']['initSOC'] = 0
            else: 
                my_ems['devices']['bat']['initSOC'] = e_bSOC - SOC_rem
       
    return my_ems  

def reflex_ev(my_ems):
    device = my_ems['reoptim']['device']
    rstep = my_ems['reoptim']['timestep']
    f_type = my_ems['reoptim']['flextype']
    ntsteps = my_ems['time_data']['ntsteps']
    
    # Flexibility information    
    f_pow = my_ems['flexopts'][device].loc[rstep, f_type+'_P']
    f_ene = my_ems['flexopts'][device].loc[rstep, f_type+'_E']
    if f_pow != 0:
        f_steps = int(round(f_ene*ntsteps/f_pow))
        my_ems['reoptim']['status'] = 1
    else:
        f_steps = 0
        print('No flexibility found \n')    
        my_ems['reoptim']['status'] = 0
            
    if my_ems['reoptim']['status'] == 1:         
        # Update initial steps for reoptimization
        my_ems['time_data']['isteps'] = rstep+f_steps+1
        
        # Battery SOC at flexibility time step
        # s_bSOC = my_ems['optplan']['bat_SOC'][rstep]
        e_bSOC = my_ems['optplan']['EV_SOC'][rstep+f_steps]    
        bat_max_e = my_ems['devices']['ev']['stocap']
        
        if f_type == 'Neg':
           SOC_added = abs(f_ene*100/bat_max_e)
           if e_bSOC + SOC_added > 100:
               my_ems['devices']['bat']['initSOC'] = 100
           else:
               my_ems['devices']['bat']['initSOC'] = e_bSOC + SOC_added
           
        elif f_type == 'Pos':
            SOC_rem = abs(f_ene*100/bat_max_e)
            if e_bSOC - SOC_rem < 0:
                my_ems['devices']['bat']['initSOC'] = 0
            else: 
                my_ems['devices']['bat']['initSOC'] = e_bSOC - SOC_rem     
                
    return my_ems  

def reflex_hp(my_ems):
    device = my_ems['reoptim']['device']
    rstep = my_ems['reoptim']['timestep']
    f_type = my_ems['reoptim']['flextype']
    ntsteps = my_ems['time_data']['ntsteps']
    
    # Flexibility information    
    f_pow = my_ems['flexopts'][device].loc[rstep, f_type+'_P']
    f_ene = my_ems['flexopts'][device].loc[rstep, f_type+'_E']
    if f_pow != 0:
        f_steps = int(round(f_ene*ntsteps/f_pow))
        my_ems['reoptim']['status'] = 1
    else:
        f_steps = 0
        print('No flexibility found \n')    
        my_ems['reoptim']['status'] = 0
        
    if my_ems['reoptim']['status'] == 1:         
        # Update initial steps for reoptimization
        my_ems['time_data']['isteps'] = rstep+f_steps+1
        
        # Battery SOC at flexibility time step
        # s_bSOC = my_ems['optplan']['bat_SOC'][rstep]
        e_hSOC = my_ems['optplan']['SOC_heat'][rstep]    
        sto_max_e = my_ems['devices']['sto']['stocap']
        COP_avg = sum(my_ems['optplan']['HP_COP'][rstep:rstep+f_steps])/f_steps
        
        if f_type == 'Neg':
           SOC_added = abs(COP_avg*f_ene*100/sto_max_e)
           if e_hSOC + SOC_added > 100:
               my_ems['devices']['sto']['initSOC'] = 100
           else:
               my_ems['devices']['sto']['initSOC'] = e_hSOC + SOC_added
           
        elif f_type == 'Pos':
            SOC_rem = abs(COP_avg*f_ene*100/sto_max_e)
            print(SOC_rem)
            if e_hSOC - SOC_rem < 0:
                my_ems['devices']['sto']['initSOC'] = 0
            else: 
                my_ems['devices']['sto']['initSOC'] = e_hSOC - SOC_rem 
                
    return my_ems      

if __name__ == '__main__':
    print('update myems')
    # my_ems = reoptimize(my_ems)