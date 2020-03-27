import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sb


"""
####################################################################
# Read data from hdf files #########################################
####################################################################
"""
chts_opt_sum_df = pd.read_hdf('C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/Aggregated Data/chts_opt_sum_data.h5', key='df')
chts_flex_sum_df = pd.read_hdf('C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/Aggregated Data/chts_flex_sum_data.h5', key='df')
# minimal and maximal time of all files (known)
t_min = min(chts_flex_sum_df.index)
t_max = max(chts_flex_sum_df.index)
# Date range from minimal to maximal time
t_range = pd.date_range(start=t_min, end=t_max, freq='15Min')
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

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
