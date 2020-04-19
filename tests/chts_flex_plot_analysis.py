import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm as cmap
import os
import numpy as np
import seaborn as sb
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

"""
####################################################################
# Read data from hdf files #########################################
####################################################################
"""
chts_flex_sum_df = pd.read_hdf('C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV/Results/Aggregated Data/chts_flex_sum_data.h5', key='df')
chts_opt_sum_df = pd.read_hdf('C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV/Results/Aggregated Data/chts_opt_sum_data.h5', key='df')
# minimal and maximal time of all files (known)
t_min = min(chts_flex_sum_df.index)
t_max = max(chts_flex_sum_df.index)
# Date range from minimal to maximal time
t_range = pd.date_range(start=t_min, end=t_max, freq='15Min')
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# """
# ####################################################################
# # Optimal charging schedule analysis ###############################
# ####################################################################
# """
# # Subplots
# fig1, axs = plt.subplots(nrows=4, ncols=1, sharex=True)
# # number of available vehicles
# axs[0].plot(chts_opt_sum_df['n_veh_avail'], color='k')
# axs[0].set_ylabel('# of available vehicles')
# axs[0].grid()
# # Electricity cost
# axs[1].plot(chts_opt_sum_df['c_elect_in_const'], color='k', label='Constant prices', zorder=10)
# axs[1].plot(chts_opt_sum_df['c_elect_in_tou'], color='g', label='ToU prices', zorder=5)
# axs[1].plot(chts_opt_sum_df['c_elect_in_rtp'], color='b', label='Real-time prices', zorder=0)
# axs[1].set_ylabel('Electricity cost [$/kWh]')
# axs[1].grid()
# axs[1].legend()
# axs[1].set_xlabel('Date')
# # Cumulated power for ev charging
# axs[2].plot(chts_opt_sum_df['P_ev_opt_sum_const'], color='k', label='Constant prices', zorder=5, linestyle='solid')
# axs[2].plot(chts_opt_sum_df['P_ev_opt_sum_tou'], color='g', label='ToU prices', zorder=0, linestyle='dashed')
# axs[2].plot(chts_opt_sum_df['P_ev_opt_sum_const_mi'], color='k', label='Constant prices minimally increasing',
#             zorder=5, linestyle='dashdot')
# axs[2].plot(chts_opt_sum_df['P_ev_opt_sum_tou_mi'], color='g', label='ToU prices minimally increasing',
#             zorder=0, linestyle='dotted')
# axs[2].plot(chts_opt_sum_df['P_ev_opt_sum_rtp'], color='b', label='RTP',
#             zorder=0, linestyle='solid')
# axs[2].hlines((chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_const_mi')['P_ev_opt_sum_const_mi'] /
#                chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_const_mi')['n_veh_avail']).mean() *
#               chts_opt_sum_df['n_veh_avail'].max(),
#               t_min, t_max, color='black', linestyle='dashdot')
# axs[2].hlines((chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_tou_mi')['P_ev_opt_sum_tou_mi'] /
#                chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_tou_mi')['n_veh_avail']).mean() *
#               chts_opt_sum_df['n_veh_avail'].max(),
#               t_min, t_max, color='g', linestyle='dotted')
# axs[2].hlines((chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_const')['P_ev_opt_sum_const'] /
#                chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_const')['n_veh_avail']).mean() *
#               chts_opt_sum_df['n_veh_avail'].max(),
#               t_min, t_max, color='black', linestyle='solid')
# axs[2].hlines((chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_tou')['P_ev_opt_sum_tou'] /
#                chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_tou')['n_veh_avail']).mean() *
#               chts_opt_sum_df['n_veh_avail'].max(),
#               t_min, t_max, color='g', linestyle='dashed')
# axs[2].hlines((chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_rtp')['P_ev_opt_sum_rtp'] /
#                chts_opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_rtp')['n_veh_avail']).mean() *
#               chts_opt_sum_df['n_veh_avail'].max(),
#               t_min, t_max, color='b', linestyle='solid')
# axs[2].set_ylabel('Charging power [kW]')
# axs[2].grid()
# axs[2].legend()
# # Cumulated flexible power for ev charging
# axs[3].plot(chts_flex_sum_df['P_pos_sum_const'], color='k', label='Constant prices', zorder=5, linestyle='solid')
# axs[3].plot(chts_flex_sum_df['P_pos_sum_const_mi'], color='g', label='ToU prices', zorder=0, linestyle='dashdot')
# axs[3].plot(chts_flex_sum_df['P_pos_sum_tou'], color='k', label='Constant prices minimally increasing',
#             zorder=5, linestyle='dashed')
# axs[3].plot(chts_flex_sum_df['P_pos_sum_tou_mi'], color='g', label='ToU prices minimally increasing',
#             zorder=0, linestyle='dotted')
# axs[3].plot(chts_flex_sum_df['P_pos_sum_rtp'], color='b', label='Real-time prices',
#             zorder=0, linestyle='solid')
# axs[3].plot(chts_flex_sum_df['P_neg_sum_const'], color='k', zorder=5, linestyle='solid')
# axs[3].plot(chts_flex_sum_df['P_neg_sum_const_mi'], color='g', zorder=0, linestyle='dashdot')
# axs[3].plot(chts_flex_sum_df['P_neg_sum_tou'], color='k', zorder=5, linestyle='dashed')
# axs[3].plot(chts_flex_sum_df['P_neg_sum_tou_mi'], color='g', zorder=0, linestyle='dotted')
# axs[3].plot(chts_flex_sum_df['P_neg_sum_rtp'], color='b', zorder=0, linestyle='solid')
# axs[3].set_ylabel('Flexible power [kW]')
# axs[3].grid()
# axs[3].legend()


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
chts_opt_per_daytime_qt = pd.DataFrame()
n_percentiles = 11           # Define number of percentiles
percentiles = np.linspace(start=0, stop=1, num=n_percentiles)
chts_opt_per_daytime_temp = chts_opt_sum_df.groupby(by='Daytime_ID').quantile(percentiles)
chts_opt_per_daytime_qt = chts_opt_per_daytime_qt.append(chts_opt_per_daytime_temp.iloc[96*n_percentiles:192*n_percentiles, :])
chts_opt_per_daytime_qt = chts_opt_per_daytime_qt.append(chts_opt_per_daytime_temp.iloc[480*n_percentiles:, :])
chts_opt_per_daytime_qt = chts_opt_per_daytime_qt.append(chts_opt_per_daytime_temp.iloc[384*n_percentiles:480*n_percentiles, :])
chts_opt_per_daytime_qt = chts_opt_per_daytime_qt.append(chts_opt_per_daytime_temp.iloc[0:96*n_percentiles, :])
chts_opt_per_daytime_qt = chts_opt_per_daytime_qt.append(chts_opt_per_daytime_temp.iloc[192*n_percentiles:384*n_percentiles, :])
chts_opt_per_daytime_qt = chts_opt_per_daytime_qt.reset_index()
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
P_pos_sum_rtp_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                columns=days)
P_neg_sum_tou_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                columns=days)
P_neg_sum_const_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                  columns=days)
P_neg_sum_tou_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                   columns=days)
P_neg_sum_const_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                     columns=days)
P_neg_sum_rtp_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                columns=days)
n_avail_veh_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                              columns=days)

