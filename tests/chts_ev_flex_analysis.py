import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sb

from ems.ems_mod import ems as ems_loc
from forecast import price_fcst

"""
#################################################################
# Preparation ###################################################
#################################################################
"""
# minimal and maximal time of all files (known)
t_min = pd.Timestamp('2012-02-01 11:30:00')
t_max = pd.Timestamp('2013-02-04 06:15:00')
# Date range from minimal to maximal time
t_range = pd.date_range(start=t_min, end=t_max, freq='15Min')
# Create df for sum of optimal charging plans
chts_opt_sum_df = pd.DataFrame(0, index=t_range, columns={'P_ev_opt_sum_tou',
                                                          'P_ev_opt_sum_const',
                                                          'P_ev_opt_sum_tou_mi',
                                                          'P_ev_opt_sum_const_mi',
                                                          'n_veh_avail',
                                                          'c_elect_in_tou',
                                                          'c_elect_in_const',
                                                          'c_elect_in_tou_mi',
                                                          'c_elect_in_const_mi',
                                                          'Daytime_ID'})
# Get forecast electricity prices for each time step
price_forecast = price_fcst.get_elect_price_fcst(t_start=t_min, t_end=t_max, pr_constant=0.19)
chts_opt_sum_df.loc[:, 'c_elect_in_tou'] = price_forecast['ToU']
chts_opt_sum_df.loc[:, 'c_elect_in_const'] = price_forecast['Constant']
chts_opt_sum_df.loc[:, 'c_elect_in_tou_mi'] = price_forecast['ToU_minimally_increasing']
chts_opt_sum_df.loc[:, 'c_elect_in_const_mi'] = price_forecast['Constant_minimally_increasing']
# Create a daytime identifier for weekday and time for heat map
chts_opt_sum_df['Daytime_ID'] = chts_opt_sum_df.index.weekday_name.array + \
                                ', ' + \
                                chts_opt_sum_df.index.strftime('%H:%M').array
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


"""
####################################################################
# Read ems results, sum charging power and veh availability ########
####################################################################
"""
# List all file names, for all scenarios (ToU & Constant, with and without minimally increasing prices) the same
file_names = os.listdir('C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/ToU/')

# read all results and store them in result lists
for result_name in file_names:
    my_ems_tou_mi = ems_loc(initialize=True,
                            path='C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/'
                                 'ToU_with_price_increment/'
                                 + result_name)
    my_ems_tou = ems_loc(initialize=True,
                         path='C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/ToU/'
                              + result_name)
    my_ems_const_mi = ems_loc(initialize=True,
                              path='C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/'
                                   'Constant_with_price_increment/'
                                   + result_name)
    my_ems_const = ems_loc(initialize=True,
                           path='C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/Constant/'
                                + result_name)

    opt_result_df = pd.DataFrame({'P_ev_opt_tou_mi': my_ems_tou_mi['optplan']['EV_power'],
                                  'P_ev_opt_tou': my_ems_tou['optplan']['EV_power'],
                                  'P_ev_opt_const_mi': my_ems_const_mi['optplan']['EV_power'],
                                  'P_ev_opt_const': my_ems_const['optplan']['EV_power']},
                                 index=pd.date_range(start=my_ems_tou_mi['time_data']['time_slots'][0],
                                                     end=my_ems_tou_mi['time_data']['time_slots'][-1],
                                                     freq='15Min'))

    chts_opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_tou_mi'] \
        += opt_result_df['P_ev_opt_tou_mi']
    chts_opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_tou'] \
        += opt_result_df['P_ev_opt_tou']
    chts_opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_const_mi'] \
        += opt_result_df['P_ev_opt_const_mi']
    chts_opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_const'] \
        += opt_result_df['P_ev_opt_const']
    chts_opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'n_veh_avail'] += 1


