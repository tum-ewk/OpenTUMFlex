import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sb
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

"""
####################################################################
# Read data from hdf files #########################################
####################################################################
"""
chts_flex_sum_df = pd.read_hdf('C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/Aggregated Data/chts_flex_sum_data.h5', key='df')
chts_opt_sum_df = pd.read_hdf('C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/Aggregated Data/chts_opt_sum_data.h5', key='df')
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
axs[1].plot(chts_opt_sum_df['P_ev_opt_sum_const'], color='k', label='Constant prices', zorder=5, linestyle='solid')
axs[1].plot(chts_opt_sum_df['P_ev_opt_sum_tou'], color='g', label='ToU prices', zorder=0, linestyle='dashed')
axs[1].plot(chts_opt_sum_df['P_ev_opt_sum_const_mi'], color='k', label='Constant prices minimally increasing',
            zorder=5, linestyle='dashdot')
axs[1].plot(chts_opt_sum_df['P_ev_opt_sum_tou_mi'], color='g', label='ToU prices minimally increasing',
            zorder=0, linestyle='dotted')
axs[1].hlines((chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_const_mi')['P_ev_opt_sum_const_mi'] /
               chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_const_mi')['n_veh_avail']).mean() *
              chts_opt_sum_df['n_veh_avail'].max(),
              t_min, t_max, color='black', linestyle='dashdot')
axs[1].hlines((chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_tou_mi')['P_ev_opt_sum_tou_mi'] /
               chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_tou_mi')['n_veh_avail']).mean() *
              chts_opt_sum_df['n_veh_avail'].max(),
              t_min, t_max, color='g', linestyle='dotted')
axs[1].hlines((chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_const')['P_ev_opt_sum_const'] /
               chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_const')['n_veh_avail']).mean() *
              chts_opt_sum_df['n_veh_avail'].max(),
              t_min, t_max, color='black', linestyle='solid')
axs[1].hlines((chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_tou')['P_ev_opt_sum_tou'] /
               chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_tou')['n_veh_avail']).mean() *
              chts_opt_sum_df['n_veh_avail'].max(),
              t_min, t_max, color='g', linestyle='dashed')
axs[1].set_ylabel('Charging power [kW]')
axs[1].grid()
axs[1].legend()
# Cumulated power for ev charging with minimal price increments
axs[2].plot(chts_flex_sum_df['P_pos_sum_const'], color='k', label='Constant prices', zorder=5, linestyle='solid')
axs[2].plot(chts_flex_sum_df['P_pos_sum_const_mi'], color='g', label='ToU prices', zorder=0, linestyle='dashdot')
axs[2].plot(chts_flex_sum_df['P_pos_sum_tou'], color='k', label='Constant prices minimally increasing',
            zorder=5, linestyle='dashed')
axs[2].plot(chts_flex_sum_df['P_pos_sum_tou_mi'], color='g', label='ToU prices minimally increasing',
            zorder=0, linestyle='dotted')
axs[2].plot(chts_flex_sum_df['P_neg_sum_const'], color='k', zorder=5, linestyle='solid')
axs[2].plot(chts_flex_sum_df['P_neg_sum_const_mi'], color='g', zorder=0, linestyle='dashdot')
axs[2].plot(chts_flex_sum_df['P_neg_sum_tou'], color='k', zorder=5, linestyle='dashed')
axs[2].plot(chts_flex_sum_df['P_neg_sum_tou_mi'], color='g', zorder=0, linestyle='dotted')
axs[2].set_ylabel('Flexible power [kW]')
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
chts_opt_per_daytime = chts_opt_per_daytime.reset_index()
# Prepare heat map for flexible power
chts_flex_per_daytime = pd.DataFrame()
chts_flex_per_daytime_temp = chts_flex_sum_df.groupby(by='Daytime_ID').mean()
chts_flex_per_daytime = chts_flex_per_daytime.append(chts_flex_per_daytime_temp.iloc[96:192, :])
chts_flex_per_daytime = chts_flex_per_daytime.append(chts_flex_per_daytime_temp.iloc[480:, :])
chts_flex_per_daytime = chts_flex_per_daytime.append(chts_flex_per_daytime_temp.iloc[384:480, :])
chts_flex_per_daytime = chts_flex_per_daytime.append(chts_flex_per_daytime_temp.iloc[0:96, :])
chts_flex_per_daytime = chts_flex_per_daytime.append(chts_flex_per_daytime_temp.iloc[192:384, :])
chts_flex_per_daytime = chts_flex_per_daytime.reset_index()

# prepare df for week heat map
P_pos_sum_tou_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                columns=days)
P_pos_sum_const_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                  columns=days)
P_pos_sum_tou_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                   columns=days)
P_pos_sum_const_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                     columns=days)
P_neg_sum_tou_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                columns=days)
P_neg_sum_const_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                  columns=days)
P_neg_sum_tou_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                   columns=days)
P_neg_sum_const_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                     columns=days)
n_avail_veh_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                              columns=days)

