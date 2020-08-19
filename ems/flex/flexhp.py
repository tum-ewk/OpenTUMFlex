# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 14:24:53 2019

@author: ge57vam
"""

import pandas as pd
import numpy as np
import heapq

from ems.ems_mod import ems as ems_loc
from ems.plot.flex_draw import plot_flex as plot_flex
from ems.plot.flex_draw import save_results as save_results


def calc_flex_hp(ems, reopt):  # datafram open and break it down

    # week = pd.DataFrame(index=pd.date_range(start="00:00", end="23:59", freq='15min').strftime('%H:%M'),
    #                     columns={'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'})

    if reopt == 0:
        optm_df = pd.DataFrame.from_dict(ems['optplan'])  
        
    elif reopt == 1:
        optm_df = pd.DataFrame.from_dict(ems['reoptim']['optplan'])       
        
    timesteps = len(optm_df['HP_operation'])
    ntsteps = ems['time_data']['ntsteps']
    pow2energy = 1 / ntsteps
    # get the values from hp dataframe

    hp_operation = optm_df['HP_operation']
    hp_heat_ifrun = optm_df['HP_heat_run']
    hp_elec_ifrun = optm_df['HP_ele_run']
    hp_heat_pow = hp_operation * hp_heat_ifrun
    hp_elec_pow = hp_operation * hp_elec_ifrun

    # get the values of heat storage
    hs_param = ems['devices']['sto']
    soc_heat = optm_df['SOC_heat']
    hs_cap = hs_param['stocap']  # kWh
    hs_soc_init = hs_param['initSOC']
    hs_soc_end = 0.5
    hs_eta = 0.98
    hs_self_discharge = 0.0005

    # get the max duration of flexibility for every time step

    # max duration from the optimal operation
    dur_max_opt = np.zeros(timesteps)

    for i in range(timesteps):
        if hp_operation[i] > 0:
            dur_max_opt[i] = next((x for x, val in enumerate(hp_operation[i:]) if val == 0), timesteps - i) + i - 1
        else:
            dur_max_opt[i] = next((x for x, val in enumerate(hp_operation[i:]) if val > 0), timesteps - i) + i - 1

    # max duration from available regeneration time

    dur_max_reg = np.zeros(timesteps)
    for i in range(timesteps):
        if hp_operation[i] > 0:
            # dur_max_reg[i] = min(i + sum(1-hp_operation[i:]) - 1, timesteps - 1)
            dur_max_reg[i] = min(i + sum(1 - hp_operation[i:]) - 1, timesteps)
        else:
            # dur_max_reg[i] = min(i + sum(hp_operation[i:]) - 1, timesteps - 1)
            dur_max_reg[i] = min(i + sum(hp_operation[i:]) - 1, timesteps)

    # max duration from storage capacity
    dur_max_sto = np.zeros(timesteps)

    # on/off states to soc change

    soc_change = hp_heat_ifrun * pow2energy / hs_cap * (0.5 - hp_operation) * 2 * 100
    for i in range(timesteps):
        soc = soc_heat[i]
        idx = i
        while 0 < soc < 100:
            idx += 1
            if idx > timesteps:
                break
            soc += soc_change[idx - 1]

        dur_max_sto[i] = idx - 2

    dur_max = list(map(int, map(min, zip(dur_max_opt, dur_max_reg, dur_max_sto))))

    # summary of flexpow and flexenergy

    pow_schedual = -hp_elec_pow
    pow_pos = -pow_schedual
    pow_neg = -(hp_elec_ifrun + pow_schedual)
    energy_pos = np.zeros(timesteps)
    energy_neg = np.zeros(timesteps)
    idx_no_flex = np.zeros(timesteps)
    for i in range(timesteps):
        if dur_max[i] < i:  # which means the flexibility is not available in this time step
            idx_no_flex[i] = 1
            pow_pos[i] = 0
            pow_neg[i] = 0
            dur_max[i] = i
        if hp_operation[i] > 0:
            energy_pos[i] = pow2energy * pow_pos[i] * (dur_max[i] - i + 1)
        else:
            energy_neg[i] = pow2energy * pow_neg[i] * (dur_max[i] - i + 1)

    # get the price

    # cost_elec_input = list(map(float, list(ems['fcst']['ele_price_in'])))
    # cost_elec_input = pd.DataFrame.from_dict(ems['fcst']['ele_price_in'], orient='index')[0]
    # cost_elec_input = ems['optplan']['elec_supply_price']
    start_step = ems['time_data']['isteps']
    cost_elec_input = ems['fcst']['ele_price_in'][start_step:]
    
    cost_diff_pos = np.zeros(timesteps)
    cost_diff_neg = np.zeros(timesteps)
    for i in range(timesteps):
        count_flex_ts = dur_max[i] - i + 1
        if hp_operation[i] > 0:
            cost_modified = list(map(float, cost_elec_input[dur_max[i] + 1:])) + hp_operation[dur_max[i] + 1:] * 100
            # cost_orig = sum(cost_elec_input[i:dur_max[i] + 1])
            cost_new = sum(heapq.nsmallest(count_flex_ts, cost_modified))
            cost_diff_pos[i] = (cost_new  / count_flex_ts) * 1.15 * (1 - idx_no_flex[i])
        else:
            cost_modified = (-hp_operation[dur_max[i] + 1:] + 1) * (-100) + \
                            list(map(float, cost_elec_input[dur_max[i] + 1:]))
            # cost_orig = sum(heapq.nsmallest(count_flex_ts, cost_modified))
            cost_new = sum(heapq.nlargest(count_flex_ts, cost_modified))
            cost_diff_neg[i] = (-cost_new / count_flex_ts) * 0.85 * (1 - idx_no_flex[i])

    # write the results in data
    timeslots = list(ems['time_data']['time_slots'])
    # 'times': pd.date_range(start="00:00", end="23:59", freq='15min').strftime('%H:%M')
    data = {
            # 'time': timeslots,
            'Sch_P': pow_schedual,
            'Neg_P': pow_neg,
            'Pos_P': pow_pos,
            'Neg_E': energy_neg,
            'Pos_E': energy_pos,
            'Neg_Pr': cost_diff_neg,
            'Pos_Pr': cost_diff_pos,
            }
    flexopts = pd.DataFrame(data)
    # flexopts.set_index('Sch_P')

    return flexopts


if __name__ == '__main__':
    my_ems = ems_loc(initialize=True, path='../ems/test_chp.txt')
    my_ems['flexopts']['hp'] = calc_flex_hp(my_ems)
    # plot_flex(my_ems, 'hp')
    # save_results(my_ems['flexopts']['hp'], "C:\data" + "\hauhalte1_hp.csv")