"""
####################################################################
# Optimal charging schedule analysis ###############################
####################################################################
"""
# Subplots
fig1, axs = plt.subplots(nrows=4, ncols=1, sharex=True)
# number of available vehicles
axs[0].plot(chts_opt_sum_df['n_veh_avail'], color='k')
axs[0].set_ylabel('# of available vehicles')
axs[0].grid()
# Cumulated power for ev charging
axs[1].plot(chts_opt_sum_df['P_ev_opt_sum_const'], color='k', label='Constant prices', zorder=5)
axs[1].plot(chts_opt_sum_df['P_ev_opt_sum_tou'], color='g', label='ToU prices', zorder=0)
axs[1].hlines((chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_const')['P_ev_opt_sum_const'] /
               chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_const')['n_veh_avail']).mean() *
              chts_opt_sum_df['n_veh_avail'].max(),
              t_min, t_max, color='black')
axs[1].hlines((chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_tou')['P_ev_opt_sum_tou'] /
               chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_tou')['n_veh_avail']).mean() *
              chts_opt_sum_df['n_veh_avail'].max(),
              t_min, t_max, color='g')
axs[1].set_ylabel('Charging power [kW]')
axs[1].grid()
axs[1].legend()
# Cumulated power for ev charging with minimal price increments
axs[2].plot(chts_opt_sum_df['P_ev_opt_sum_const_mi'], color='k', label='Constant prices minimally increasing', zorder=5)
axs[2].plot(chts_opt_sum_df['P_ev_opt_sum_tou_mi'], color='g', label='ToU prices minimally increasing', zorder=0)
axs[2].hlines((chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_const_mi')['P_ev_opt_sum_const_mi'] /
               chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_const_mi')['n_veh_avail']).mean() *
              chts_opt_sum_df['n_veh_avail'].max(),
              t_min, t_max, color='black')
axs[2].hlines((chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_tou_mi')['P_ev_opt_sum_tou_mi'] /
               chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_tou_mi')['n_veh_avail']).mean() *
              chts_opt_sum_df['n_veh_avail'].max(),
              t_min, t_max, color='g')
axs[2].set_ylabel('Charging power [kW]')
axs[2].grid()
axs[2].legend()
# Electricity cost
axs[3].plot(chts_opt_sum_df['c_elect_in_const'], color='k', label='Constant prices', zorder=5)
axs[3].plot(chts_opt_sum_df['c_elect_in_tou'], color='g', label='ToU prices', zorder=0)
axs[3].set_ylabel('Electricity cost [$/kWh]')
axs[3].grid()
axs[3].legend()
axs[3].set_xlabel('Date')

"""
####################################################################
# Maximum power per day analysis ###################################
####################################################################
"""
max_values_per_day = chts_opt_sum_df.groupby(chts_opt_sum_df.index.floor('d')).max().reset_index()

# Subplots
fig2, axs = plt.subplots(nrows=4, ncols=2, sharex=True, sharey=True)
# Plot maximum power per day
axs[0, 0].set_title('ToU and constant prices')
axs[0, 0].bar(max_values_per_day['index'], max_values_per_day['P_ev_opt_sum_tou'],
              color='green', label='ToU prices', zorder=0)
axs[0, 0].bar(max_values_per_day['index'], max_values_per_day['P_ev_opt_sum_const'],
              color='black', label='Constant prices', zorder=5)
axs[0, 0].set_ylabel('Daily maximal power [kW]')
axs[0, 0].grid()
axs[0, 0].legend()
# Plot difference in maximal power between constant and tou prices
axs[0, 1].bar(max_values_per_day['index'],
              max_values_per_day['P_ev_opt_sum_tou'] - max_values_per_day['P_ev_opt_sum_const'],
              label='P_max_tou - P_max_const')
axs[0, 1].hlines((max_values_per_day['P_ev_opt_sum_tou']-max_values_per_day['P_ev_opt_sum_const']).mean(),
                 t_min.floor('d'), t_max.floor('d'), label='Average difference')
axs[0, 1].set_xlabel('Date')
axs[0, 1].set_ylabel('Power difference [kW]')
axs[0, 1].legend()
axs[0, 1].grid()
# Plot maximum power per day
axs[1, 0].set_title('ToU and constant prices minimally increasing')
axs[1, 0].bar(max_values_per_day['index'], max_values_per_day['P_ev_opt_sum_tou_mi'],
              color='green', label='ToU prices minimally increasing', zorder=0)
axs[1, 0].bar(max_values_per_day['index'], max_values_per_day['P_ev_opt_sum_const_mi'],
              color='black', label='Constant prices minimally increasing', zorder=5)
axs[1, 0].set_ylabel('Daily maximal power [kW]')
axs[1, 0].grid()
axs[1, 0].legend()
# Plot difference in maximal power between constant and tou prices
axs[1, 1].bar(max_values_per_day['index'],
              max_values_per_day['P_ev_opt_sum_tou_mi']-max_values_per_day['P_ev_opt_sum_const_mi'],
              label='P_max_tou_mi - P_max_const_mi')
axs[1, 1].hlines((max_values_per_day['P_ev_opt_sum_tou_mi']-max_values_per_day['P_ev_opt_sum_const_mi']).mean(),
                 t_min.floor('d'), t_max.floor('d'), label='Average difference')
axs[1, 1].set_xlabel('Date')
axs[1, 1].set_ylabel('Power difference [kW]')
axs[1, 1].legend()
axs[1, 1].grid()
# Plot maximum power per day
axs[2, 0].set_title('ToU prices and minimally increasing ToU prices')
axs[2, 0].bar(max_values_per_day['index'], max_values_per_day['P_ev_opt_sum_tou_mi'],
              color='green', label='ToU prices minimally increasing', zorder=0)
axs[2, 0].bar(max_values_per_day['index'], max_values_per_day['P_ev_opt_sum_tou'],
              color='black', label='ToU prices', zorder=5)
axs[2, 0].set_ylabel('Daily maximal power [kW]')
axs[2, 0].grid()
axs[2, 0].legend()
# Plot difference in maximal power between constant and tou prices
axs[2, 1].bar(max_values_per_day['index'],
              max_values_per_day['P_ev_opt_sum_tou_mi']-max_values_per_day['P_ev_opt_sum_tou'],
              label='P_max_tou_mi - P_max_tou')
axs[2, 1].hlines((max_values_per_day['P_ev_opt_sum_tou_mi']-max_values_per_day['P_ev_opt_sum_tou']).mean(),
                 t_min.floor('d'), t_max.floor('d'), label='Average difference')
axs[2, 1].set_xlabel('Date')
axs[2, 1].set_ylabel('Power difference [kW]')
axs[2, 1].grid()
axs[2, 1].legend()
# Plot maximum power per day
axs[3, 0].set_title('Constant prices and minimally increasing prices')
axs[3, 0].bar(max_values_per_day['index'], max_values_per_day['P_ev_opt_sum_const_mi'],
              color='green', label='Constant prices minimally increasing', zorder=0)
axs[3, 0].bar(max_values_per_day['index'], max_values_per_day['P_ev_opt_sum_const'],
              color='black', label='Constant prices', zorder=5)
axs[3, 0].set_ylabel('Daily maximal power [kW]')
axs[3, 0].grid()
axs[3, 0].legend()
# Plot difference in maximal power between constant and tou prices
axs[3, 1].bar(max_values_per_day['index'],
              max_values_per_day['P_ev_opt_sum_const_mi']-max_values_per_day['P_ev_opt_sum_const'],
              label='P_max_const_mi - P_max_const')
axs[3, 1].hlines((max_values_per_day['P_ev_opt_sum_const_mi']-max_values_per_day['P_ev_opt_sum_const']).mean(),
                 t_min.floor('d'), t_max.floor('d'), label='Mean difference')
axs[3, 1].set_xlabel('Date')
axs[3, 1].set_ylabel('Power difference [kW]')
axs[3, 1].grid()
axs[3, 1].legend()

"""
####################################################################
# Average charging power per time step and day of week #############
####################################################################
"""

# Prepare heat map for optimal charging power
chts_opt_per_daytime = pd.DataFrame()
chts_opt_per_daytime_temp = chts_opt_sum_df.groupby(by='Daytime_ID').mean()
chts_opt_per_daytime = chts_opt_per_daytime.append(chts_opt_per_daytime_temp.iloc[96:192, :])
chts_opt_per_daytime = chts_opt_per_daytime.append(chts_opt_per_daytime_temp.iloc[480:, :])
chts_opt_per_daytime = chts_opt_per_daytime.append(chts_opt_per_daytime_temp.iloc[384:480, :])
chts_opt_per_daytime = chts_opt_per_daytime.append(chts_opt_per_daytime_temp.iloc[0:96, :])
chts_opt_per_daytime = chts_opt_per_daytime.append(chts_opt_per_daytime_temp.iloc[192:384, :])
# prepare df for week heat map
P_opt_sum_tou_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                columns=days)
P_opt_sum_const_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                  columns=days)
P_opt_sum_tou_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                   columns=days)
P_opt_sum_const_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                     columns=days)
n_avail_veh_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                              columns=days)