# Copy power to single day columns
for i in range(7):
    P_pos_sum_tou_hm[days[i]].iloc[:] = chts_flex_per_daytime['P_pos_sum_tou'].iloc[i*96:i*96+96].values
    P_pos_sum_const_hm[days[i]].iloc[:] = chts_flex_per_daytime['P_pos_sum_const'].iloc[i*96:i*96+96].values
    P_pos_sum_tou_mi_hm[days[i]].iloc[:] = chts_flex_per_daytime['P_pos_sum_tou_mi'].iloc[i*96:i*96+96].values
    P_pos_sum_const_mi_hm[days[i]].iloc[:] = chts_flex_per_daytime['P_pos_sum_const_mi'].iloc[i*96:i*96+96].values
    P_neg_sum_tou_hm[days[i]].iloc[:] = chts_flex_per_daytime['P_neg_sum_tou'].iloc[i*96:i*96+96].values
    P_neg_sum_const_hm[days[i]].iloc[:] = chts_flex_per_daytime['P_neg_sum_const'].iloc[i*96:i*96+96].values
    P_neg_sum_tou_mi_hm[days[i]].iloc[:] = chts_flex_per_daytime['P_neg_sum_tou_mi'].iloc[i*96:i*96+96].values
    P_neg_sum_const_mi_hm[days[i]].iloc[:] = chts_flex_per_daytime['P_neg_sum_const_mi'].iloc[i*96:i*96+96].values

# Charging power
fig3, axs = plt.subplots(nrows=4, ncols=2, sharex=True, sharey=True)
cm = ['Greens', 'Blues_r']
pcm = axs[0, 0].pcolormesh(P_pos_sum_tou_hm, vmin=0, vmax=20, cmap='Greens')
axs[0, 0].set_title('ToU prices')
sb.heatmap(P_pos_sum_const_hm, ax=axs[1, 0], cbar=False, vmin=0, vmax=20, cmap='Greens')
axs[1, 0].set_title('Constant prices')
sb.heatmap(P_pos_sum_tou_mi_hm, ax=axs[2, 0], cbar=False, vmin=0, vmax=20, cmap='Greens')
axs[2, 0].set_title('ToU prices minimally increasing')
sb.heatmap(P_pos_sum_const_mi_hm, ax=axs[3, 0], cbar=False, vmin=0, vmax=20, cmap='Greens')
axs[3, 0].set_title('Constant prices minimally increasing')
fig3.colorbar(pcm, ax=axs[:, 0], shrink=0.6, label='Positive flexible power [kW]')
axs[0, 0].set_xticklabels(P_pos_sum_const_hm.columns)
axs[0, 0].set_yticklabels(P_pos_sum_const_hm.index)

pcm = axs[0, 1].pcolormesh(P_neg_sum_tou_hm, vmin=-50, vmax=0, cmap='Blues_r')
axs[0, 1].set_title('ToU prices')
sb.heatmap(P_neg_sum_const_hm, ax=axs[1, 1], cbar=False, vmin=-50, vmax=0, cmap='Blues_r')
axs[1, 1].set_title('Constant prices')
sb.heatmap(P_neg_sum_tou_mi_hm, ax=axs[2, 1], cbar=False, vmin=-50, vmax=0, cmap='Blues_r')
axs[2, 1].set_title('ToU prices minimally increasing')
sb.heatmap(P_neg_sum_const_mi_hm, ax=axs[3, 1], cbar=False, vmin=-50, vmax=0, cmap='Blues_r')
axs[3, 1].set_title('Constant prices minimally increasing')
fig3.colorbar(pcm, ax=axs[:, 1], shrink=0.6, label='Negative flexible power [kW]')