# Copy power to single day columns
for i in range(7):
    P_pos_sum_tou_hm[days[i]].iloc[:] = chts_flex_per_daytime['P_pos_sum_tou'].iloc[i*96:i*96+96].values
    P_pos_sum_const_hm[days[i]].iloc[:] = chts_flex_per_daytime['P_pos_sum_const'].iloc[i*96:i*96+96].values
    P_pos_sum_tou_mi_hm[days[i]].iloc[:] = chts_flex_per_daytime['P_pos_sum_tou_mi'].iloc[i*96:i*96+96].values
    P_pos_sum_const_mi_hm[days[i]].iloc[:] = chts_flex_per_daytime['P_pos_sum_const_mi'].iloc[i*96:i*96+96].values
    P_pos_sum_rtp_hm[days[i]].iloc[:] = chts_flex_per_daytime['P_pos_sum_rtp'].iloc[i*96:i*96+96].values
    P_neg_sum_tou_hm[days[i]].iloc[:] = chts_flex_per_daytime['P_neg_sum_tou'].iloc[i*96:i*96+96].values
    P_neg_sum_const_hm[days[i]].iloc[:] = chts_flex_per_daytime['P_neg_sum_const'].iloc[i*96:i*96+96].values
    P_neg_sum_tou_mi_hm[days[i]].iloc[:] = chts_flex_per_daytime['P_neg_sum_tou_mi'].iloc[i*96:i*96+96].values
    P_neg_sum_const_mi_hm[days[i]].iloc[:] = chts_flex_per_daytime['P_neg_sum_const_mi'].iloc[i*96:i*96+96].values
    P_neg_sum_rtp_hm[days[i]].iloc[:] = chts_flex_per_daytime['P_neg_sum_rtp'].iloc[i*96:i*96+96].values

