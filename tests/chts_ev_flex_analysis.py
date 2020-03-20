import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sb

from ems.ems_mod import ems as ems_loc
from forecast import price_fcst

# Prepare memory variables for analysis
results_tou = list()
results_const = list()

"""
Setup of analysis data frame
"""
# minimal and maximal time of all files (known)
t_min = pd.Timestamp('2012-02-01 11:30:00')
t_max = pd.Timestamp('2013-02-04 06:15:00')
# Date range from minimal to maximal time
t_range = pd.date_range(start=t_min, end=t_max, freq='15Min')
# Create df for sum of optimal charging plans
chts_opt_sum_df = pd.DataFrame(0, index=t_range, columns={'P_ev_opt_sum_tou',
                                                          'P_ev_opt_sum_const',
                                                          'n_veh_avail_tou',
                                                          'n_veh_avail_const',
                                                          'c_elect_in_tou',
                                                          'c_elect_in_const'})
# Get forecast electricity prices for each time step
price_forecast = price_fcst.get_elect_price_fcst(t_start=t_min, t_end=t_max)
chts_opt_sum_df.loc[:, 'c_elect_in_tou'] = price_forecast['ToU']
chts_opt_sum_df.loc[:, 'c_elect_in_const'] = price_forecast['Constant']
# Create a daytime identifier for weekday and time for heat map
chts_opt_sum_df['Daytime_ID'] = chts_opt_sum_df.index.weekday_name.array + \
                                ', ' + \
                                chts_opt_sum_df.index.strftime('%H:%M').array
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

"""
ToU Analysis
"""
# List all files in a directory using os.listdir
file_names_tou = os.listdir('C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/ToU/')

# read all results and save them in memory
for result_name in file_names_tou:
    my_ems = ems_loc(initialize=True,
                     path='C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/ToU/' + result_name)
    results_tou.append(my_ems)

# optimal charging plan
for i in range(len(results_tou)):
    opt_result_df = pd.DataFrame(results_tou[i]['optplan']['EV_power'],
                                 columns={'P_ev_opt'},
                                 index=pd.date_range(start=results_tou[i]['time_data']['time_slots'][0],
                                                     end=results_tou[i]['time_data']['time_slots'][-1], freq='15Min'))

    chts_opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_tou'] += opt_result_df['P_ev_opt']
    chts_opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'n_veh_avail_tou'] += 1

"""
Constant electricity price analysis
"""
# List all files in a directory using os.listdir
file_names_const = os.listdir('C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/Constant/')

# read all results and save them in memory
for result_name in file_names_const:
    my_ems = ems_loc(initialize=True,
                     path='C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/Constant/' + result_name)
    results_const.append(my_ems)

# optimal charging plan
for i in range(len(results_const)):
    opt_result_df = pd.DataFrame(results_const[i]['optplan']['EV_power'],
                                 columns={'P_ev_opt'},
                                 index=pd.date_range(start=results_const[i]['time_data']['time_slots'][0],
                                                     end=results_const[i]['time_data']['time_slots'][-1], freq='15Min'))

    chts_opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_const'] += opt_result_df['P_ev_opt']
    chts_opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'n_veh_avail_const'] += 1

"""
Optimal charging schedule analysis
"""
# Subplots
fig, axs = plt.subplots(nrows=3, ncols=1, sharex=True)
# number of available vehicles
axs[0].plot(chts_opt_sum_df['n_veh_avail_const'], color='k', label='Constant electricity prices')
axs[0].plot(chts_opt_sum_df['n_veh_avail_tou'], color='g', label='ToU electricity prices')
axs[0].set_ylabel('# of available vehicles')
axs[0].grid()
axs[0].legend()
axs[1].plot(chts_opt_sum_df['P_ev_opt_sum_const'], color='k', label='Constant electricity prices')
axs[1].plot(chts_opt_sum_df['P_ev_opt_sum_tou'], color='g', label='ToU electricity prices')
axs[1].hlines((chts_opt_sum_df.nlargest(round(len(t_range) * 0.01), 'P_ev_opt_sum_const')['P_ev_opt_sum_const'] /
               chts_opt_sum_df.nlargest(round(len(t_range) * 0.01), 'P_ev_opt_sum_const')['n_veh_avail_tou']).mean() *
              chts_opt_sum_df['n_veh_avail_tou'].max(),
              t_min, t_max, color='black')