# Write days to
for i in range(7):
    P_opt_sum_tou_hm[chts_opt_per_daytime.index[i*96][:3]].iloc[:] = chts_opt_per_daytime['P_ev_opt_sum_tou'].iloc[i*96:i*96+96].values
    P_opt_sum_const_hm[chts_opt_per_daytime.index[i*96][:3]].iloc[:] = chts_opt_per_daytime['P_ev_opt_sum_const'].iloc[i*96:i*96+96].values
    P_opt_sum_tou_mi_hm[chts_opt_per_daytime.index[i*96][:3]].iloc[:] = chts_opt_per_daytime['P_ev_opt_sum_tou_mi'].iloc[i*96:i*96+96].values
    P_opt_sum_const_mi_hm[chts_opt_per_daytime.index[i*96][:3]].iloc[:] = chts_opt_per_daytime['P_ev_opt_sum_const_mi'].iloc[i*96:i*96+96].values
    n_avail_veh_hm[chts_opt_per_daytime.index[i*96][:3]].iloc[:] = chts_opt_per_daytime['n_veh_avail'].iloc[i*96:i*96+96].values

# Charging power
fig3, axs = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
sb.heatmap(P_opt_sum_tou_hm, ax=axs[0, 0], cbar_kws={'label': 'Average charging power [kW]'}, vmin=0, vmax=20)
axs[0, 0].set_title('ToU prices')
sb.heatmap(P_opt_sum_const_hm, ax=axs[0, 1], cbar_kws={'label': 'Average charging power [kW]'}, vmin=0, vmax=20)
axs[0, 1].set_title('Constant prices')
sb.heatmap(P_opt_sum_tou_mi_hm, ax=axs[1, 0], cbar_kws={'label': 'Average charging power [kW]'}, vmin=0, vmax=20)
axs[1, 0].set_title('ToU prices minimally increasing')
sb.heatmap(P_opt_sum_const_mi_hm, ax=axs[1, 1], cbar_kws={'label': 'Average charging power [kW]'}, vmin=0, vmax=20)
axs[1, 1].set_title('Constant prices minimally increasing')

"""
####################################################################
# Average number of available vehicles #############################
####################################################################
"""
# Average vehicle availabilities
plt.figure()
plt.title('Average vehicle availability')
sb.heatmap(n_avail_veh_hm, vmin=0, vmax=8)
# plt.figure()
# plt.plot(chts_opt_per_daytime['n_veh_avail'])