# Charging power
fig3, axs = plt.subplots(nrows=5, ncols=2, sharex=True, sharey=True)
cm = ['Greens', 'Blues_r']
pcm = axs[0, 0].pcolormesh(P_pos_sum_tou_hm, vmin=0, vmax=20, cmap='Greens', edgecolors=None)
axs[0, 0].set_title('ToU prices')
sb.heatmap(P_pos_sum_const_hm, ax=axs[1, 0], cbar=False, vmin=0, vmax=20, cmap='Greens')
axs[1, 0].set_title('Constant prices')
sb.heatmap(P_pos_sum_tou_mi_hm, ax=axs[2, 0], cbar=False, vmin=0, vmax=20, cmap='Greens')
axs[2, 0].set_title('ToU prices minimally increasing')
sb.heatmap(P_pos_sum_const_mi_hm, ax=axs[3, 0], cbar=False, vmin=0, vmax=20, cmap='Greens')
axs[3, 0].set_title('Constant prices minimally increasing')
sb.heatmap(P_pos_sum_rtp_hm, ax=axs[4, 0], cbar=False, vmin=0, vmax=20, cmap='Greens')
axs[4, 0].set_title('Real-time prices')
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
sb.heatmap(P_neg_sum_rtp_hm, ax=axs[4, 1], cbar=False, vmin=-50, vmax=0, cmap='Blues_r')
axs[4, 1].set_title('Real-time prices')
fig3.colorbar(pcm, ax=axs[:, 1], shrink=0.6, label='Negative flexible power [kW]')




"""
##################################################################
##################################################################
##################################################################
"""
# Subplots
fig4, axs = plt.subplots(nrows=4, ncols=1, sharex=True)
# number of available vehicles
axs[0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['n_veh_avail'], color='k', label='Mean')
n_qt_plots = int((n_percentiles-1)/2)
for i in range(n_qt_plots):
    axs[0].fill_between(chts_opt_per_daytime.index,
                        chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] == percentiles[i]]['n_veh_avail'],
                        chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] == percentiles[-1-i]]['n_veh_avail'],
                        facecolors=cmap.YlGn((i+1)/(n_qt_plots+1)),
                        label=str(int(percentiles[i]*100)) + '-' + str(int(percentiles[-1-i]*100)) + '%-ile')
# axs[0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] ==
#                                                                 percentiles[int((n_percentiles-1)/2)]]['n_veh_avail'],
#             color='k', label='Median')
axs[0].set_ylabel('# of available vehicles')
axs[0].grid()
axs[0].legend()
# Electricity cost
axs[1].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['c_elect_in_const'], color='k',
            label='Constant prices', zorder=5)
axs[1].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['c_elect_in_tou'], color='b',
            label='ToU prices', zorder=0, linestyle='dashed')
axs[1].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['c_elect_in_rtp'], color='xkcd:orange',
            label='Real-time prices', zorder=0, linestyle='solid')