axs[1].hlines((chts_opt_sum_df.nlargest(round(len(t_range) * 0.01), 'P_ev_opt_sum_tou')['P_ev_opt_sum_tou'] /
               chts_opt_sum_df.nlargest(round(len(t_range) * 0.01), 'P_ev_opt_sum_tou')['n_veh_avail_tou']).mean() *
              chts_opt_sum_df['n_veh_avail_tou'].max(),
              t_min, t_max, color='g')
axs[1].set_ylabel('Charging power [kW]')
axs[1].grid()
axs[1].legend()
axs[2].plot(chts_opt_sum_df['c_elect_in_const'], color='k', label='Constant electricity prices')
axs[2].plot(chts_opt_sum_df['c_elect_in_tou'], color='g', label='ToU electricity prices')
axs[2].set_ylabel('Electricity cost [$/kWh]')
axs[2].grid()
axs[2].legend()
axs[2].set_xlabel('Date')

# Retrieve the maximum power of each day
max_values_per_day = chts_opt_sum_df.groupby(chts_opt_sum_df.index.floor('d')).max().reset_index()

# Subplots
fig, axs = plt.subplots(nrows=2, ncols=1, sharex=True)
# Plot maximum power per day
axs[0].bar(max_values_per_day['index'], max_values_per_day['P_ev_opt_sum_tou'],
           color='green', label='ToU electricity prices', zorder=5)
axs[0].bar(max_values_per_day['index'], max_values_per_day['P_ev_opt_sum_const'],
           color='black', label='Constant electricity prices', zorder=0)
axs[0].set_ylabel('Daily maximal power [kW]')
axs[0].grid()
axs[0].legend()
# Plot difference in maximal power between constant and tou prices
axs[1].bar(max_values_per_day['index'], max_values_per_day['P_ev_opt_sum_tou']-max_values_per_day['P_ev_opt_sum_const'])
axs[1].hlines((max_values_per_day['P_ev_opt_sum_tou']-max_values_per_day['P_ev_opt_sum_const']).mean(),
              t_min.floor('d'), t_max.floor('d'), label='Mean difference')
axs[1].set_xlabel('Date')
axs[1].set_ylabel('P_max_tou - P_max_const [kW]')
axs[1].grid()

# Prepare heat map for optimal charging power
chts_opt_per_daytime = chts_opt_sum_df.groupby(by='Daytime_ID').mean()
# prepare df for week heat map
P_opt_sum_tou_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                columns=days)
P_opt_sum_const_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                  columns=days)
# P_opt_sum_tou_hm = P_opt_sum_tou_hm.drop(index='')     # drop first column with no index
# P_opt_sum_const_hm = P_opt_sum_const_hm.drop(index='')     # drop first column with no index

for i in range(7):
    P_opt_sum_tou_hm[chts_opt_per_daytime.index[i*96][:3]].iloc[:] = chts_opt_per_daytime['P_ev_opt_sum_tou'].iloc[i*96:i*96+96].values
    P_opt_sum_const_hm[chts_opt_per_daytime.index[i*96][:3]].iloc[:] = chts_opt_per_daytime['P_ev_opt_sum_const'].iloc[i*96:i*96+96].values

plt.figure()
sb.heatmap(P_opt_sum_tou_hm)
plt.figure()
sb.heatmap(P_opt_sum_const_hm)

"""
Analysis of ev flexibility
"""