"""
Plot average flexibility over time
"""
# Subplots
fig4, axs = plt.subplots(nrows=4, ncols=1, sharex=True)
# number of available vehicles
axs[0].plot(chts_opt_per_daytime.index+1, chts_opt_per_daytime['n_veh_avail'], color='k')
axs[0].set_ylabel('# of available vehicles')
axs[0].grid()
# Cumulated power for ev charging
axs[1].plot(chts_opt_per_daytime.index+1, chts_opt_per_daytime['P_ev_opt_sum_const'], color='k',
            label='Constant prices', zorder=5, linestyle='solid')
axs[1].plot(chts_opt_per_daytime.index+1, chts_opt_per_daytime['P_ev_opt_sum_const_mi'], color='k',
            label='Constant prices minimally increasing', zorder=5, linestyle='dashdot')
axs[1].plot(chts_opt_per_daytime.index+1, chts_opt_per_daytime['P_ev_opt_sum_tou'], color='g',
            label='ToU prices', zorder=0, linestyle='dashed')
axs[1].plot(chts_opt_per_daytime.index+1, chts_opt_per_daytime['P_ev_opt_sum_tou_mi'], color='g',
            label='ToU prices minimally increasing', zorder=0, linestyle='dotted')
axs[1].set_ylabel('Charging power [kW]')
axs[1].grid()
axs[1].legend()
# Cumulated power for ev charging with minimal price increments
axs[2].plot(chts_flex_per_daytime.index+1, chts_flex_per_daytime['P_pos_sum_const'], color='k',
            label='Constant prices', zorder=5, linestyle='solid')
axs[2].plot(chts_flex_per_daytime.index+1, chts_flex_per_daytime['P_pos_sum_const_mi'], color='k',
            label='Constant prices minimally increasing', zorder=0, linestyle='dashdot')
axs[2].plot(chts_flex_per_daytime.index+1, chts_flex_per_daytime['P_pos_sum_tou'], color='g',
            label='ToU prices', zorder=5, linestyle='dashed')
axs[2].plot(chts_flex_per_daytime.index+1, chts_flex_per_daytime['P_pos_sum_tou_mi'], color='g',
            label='ToU prices minimally increasing', zorder=0, linestyle='dotted')
axs[2].plot(chts_flex_per_daytime.index+1, chts_flex_per_daytime['P_neg_sum_const'],
            color='k', zorder=5, linestyle='solid')
axs[2].plot(chts_flex_per_daytime.index+1, chts_flex_per_daytime['P_neg_sum_const_mi'],
            color='k', zorder=0, linestyle='dashdot')
axs[2].plot(chts_flex_per_daytime.index+1, chts_flex_per_daytime['P_neg_sum_tou'],
            color='g', zorder=5, linestyle='dashed')
axs[2].plot(chts_flex_per_daytime.index+1, chts_flex_per_daytime['P_neg_sum_tou_mi'],
            color='g', zorder=0, linestyle='dotted')
axs[2].set_ylabel('Flexible power [kW]')
axs[2].grid()
axs[2].legend()
# Electricity cost
axs[3].plot(chts_opt_per_daytime.index+1, chts_opt_per_daytime['c_elect_in_const'], color='k',
            label='Constant prices', zorder=5)
axs[3].plot(chts_opt_per_daytime.index+1, chts_opt_per_daytime['c_elect_in_tou'], color='g',
            label='ToU prices', zorder=0, linestyle='dashed')
axs[3].set_ylabel('Electricity cost [$/kWh]')
axs[3].grid()
axs[3].legend()
axs[3].set_xlabel('Date')


# """
# ####################################################################
# # Average number of available vehicles #############################
# ####################################################################
# """
# # Average vehicle availabilities
# plt.figure()
# plt.title('Average vehicle availability')
# sb.heatmap(n_avail_veh_hm, vmin=0, vmax=8)
# # plt.figure()
# # plt.plot(chts_opt_per_daytime['n_veh_avail'])