axs[1].set_ylabel('Electricity cost [$/kWh]')
axs[1].grid()
axs[1].legend()
# Cumulated power for ev charging
axs[2].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_const'], color='k',
            label='Constant prices', zorder=5, linestyle='solid')
axs[2].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_const_mi'], color='xkcd:purple',
            label='Constant prices minimally increasing', zorder=5, linestyle='dashdot')
axs[2].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_tou'], color='b',
            label='ToU prices', zorder=0, linestyle='dashed')
axs[2].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_tou_mi'], color='g',
            label='ToU prices minimally increasing', zorder=0, linestyle='dotted')
axs[2].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_rtp'], color='xkcd:orange',
            label='Real-time prices', zorder=0, linestyle='solid')
axs[2].set_ylabel('Average charging power [kW]')
axs[2].grid()
axs[2].legend()
# Cumulated power for ev charging with minimal price increments
axs[3].fill_between(chts_flex_per_daytime.index,
                    chts_flex_per_daytime['P_pos_sum_const'],
                    chts_flex_per_daytime['P_neg_sum_const'],
                    alpha=0.3, label='Constant prices', zorder=5, linestyle='solid', facecolor='k')
axs[3].fill_between(chts_flex_per_daytime.index,
                    chts_flex_per_daytime['P_pos_sum_const_mi'],
                    chts_flex_per_daytime['P_neg_sum_const_mi'],
                    alpha=0.3, label='Constant prices minimally increasing', zorder=0,
                    linestyle='dashdot', facecolor='xkcd:purple')
axs[3].fill_between(chts_flex_per_daytime.index,
                    chts_flex_per_daytime['P_pos_sum_tou'],
                    chts_flex_per_daytime['P_neg_sum_tou'],
                    alpha=0.3, label='ToU prices', zorder=5, linestyle='dashed', facecolor='b')
axs[3].fill_between(chts_flex_per_daytime.index,
                    chts_flex_per_daytime['P_pos_sum_tou_mi'],
                    chts_flex_per_daytime['P_neg_sum_tou_mi'],
                    alpha=0.3, label='ToU prices minimally increasing', zorder=0,
                    linestyle='dotted', facecolor='g')
axs[3].fill_between(chts_flex_per_daytime.index,
                    chts_flex_per_daytime['P_pos_sum_rtp'],
                    chts_flex_per_daytime['P_neg_sum_rtp'],
                    alpha=0.3, label='Real-time prices', zorder=0,
                    linestyle='dotted', facecolor='xkcd:orange')
axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_const'], color='k', zorder=0,
            linestyle='solid')        # label='Constant prices')
axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_const_mi'], color='xkcd:purple', zorder=0,
            linestyle='dashdot')      # label='Constant prices minimally increasing'
axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_tou'], color='b', zorder=0,
            linestyle='dashed')       # label='ToU prices'
axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_tou_mi'], color='g', zorder=0,
            linestyle='dotted')       # label='ToU prices minimally increasing'
axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_rtp'], color='xkcd:orange', zorder=0,
            linestyle='solid')        # label='Real-time prices',
axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_const'],
            color='k', zorder=5, linestyle='solid')
axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_const_mi'],
            color='xkcd:purple', zorder=0, linestyle='dashdot')
axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_tou'],
            color='b', zorder=5, linestyle='dashed')
axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_tou_mi'],
            color='g', zorder=0, linestyle='dotted')
axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_rtp'],
            color='xkcd:orange', zorder=0, linestyle='solid')
axs[3].set_ylabel('Flexible power [kW]')
axs[3].grid()
axs[3].legend()
plt.xlim([0, 672])
n_ticks = 14
tick_range = np.linspace(start=0, stop=624, num=n_ticks)
plt.xticks(tick_range, chts_flex_per_daytime.loc[tick_range, 'Daytime_ID'], rotation=45)


