"""
The "flex_chp.py" quantifies the flexibility of combined heat and power
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
import heapq


from opentumflex.configuration.init_ems import ems as ems_loc


def calc_flex_chp(ems):  # datafram open and break it down

    optm_df = pd.DataFrame.from_dict(ems['optplan'])
    timesteps = len(optm_df['CHP_operation'])
    ntsteps = ems['time_data']['ntsteps']
    pow2energy = 1 / ntsteps
    # get the values from hp dataframe

    chp_operation = optm_df['CHP_operation']
    chp_heat_ifrun = optm_df['CHP_heat_run']
    chp_elec_ifrun = optm_df['CHP_elec_run']
    chp_gas_ifrun = optm_df['CHP_gas_run']
    soc_heat = optm_df['SOC_heat']
    chp_heat_pow = chp_operation * chp_heat_ifrun
    chp_elec_pow = chp_operation * chp_elec_ifrun
    chp_gas_pow = chp_operation * chp_gas_ifrun

    # get the values of heat storage
    hs_param = ems['devices']['sto']
    hs_cap = hs_param['stocap']  # kWh
    hs_soc_init = hs_param['initSOC']
    hs_soc_end = 0.5
    hs_eta = 0.98
    hs_self_discharge = 0.0005

    # get the max duration of flexibility for every time step

    # max duration from the optimal operation
    dur_max_opt = np.zeros(timesteps)

    for i in range(timesteps):
        if chp_operation[i] > 0:
            dur_max_opt[i] = next((x for x, val in enumerate(chp_operation[i:]) if val == 0), timesteps - i) + i - 1
        else:
            dur_max_opt[i] = next((x for x, val in enumerate(chp_operation[i:]) if val > 0), timesteps - i) + i - 1

    # max duration from available regeneration time

    dur_max_reg = np.zeros(timesteps)
    for i in range(timesteps):
        if chp_operation[i] > 0:
            # dur_max_reg[i] = i + sum(1-chp_operation[i:]) - 1
            dur_max_reg[i] = min(i + sum(1 - chp_operation[i:]) - 1, timesteps)
        else:
            # dur_max_reg[i] = i + sum(chp_operation[i:]) - 1
            dur_max_reg[i] = min(i + sum(chp_operation[i:]) - 1, timesteps)
    # max duration from storage capacity
    dur_max_sto = np.zeros(timesteps)

    # on/off states to soc change

    soc_change = chp_heat_ifrun * pow2energy / hs_cap * (0.5 - chp_operation) * 2 * 100
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

    pow_schedual = chp_elec_pow
    pow_pos = chp_elec_ifrun - chp_elec_pow
    pow_neg = -pow_schedual
    energy_pos = np.zeros(timesteps)
    energy_neg = np.zeros(timesteps)
    idx_no_flex = np.zeros(timesteps)
    for i in range(timesteps):
        if dur_max[i] < i:  # which means the flexibility is not available in this time step
            idx_no_flex[i] = 1
            pow_pos[i] = 0
            pow_neg[i] = 0
            dur_max[i] = i
        if chp_operation[i] > 0:
            energy_neg[i] = pow2energy * pow_neg[i] * (dur_max[i] - i + 1)
        else:
            energy_pos[i] = pow2energy * pow_pos[i] * (dur_max[i] - i + 1)

    # get the price

    cost_elec_input = list(map(float, list(ems['fcst']['ele_price_in'])))
    cost_elec_output = list(map(float, list(ems['fcst']['ele_price_out'])))
    # cost_gas_input = pd.DataFrame.from_dict(opentumflex['fcst']['gas'], orient='index')[0]
    cost_gas_input = list(ems['fcst']['gas'])
    # cost_elec_input = opentumflex['optplan']['elec_supply_price']
    cost_diff_pos = np.zeros(timesteps)
    cost_diff_neg = np.zeros(timesteps)
    for i in range(timesteps):
        count_flex_ts = dur_max[i] - i + 1
        if chp_operation[i] > 0:
            cost_modified = list(map(float, cost_elec_input[dur_max[i] + 1:])) + chp_operation[dur_max[i] + 1:] * (-100)
            # cost_elec_modified = list(map(float, cost_elec_input[dur_max[i] + 1:])) + \
            #                     (1 - chp_operation[dur_max[i] + 1:]) * 0.1
            # cost_orig = sum(cost_gas_input[i:dur_max[i] + 1])
            #                 + sum(heapq.nsmallest(count_flex_ts, cost_elec_modified))
            # cost_new = sum(heapq.nsmallest(count_flex_ts, cost_modified)) + sum(cost_elec_input[i:dur_max[i] + 1])
            cost_new = sum(heapq.nlargest(count_flex_ts, cost_modified))
            cost_diff_neg[i] = (-cost_new / count_flex_ts) * 0.85 * (1-idx_no_flex[i])
        else:
            cost_modified = (-chp_operation[dur_max[i] + 1:] + 1) * 100 + \
                            list(map(float, cost_elec_input[dur_max[i] + 1:]))
            # cost_elec_modified = list(map(float, cost_elec_input[dur_max[i] + 1:]))
            # cost_orig = sum(heapq.nsmallest(count_flex_ts, cost_modified)) + sum(cost_elec_input[i:dur_max[i] + 1])
            # cost_new = sum(cost_gas_input[i:dur_max[i] + 1]) + sum(heapq.nlargest(count_flex_ts, cost_elec_modified))
            cost_new = sum(heapq.nsmallest(count_flex_ts, cost_modified))
            cost_diff_pos[i] = (cost_new / count_flex_ts) * 1.15 * (1-idx_no_flex[i])

    # write the results in data

    # 'times': pd.date_range(start="00:00", end="23:59", freq='15min').strftime('%H:%M')
    data = {# 'time': pd.date_range(start="00:00", end="23:59", freq='15min').strftime('%H:%M'),
            'Sch_P': pow_schedual,
            'Neg_P': pow_neg,
            'Pos_P': pow_pos,
            'Neg_E': energy_neg,
            'Pos_E': energy_pos,
            'Neg_Pr': cost_diff_neg,
            'Pos_Pr': cost_diff_pos
            }
    flexopts = pd.DataFrame(data)
    ems['flexopts']['chp'] = flexopts

    return ems


if __name__ == '__main__':

    my_ems = ems_loc(initialize=True, path='C:/Users/ge57vam/emsflex/opentumflex/test_chp.txt')
    my_ems['flexopts']['chp'] = calc_flex_chp(my_ems)
    plot_flex(my_ems, 'chp')
   # save_results(my_ems['flexopts']['hp'])