# """
# ################################################################
# # Plot optimal charging power with percentiles #################
# ################################################################
# """
# # Subplots
# fig5, axs = plt.subplots(nrows=5, ncols=1, sharex=True, sharey=True)
# # Cumulated power for ev charging
# axs[0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_const'], color='k',
#             label='Constant prices', zorder=5, linestyle='solid')
# n_qt_plots = int((n_percentiles-1)/2)
# for i in range(n_qt_plots):
#     axs[0].fill_between(chts_opt_per_daytime.index,
#                         chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] == percentiles[i]]['P_ev_opt_sum_const'],
#                         chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] == percentiles[-1-i]]['P_ev_opt_sum_const'],
#                         facecolors=cmap.Greys((i+1)/(n_qt_plots+1)),
#                         label=str(round(percentiles[i], 1)*100) + '-' + str(round(percentiles[-1-i], 1)*100) + '%-ile')
# axs[0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] ==
#                                                                 percentiles[int((n_percentiles-1)/2)]]['P_ev_opt_sum_const'],
#             color='k', label='Median')
# axs[0].grid()
# axs[0].legend()
# axs[1].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_const_mi'], color='k',
#             label='Constant prices minimally increasing', zorder=5, linestyle='solid')
# n_qt_plots = int((n_percentiles-1)/2)
# for i in range(n_qt_plots):
#     axs[1].fill_between(chts_opt_per_daytime.index,
#                         chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] == percentiles[i]]['P_ev_opt_sum_const_mi'],
#                         chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] == percentiles[-1-i]]['P_ev_opt_sum_const_mi'],
#                         facecolors=cmap.Purples((i+1)/(n_qt_plots+1)),
#                         label=str(round(percentiles[i], 1)*100) + '-' + str(round(percentiles[-1-i], 1)*100) + '%-ile')
# axs[1].plot(chts_opt_per_daytime.index, chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] ==
#                                                                 percentiles[int((n_percentiles-1)/2)]]['P_ev_opt_sum_const_mi'],
#             color='k', label='Median')
# axs[1].grid()
# axs[1].legend()
# axs[2].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_tou'], color='k',
#             label='ToU prices', zorder=5, linestyle='solid')
# n_qt_plots = int((n_percentiles-1)/2)
# for i in range(n_qt_plots):
#     axs[2].fill_between(chts_opt_per_daytime.index,
#                         chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] == percentiles[i]]['P_ev_opt_sum_tou'],
#                         chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] == percentiles[-1-i]]['P_ev_opt_sum_tou'],
#                         facecolors=cmap.Blues((i+1)/(n_qt_plots+1)),
#                         label=str(round(percentiles[i], 1)*100) + '-' + str(round(percentiles[-1-i], 1)*100) + '%-ile')
# axs[2].plot(chts_opt_per_daytime.index, chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] ==
#                                                                 percentiles[int((n_percentiles-1)/2)]]['P_ev_opt_sum_tou'],
#             color='k', label='Median')
# axs[2].grid()
# axs[2].legend()
# axs[3].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_tou_mi'], color='k',
#             label='ToU prices minimally increasing', zorder=5, linestyle='solid')
# n_qt_plots = int((n_percentiles-1)/2)
# for i in range(n_qt_plots):
#     axs[3].fill_between(chts_opt_per_daytime.index,
#                         chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] == percentiles[i]]['P_ev_opt_sum_tou_mi'],
#                         chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] == percentiles[-1-i]]['P_ev_opt_sum_tou_mi'],
#                         facecolors=cmap.Greens((i+1)/(n_qt_plots+1)),
#                         label=str(round(percentiles[i], 1)*100) + '-' + str(round(percentiles[-1-i], 1)*100) + '%-ile')
# axs[3].plot(chts_opt_per_daytime.index, chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] ==
#                                                                 percentiles[int((n_percentiles-1)/2)]]['P_ev_opt_sum_tou_mi'],
#             color='k', label='Median')
# axs[3].grid()
# axs[3].legend()
# axs[4].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_rtp'], color='k',
#             label='Real-time prices', zorder=5, linestyle='solid')
# n_qt_plots = int((n_percentiles-1)/2)
# for i in range(n_qt_plots):
#     axs[4].fill_between(chts_opt_per_daytime.index,
#                         chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] == percentiles[i]]['P_ev_opt_sum_rtp'],
#                         chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] == percentiles[-1-i]]['P_ev_opt_sum_rtp'],
#                         facecolors=cmap.Oranges((i+1)/(n_qt_plots+1)),
#                         label=str(round(percentiles[i], 1)*100) + '-' + str(round(percentiles[-1-i], 1)*100) + '%-ile')
# axs[4].plot(chts_opt_per_daytime.index, chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] ==
#                                                                 percentiles[int((n_percentiles-1)/2)]]['P_ev_opt_sum_rtp'],
#             color='k', label='Median')
# axs[4].grid()
# axs[4].legend()
# axs[2].set_ylabel('Charging power [kW]')
# plt.xlim([0, 672])
# n_ticks = 14
# tick_range = np.linspace(start=0, stop=624, num=n_ticks)
# plt.xticks(tick_range, chts_flex_per_daytime.loc[tick_range, 'Daytime_ID'], rotation=45)

# """
# ################################################################
# # Plot number of available vehicles and electricity prices #####
# ################################################################
# """
# # Subplots
# fig4, axs = plt.subplots(nrows=2, ncols=1, sharex=True)
# # number of available vehicles
# axs[0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['n_veh_avail'], color='k', label='Mean')
# n_qt_plots = int((n_percentiles-1)/2)
# for i in range(n_qt_plots):
#     axs[0].fill_between(chts_opt_per_daytime.index,
#                         chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] == percentiles[i]]['n_veh_avail'],
#                         chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] == percentiles[-1-i]]['n_veh_avail'],
#                         facecolors=cmap.YlGn((i+1)/(n_qt_plots+1)),
#                         label=str(int(percentiles[i]*100)) + '-' + str(int(percentiles[-1-i]*100)) + '%-ile')
# axs[0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] ==
#                                                                 percentiles[int((n_percentiles-1)/2)]]['n_veh_avail'],
#             color='k', label='Median')
# axs[0].set_ylabel('# of available vehicles')
# axs[0].grid()
# axs[0].legend()
# # Electricity cost
# axs[1].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['c_elect_in_const'], color='k',
#             label='Constant prices', zorder=5)
# axs[1].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['c_elect_in_tou'], color='b',
#             label='ToU prices', zorder=0, linestyle='dashed')
# axs[1].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['c_elect_in_rtp'], color='xkcd:orange',
#             label='Real-time prices', zorder=0, linestyle='solid')
# axs[1].set_ylabel('Electricity cost [$/kWh]')
# axs[1].grid()
# axs[1].legend()
# axs[1].set_xlabel('Date')
# plt.xlim([0, 672])
# n_ticks = 14
# tick_range = np.linspace(start=0, stop=624, num=n_ticks)
# plt.xticks(tick_range, chts_flex_per_daytime.loc[tick_range, 'Daytime_ID'], rotation=45)
#
#
# """
# ################################################################
# # Plot mean charging power and flexibility #####################
# ################################################################
# """
# fig4, axs = plt.subplots(nrows=2, ncols=1, sharex=True)
# # Cumulated power for ev charging
# axs[0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_const'], color='k',
#             label='Constant prices', zorder=5, linestyle='solid')
# axs[0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_const_mi'], color='xkcd:purple',
#             label='Constant prices minimally increasing', zorder=5, linestyle='dashdot')
# axs[0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_tou'], color='b',
#             label='ToU prices', zorder=0, linestyle='dashed')
# axs[0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_tou_mi'], color='g',
#             label='ToU prices minimally increasing', zorder=0, linestyle='dotted')
# axs[0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_rtp'], color='xkcd:orange',
#             label='Real-time prices', zorder=0, linestyle='solid')
# axs[0].set_ylabel('Average charging power [kW]')
# axs[0].grid()
# axs[0].legend()
# # Cumulated power for ev charging with minimal price increments
# axs[1].fill_between(chts_flex_per_daytime.index,
#                     chts_flex_per_daytime['P_pos_sum_const'],
#                     chts_flex_per_daytime['P_neg_sum_const'],
#                     alpha=0.3, label='Constant prices', zorder=5, linestyle='solid', facecolor='k')
# axs[1].fill_between(chts_flex_per_daytime.index,
#                     chts_flex_per_daytime['P_pos_sum_const_mi'],
#                     chts_flex_per_daytime['P_neg_sum_const_mi'],
#                     alpha=0.3, label='Constant prices minimally increasing', zorder=0,
#                     linestyle='dashdot', facecolor='xkcd:purple')
# axs[1].fill_between(chts_flex_per_daytime.index,
#                     chts_flex_per_daytime['P_pos_sum_tou'],
#                     chts_flex_per_daytime['P_neg_sum_tou'],
#                     alpha=0.3, label='ToU prices', zorder=5, linestyle='dashed', facecolor='b')
# axs[1].fill_between(chts_flex_per_daytime.index,
#                     chts_flex_per_daytime['P_pos_sum_tou_mi'],
#                     chts_flex_per_daytime['P_neg_sum_tou_mi'],
#                     alpha=0.3, label='ToU prices minimally increasing', zorder=0,
#                     linestyle='dotted', facecolor='g')
# axs[1].fill_between(chts_flex_per_daytime.index,
#                     chts_flex_per_daytime['P_pos_sum_rtp'],
#                     chts_flex_per_daytime['P_neg_sum_rtp'],
#                     alpha=0.3, label='Real-time prices', zorder=0,
#                     linestyle='dotted', facecolor='xkcd:orange')
# axs[1].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_const'], color='k', zorder=0,
#             linestyle='solid')        # label='Constant prices')
# axs[1].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_const_mi'], color='xkcd:purple', zorder=0,
#             linestyle='dashdot')      # label='Constant prices minimally increasing'
# axs[1].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_tou'], color='b', zorder=0,
#             linestyle='dashed')       # label='ToU prices'
# axs[1].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_tou_mi'], color='g', zorder=0,
#             linestyle='dotted')       # label='ToU prices minimally increasing'
# axs[1].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_rtp'], color='xkcd:orange', zorder=0,
#             linestyle='solid')        # label='Real-time prices',
# axs[1].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_const'],
#             color='k', zorder=5, linestyle='solid')
# axs[1].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_const_mi'],
#             color='xkcd:purple', zorder=0, linestyle='dashdot')
# axs[1].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_tou'],
#             color='b', zorder=5, linestyle='dashed')
# axs[1].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_tou_mi'],
#             color='g', zorder=0, linestyle='dotted')
# axs[1].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_rtp'],
#             color='xkcd:orange', zorder=0, linestyle='solid')
# axs[1].set_ylabel('Flexible power [kW]')
# axs[1].grid()
# axs[1].legend()
# plt.xlim([0, 672])
# n_ticks = 14
# tick_range = np.linspace(start=0, stop=624, num=n_ticks)
# plt.xticks(tick_range, chts_flex_per_daytime.loc[tick_range, 'Daytime_ID'], rotation=45)


# """
# ################################################################
# # Plot average flexibility over time ###########################
# ################################################################
# """
# # Subplots
# fig4, axs = plt.subplots(nrows=4, ncols=1, sharex=True)
# # number of available vehicles
# axs[0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['n_veh_avail'], color='k')
# axs[0].set_ylabel('# of available vehicles')
# axs[0].grid()
# # Electricity cost
# axs[1].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['c_elect_in_const'], color='k',
#             label='Constant prices', zorder=5)
# axs[1].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['c_elect_in_tou'], color='g',
#             label='ToU prices', zorder=0, linestyle='dashed')
# axs[1].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['c_elect_in_rtp'], color='b',
#             label='Real-time prices', zorder=0, linestyle='solid')
# axs[1].set_ylabel('Electricity cost [$/kWh]')
# axs[1].grid()
# axs[1].legend()
# axs[1].set_xlabel('Date')
# # Cumulated power for ev charging
# axs[2].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_const'], color='k',
#             label='Constant prices', zorder=5, linestyle='solid')
# axs[2].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_const_mi'], color='k',
#             label='Constant prices minimally increasing', zorder=5, linestyle='dashdot')
# axs[2].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_tou'], color='g',
#             label='ToU prices', zorder=0, linestyle='dashed')
# axs[2].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_tou_mi'], color='g',
#             label='ToU prices minimally increasing', zorder=0, linestyle='dotted')
# axs[2].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_rtp'], color='b',
#             label='Real-time prices', zorder=0, linestyle='solid')
# axs[2].set_ylabel('Charging power [kW]')
# axs[2].grid()
# axs[2].legend()
# # Cumulated power for ev charging with minimal price increments
# axs[3].fill_between(chts_flex_per_daytime.index,
#                     chts_flex_per_daytime['P_pos_sum_const'],
#                     chts_flex_per_daytime['P_neg_sum_const'],
#                     alpha=0.3, color='k', label='Constant prices', zorder=5, linestyle='solid', edgecolor='k')
# axs[3].fill_between(chts_flex_per_daytime.index,
#                     chts_flex_per_daytime['P_pos_sum_const_mi'],
#                     chts_flex_per_daytime['P_neg_sum_const_mi'],
#                     alpha=0.3, color='k', label='Constant prices minimally increasing', zorder=0,
#                     linestyle='dashdot', edgecolor='k')
# axs[3].fill_between(chts_flex_per_daytime.index,
#                     chts_flex_per_daytime['P_pos_sum_tou'],
#                     chts_flex_per_daytime['P_neg_sum_tou'],
#                     alpha=0.3, color='g', label='ToU prices', zorder=5, linestyle='dashed', edgecolor='g')
# axs[3].fill_between(chts_flex_per_daytime.index,
#                     chts_flex_per_daytime['P_pos_sum_tou_mi'],
#                     chts_flex_per_daytime['P_neg_sum_tou_mi'],
#                     alpha=0.3, color='g', label='ToU prices minimally increasing', zorder=0,
#                     linestyle='dotted', edgecolor='g')
# axs[3].fill_between(chts_flex_per_daytime.index,
#                     chts_flex_per_daytime['P_pos_sum_rtp'],
#                     chts_flex_per_daytime['P_neg_sum_rtp'],
#                     alpha=0.3, color='b', label='Real-time prices', zorder=0,
#                     linestyle='dotted', edgecolor='b')
# axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_const'], color='k', zorder=0,
#             linestyle='solid')        # label='Constant prices')
# axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_const_mi'], color='k', zorder=0,
#             linestyle='dashdot')      # label='Constant prices minimally increasing'
# axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_tou'], color='g', zorder=0,
#             linestyle='dashed')       # label='ToU prices'
# axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_tou_mi'], color='g', zorder=0,
#             linestyle='dotted')       # label='ToU prices minimally increasing'
# axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_rtp'], color='b', zorder=0,
#             linestyle='solid')        # label='Real-time prices',
# axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_const'],
#             color='k', zorder=5, linestyle='solid')
# axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_const_mi'],
#             color='k', zorder=0, linestyle='dashdot')
# axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_tou'],
#             color='g', zorder=5, linestyle='dashed')
# axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_tou_mi'],
#             color='g', zorder=0, linestyle='dotted')
# axs[3].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_rtp'],
#             color='b', zorder=0, linestyle='solid')
# axs[3].set_ylabel('Flexible power [kW]')
# axs[3].grid()
# axs[3].legend()
# n_ticks = 14
# tick_range = np.linspace(start=0, stop=624, num=n_ticks)
# plt.xlim([0, 672])
# plt.xticks(tick_range, chts_flex_per_daytime.loc[tick_range, 'Daytime_ID'], rotation=45)


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
