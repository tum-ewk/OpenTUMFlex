import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm as cmap
from matplotlib import rcParams
import os
import numpy as np
import seaborn as sb
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Set font style
rcParams["font.family"] = "Times New Roman"
rcParams["font.size"] = 10
rcParams["figure.figsize"] = [11.69, 8.27]

"""
####################################################################
# Read data from hdf files #########################################
####################################################################
"""
# Output and input path
chts_output_path = 'C:/Users/ga47num/PycharmProjects/US CHTS - OpenTUMFlex - EV/Output/'
chts_input_path = 'C:/Users/ga47num/PycharmProjects/US CHTS - OpenTUMFlex - EV/Input/'
# Read data
chts_flex_sum_df = pd.read_hdf(chts_output_path + 'Aggregated Data/flex_sum_data.h5', key='df')
chts_opt_sum_df = pd.read_hdf(chts_output_path + 'Aggregated Data/opt_sum_data.h5', key='df')
chts_opt_per_daytime = pd.read_hdf(chts_output_path + 'Aggregated Data/opt_per_daytime_data.h5', key='df')
chts_flex_per_daytime = pd.read_hdf(chts_output_path + 'Aggregated Data/flex_per_daytime_data.h5', key='df')
chts_opt_per_daytime_qt = pd.read_hdf(chts_output_path + 'Aggregated Data/opt_per_daytime_qt_data.h5', key='df')
chts_P_pos_tou_hm = pd.read_hdf(chts_output_path + 'Aggregated Data/P_pos_tou_hm_data.h5', key='df')
chts_P_pos_const_hm = pd.read_hdf(chts_output_path + 'Aggregated Data/P_pos_const_hm_data.h5', key='df')
chts_P_pos_tou_mi_hm = pd.read_hdf(chts_output_path + 'Aggregated Data/P_pos_tou_mi_hm_data.h5', key='df')
chts_P_pos_const_mi_hm = pd.read_hdf(chts_output_path + 'Aggregated Data/P_pos_const_mi_hm_data.h5', key='df')
chts_P_pos_rtp_hm = pd.read_hdf(chts_output_path + 'Aggregated Data/P_pos_rtp_hm_data.h5', key='df')
chts_P_neg_tou_hm = pd.read_hdf(chts_output_path + 'Aggregated Data/P_neg_tou_hm_data.h5', key='df')
chts_P_neg_const_hm = pd.read_hdf(chts_output_path + 'Aggregated Data/P_neg_const_hm_data.h5', key='df')
chts_P_neg_tou_mi_hm = pd.read_hdf(chts_output_path + 'Aggregated Data/P_neg_tou_mi_hm_data.h5', key='df')
chts_P_neg_const_mi_hm = pd.read_hdf(chts_output_path + 'Aggregated Data/P_neg_const_mi_hm_data.h5', key='df')
chts_P_neg_rtp_hm = pd.read_hdf(chts_output_path + 'Aggregated Data/P_neg_rtp_hm_data.h5', key='df')

# Output and input path
mp_output_path = 'C:/Users/ga47num/PycharmProjects/GER MP - OpenTUMFlex - EV/Output/'
mp_input_path = 'C:/Users/ga47num/PycharmProjects/GER MP - OpenTUMFlex - EV/Input/'
# Read data
mp_flex_sum_df = pd.read_hdf(mp_output_path + 'Aggregated Data/flex_sum_data.h5', key='df')
mp_opt_sum_df = pd.read_hdf(mp_output_path + 'Aggregated Data/opt_sum_data.h5', key='df')
mp_opt_per_daytime = pd.read_hdf(mp_output_path + 'Aggregated Data/opt_per_daytime_data.h5', key='df')
mp_flex_per_daytime = pd.read_hdf(mp_output_path + 'Aggregated Data/flex_per_daytime_data.h5', key='df')
mp_opt_per_daytime_qt = pd.read_hdf(mp_output_path + 'Aggregated Data/opt_per_daytime_qt_data.h5', key='df')
mp_P_pos_tou_hm = pd.read_hdf(mp_output_path + 'Aggregated Data/P_pos_tou_hm_data.h5', key='df')
mp_P_pos_const_hm = pd.read_hdf(mp_output_path + 'Aggregated Data/P_pos_const_hm_data.h5', key='df')
mp_P_pos_tou_mi_hm = pd.read_hdf(mp_output_path + 'Aggregated Data/P_pos_tou_mi_hm_data.h5', key='df')
mp_P_pos_const_mi_hm = pd.read_hdf(mp_output_path + 'Aggregated Data/P_pos_const_mi_hm_data.h5', key='df')
mp_P_pos_rtp_hm = pd.read_hdf(mp_output_path + 'Aggregated Data/P_pos_rtp_hm_data.h5', key='df')
mp_P_neg_tou_hm = pd.read_hdf(mp_output_path + 'Aggregated Data/P_neg_tou_hm_data.h5', key='df')
mp_P_neg_const_hm = pd.read_hdf(mp_output_path + 'Aggregated Data/P_neg_const_hm_data.h5', key='df')
mp_P_neg_tou_mi_hm = pd.read_hdf(mp_output_path + 'Aggregated Data/P_neg_tou_mi_hm_data.h5', key='df')
mp_P_neg_const_mi_hm = pd.read_hdf(mp_output_path + 'Aggregated Data/P_neg_const_mi_hm_data.h5', key='df')
mp_P_neg_rtp_hm = pd.read_hdf(mp_output_path + 'Aggregated Data/P_neg_rtp_hm_data.h5', key='df')

# Charging power
fig3, axs = plt.subplots(nrows=5, ncols=2, sharex=True, sharey=True)
cm = ['Greens', 'Blues_r']
pcm = axs[0, 0].pcolormesh(chts_P_pos_tou_hm, vmin=0, vmax=20, cmap='Greens', edgecolors=None)
axs[0, 0].set_title('ToU prices')
sb.heatmap(chts_P_pos_const_hm, ax=axs[1, 0], cbar=False, vmin=0, vmax=20, cmap='Greens')
axs[1, 0].set_title('Constant prices')
sb.heatmap(chts_P_pos_tou_mi_hm, ax=axs[2, 0], cbar=False, vmin=0, vmax=20, cmap='Greens')
axs[2, 0].set_title('ToU prices minimally increasing')
sb.heatmap(chts_P_pos_const_mi_hm, ax=axs[3, 0], cbar=False, vmin=0, vmax=20, cmap='Greens')
axs[3, 0].set_title('Constant prices minimally increasing')
sb.heatmap(chts_P_pos_rtp_hm, ax=axs[4, 0], cbar=False, vmin=0, vmax=20, cmap='Greens')
axs[4, 0].set_title('Real-time prices')
fig3.colorbar(pcm, ax=axs[:, 0], shrink=0.6, label='Positive flexible power [kW]')
axs[0, 0].set_xticklabels(chts_P_pos_const_hm.columns)
axs[0, 0].set_yticklabels(chts_P_pos_const_hm.index)

pcm = axs[0, 1].pcolormesh(chts_P_neg_tou_hm, vmin=-50, vmax=0, cmap='Blues_r')
axs[0, 1].set_title('ToU prices')
sb.heatmap(chts_P_neg_const_hm, ax=axs[1, 1], cbar=False, vmin=-50, vmax=0, cmap='Blues_r')
axs[1, 1].set_title('Constant prices')
sb.heatmap(chts_P_neg_tou_mi_hm, ax=axs[2, 1], cbar=False, vmin=-50, vmax=0, cmap='Blues_r')
axs[2, 1].set_title('ToU prices minimally increasing')
sb.heatmap(chts_P_neg_const_mi_hm, ax=axs[3, 1], cbar=False, vmin=-50, vmax=0, cmap='Blues_r')
axs[3, 1].set_title('Constant prices minimally increasing')
sb.heatmap(chts_P_neg_rtp_hm, ax=axs[4, 1], cbar=False, vmin=-50, vmax=0, cmap='Blues_r')
axs[4, 1].set_title('Real-time prices')
fig3.colorbar(pcm, ax=axs[:, 1], shrink=0.6, label='Negative flexible power [kW]')


"""
##################################################################
# Week long time series ##########################################
##################################################################
"""
n_percentiles = 9           # Define number of percentiles
percentiles = np.linspace(start=0.1, stop=0.9, num=n_percentiles).round(decimals=1)
chts_opt_per_daytime_qt['level_1'] = chts_opt_per_daytime_qt['level_1'].round(decimals=1)
mp_opt_per_daytime_qt['level_1'] = mp_opt_per_daytime_qt['level_1'].round(decimals=1)
# Subplots
fig4, axs = plt.subplots(nrows=4, ncols=2, sharex=True)
# Number of available vehicles ##############################################
# CHTS
axs[0, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['n_veh_avail'], color='k', label='Mean')
n_qt_plots = int((n_percentiles-1)/2)
for i in range(n_qt_plots):
    axs[0, 0].fill_between(chts_opt_per_daytime.index,
                           chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] == percentiles[i]]['n_veh_avail'],
                           chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] == percentiles[-1-i]]['n_veh_avail'],
                           facecolors=cmap.YlGn((i+1)/(n_qt_plots+1)),
                           label=str(int(percentiles[i]*100)) + '-' + str(int(percentiles[-1-i]*100)) + '%-ile')
# axs[0].plot(opt_per_daytime.index, opt_per_daytime_qt[opt_per_daytime_qt['level_1'] ==
#                                                                 percentiles[int((n_percentiles-1)/2)]]['n_veh_avail'],
#             color='k', label='Median')
axs[0, 0].set_ylabel('# of available vehicles')
axs[0, 0].grid()
axs[0, 0].legend()
# MP
axs[0, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['n_veh_avail'], color='k', label='Mean')
n_qt_plots = int((n_percentiles-1)/2)
for i in range(n_qt_plots):
    axs[0, 1].fill_between(mp_opt_per_daytime.index,
                           mp_opt_per_daytime_qt[mp_opt_per_daytime_qt['level_1'] == percentiles[i]]['n_veh_avail'],
                           mp_opt_per_daytime_qt[mp_opt_per_daytime_qt['level_1'] == percentiles[-1-i]]['n_veh_avail'],
                           facecolors=cmap.YlGn((i+1)/(n_qt_plots+1)),
                           label=str(int(percentiles[i]*100)) + '-' + str(int(percentiles[-1-i]*100)) + '%-ile')
# axs[0].plot(opt_per_daytime.index, opt_per_daytime_qt[opt_per_daytime_qt['level_1'] ==
#                                                                 percentiles[int((n_percentiles-1)/2)]]['n_veh_avail'],
#             color='k', label='Median')
axs[0, 1].set_ylabel('# of available vehicles')
axs[0, 1].grid()
axs[0, 1].legend()
# Electricity cost ##########################
# CHTS
axs[1, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['c_elect_in_const'], color='k',
               label='Constant prices', zorder=5)
axs[1, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['c_elect_in_tou'], color='b',
               label='ToU prices', zorder=0, linestyle='dashed')
axs[1, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['c_elect_in_rtp'], color='xkcd:orange',
               label='Real-time prices', zorder=0, linestyle='solid')
axs[1, 0].set_ylabel('Electricity cost [$/kWh]')
axs[1, 0].grid()
axs[1, 0].legend()
# MP
axs[1, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['c_elect_in_const'], color='k',
               label='Constant prices', zorder=5)
axs[1, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['c_elect_in_tou'], color='b',
               label='ToU prices', zorder=0, linestyle='dashed')
axs[1, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['c_elect_in_rtp'], color='xkcd:orange',
               label='Real-time prices', zorder=0, linestyle='solid')
axs[1, 1].set_ylabel('Electricity cost [$/kWh]')
axs[1, 1].grid()
axs[1, 1].legend()
# Cumulated power for ev charging ######################
# CHTS
axs[2, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_const'], color='k',
               label='Constant prices', zorder=5, linestyle='solid')
axs[2, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_const_mi'], color='xkcd:purple',
               label='Constant prices minimally increasing', zorder=5, linestyle='dashdot')
axs[2, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_tou'], color='b',
               label='ToU prices', zorder=0, linestyle='dashed')
axs[2, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_tou_mi'], color='g',
               label='ToU prices minimally increasing', zorder=0, linestyle='dotted')
axs[2, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_rtp'], color='xkcd:orange',
               label='Real-time prices', zorder=0, linestyle='solid')
axs[2, 0].set_ylabel('Average charging power [kW]')
axs[2, 0].grid()
axs[2, 0].legend()
# MP
axs[2, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['P_ev_opt_sum_const'], color='k',
               label='Constant prices', zorder=5, linestyle='solid')
axs[2, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['P_ev_opt_sum_const_mi'], color='xkcd:purple',
               label='Constant prices minimally increasing', zorder=5, linestyle='dashdot')
axs[2, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['P_ev_opt_sum_tou'], color='b',
               label='ToU prices', zorder=0, linestyle='dashed')
axs[2, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['P_ev_opt_sum_tou_mi'], color='g',
               label='ToU prices minimally increasing', zorder=0, linestyle='dotted')
axs[2, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['P_ev_opt_sum_rtp'], color='xkcd:orange',
               label='Real-time prices', zorder=0, linestyle='solid')
axs[2, 1].set_ylabel('Average charging power [kW]')
axs[2, 1].grid()
axs[2, 1].legend()
# Flexible Power ###########################################
# CHTS
axs[3, 0].fill_between(chts_flex_per_daytime.index,
                       chts_flex_per_daytime['P_pos_sum_const'],
                       chts_flex_per_daytime['P_neg_sum_const'],
                       alpha=0.3, label='Constant prices', zorder=5, linestyle='solid', facecolor='k')
axs[3, 0].fill_between(chts_flex_per_daytime.index,
                    chts_flex_per_daytime['P_pos_sum_const_mi'],
                    chts_flex_per_daytime['P_neg_sum_const_mi'],
                    alpha=0.3, label='Constant prices minimally increasing', zorder=0,
                    linestyle='dashdot', facecolor='xkcd:purple')
axs[3, 0].fill_between(chts_flex_per_daytime.index,
                    chts_flex_per_daytime['P_pos_sum_tou'],
                    chts_flex_per_daytime['P_neg_sum_tou'],
                    alpha=0.3, label='ToU prices', zorder=5, linestyle='dashed', facecolor='b')
axs[3, 0].fill_between(chts_flex_per_daytime.index,
                    chts_flex_per_daytime['P_pos_sum_tou_mi'],
                    chts_flex_per_daytime['P_neg_sum_tou_mi'],
                    alpha=0.3, label='ToU prices minimally increasing', zorder=0,
                    linestyle='dotted', facecolor='g')
axs[3, 0].fill_between(chts_flex_per_daytime.index,
                    chts_flex_per_daytime['P_pos_sum_rtp'],
                    chts_flex_per_daytime['P_neg_sum_rtp'],
                    alpha=0.3, label='Real-time prices', zorder=0,
                    linestyle='dotted', facecolor='xkcd:orange')
axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_const'], color='k', zorder=0,
            linestyle='solid')        # label='Constant prices')
axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_const_mi'], color='xkcd:purple', zorder=0,
            linestyle='dashdot')      # label='Constant prices minimally increasing'
axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_tou'], color='b', zorder=0,
            linestyle='dashed')       # label='ToU prices'
axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_tou_mi'], color='g', zorder=0,
            linestyle='dotted')       # label='ToU prices minimally increasing'
axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_rtp'], color='xkcd:orange', zorder=0,
            linestyle='solid')        # label='Real-time prices',
axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_const'],
            color='k', zorder=5, linestyle='solid')
axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_const_mi'],
            color='xkcd:purple', zorder=0, linestyle='dashdot')
axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_tou'],
            color='b', zorder=5, linestyle='dashed')
axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_tou_mi'],
            color='g', zorder=0, linestyle='dotted')
axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_rtp'],
            color='xkcd:orange', zorder=0, linestyle='solid')
axs[3, 0].set_ylabel('Flexible power [kW]')
axs[3, 0].grid()
axs[3, 0].legend()
# MP
axs[3, 1].fill_between(mp_flex_per_daytime.index,
                       mp_flex_per_daytime['P_pos_sum_const'],
                       mp_flex_per_daytime['P_neg_sum_const'],
                       alpha=0.3, label='Constant prices', zorder=5, linestyle='solid', facecolor='k')
axs[3, 1].fill_between(mp_flex_per_daytime.index,
                       mp_flex_per_daytime['P_pos_sum_const_mi'],
                       mp_flex_per_daytime['P_neg_sum_const_mi'],
                       alpha=0.3, label='Constant prices minimally increasing', zorder=0,
                       linestyle='dashdot', facecolor='xkcd:purple')
axs[3, 1].fill_between(mp_flex_per_daytime.index,
                       mp_flex_per_daytime['P_pos_sum_tou'],
                       mp_flex_per_daytime['P_neg_sum_tou'],
                       alpha=0.3, label='ToU prices', zorder=5, linestyle='dashed', facecolor='b')
axs[3, 1].fill_between(mp_flex_per_daytime.index,
                       mp_flex_per_daytime['P_pos_sum_tou_mi'],
                       mp_flex_per_daytime['P_neg_sum_tou_mi'],
                       alpha=0.3, label='ToU prices minimally increasing', zorder=0,
                       linestyle='dotted', facecolor='g')
axs[3, 1].fill_between(mp_flex_per_daytime.index,
                       mp_flex_per_daytime['P_pos_sum_rtp'],
                       mp_flex_per_daytime['P_neg_sum_rtp'],
                       alpha=0.3, label='Real-time prices', zorder=0,
                       linestyle='dotted', facecolor='xkcd:orange')
axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_const'], color='k', zorder=0,
               linestyle='solid')        # label='Constant prices')
axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_const_mi'], color='xkcd:purple', zorder=0,
               linestyle='dashdot')      # label='Constant prices minimally increasing'
axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_tou'], color='b', zorder=0,
               linestyle='dashed')       # label='ToU prices'
axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_tou_mi'], color='g', zorder=0,
               linestyle='dotted')       # label='ToU prices minimally increasing'
axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_rtp'], color='xkcd:orange', zorder=0,
               linestyle='solid')        # label='Real-time prices',
axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_neg_sum_const'],
               color='k', zorder=5, linestyle='solid')
axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_neg_sum_const_mi'],
               color='xkcd:purple', zorder=0, linestyle='dashdot')
axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_neg_sum_tou'],
               color='b', zorder=5, linestyle='dashed')
axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_neg_sum_tou_mi'],
               color='g', zorder=0, linestyle='dotted')
axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_neg_sum_rtp'],
               color='xkcd:orange', zorder=0, linestyle='solid')
axs[3, 1].set_ylabel('Flexible power [kW]')
axs[3, 1].grid()
axs[3, 1].legend()
plt.xlim([0, 672])
n_ticks = 14
tick_range = np.linspace(start=0, stop=624, num=n_ticks)
axs[3, 0].set_xticks(tick_range)
axs[3, 1].set_xticks(tick_range)
axs[3, 0].set_xticklabels(chts_flex_per_daytime.loc[tick_range, 'Daytime_ID'], rotation=45)
axs[3, 1].set_xticklabels(chts_flex_per_daytime.loc[tick_range, 'Daytime_ID'], rotation=45)


#########################################################################
#########################################################################
#########################################################################
# Subplots
fig4, axs = plt.subplots(nrows=2, ncols=2, sharex=True)
# Cumulated power for ev charging ######################
# CHTS
axs[0, 0].set_title('California household travel survey, US')
axs[0, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_const'], color='k',
               label='Constant prices', zorder=5, linestyle='solid')
axs[0, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_const_mi'], color='xkcd:purple',
               label='Constant prices minimally increasing', zorder=5, linestyle='dashdot')
axs[0, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_tou'], color='b',
               label='ToU prices', zorder=0, linestyle='dashed')
axs[0, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_tou_mi'], color='g',
               label='ToU prices minimally increasing', zorder=0, linestyle='dotted')
axs[0, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_rtp'], color='xkcd:orange',
               label='Real-time prices', zorder=0, linestyle='solid')
axs[0, 0].set_ylabel('Average charging power [kW]')
axs[0, 0].grid()
axs[0, 0].legend()
# MP
axs[0, 1].set_title('German Mobility Panel, GER')
axs[0, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['P_ev_opt_sum_const'], color='k',
               label='Constant prices', zorder=5, linestyle='solid')
axs[0, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['P_ev_opt_sum_const_mi'], color='xkcd:purple',
               label='Constant prices minimally increasing', zorder=5, linestyle='dashdot')
axs[0, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['P_ev_opt_sum_tou'], color='b',
               label='ToU prices', zorder=0, linestyle='dashed')
axs[0, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['P_ev_opt_sum_tou_mi'], color='g',
               label='ToU prices minimally increasing', zorder=0, linestyle='dotted')
axs[0, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['P_ev_opt_sum_rtp'], color='xkcd:orange',
               label='Real-time prices', zorder=0, linestyle='solid')
axs[0, 1].set_ylabel('Average charging power [kW]')
axs[0, 1].grid()
axs[0, 1].legend()
# Flexible Power ###########################################
# CHTS
axs[1, 0].fill_between(chts_flex_per_daytime.index,
                       chts_flex_per_daytime['P_pos_sum_const'],
                       chts_flex_per_daytime['P_neg_sum_const'],
                       alpha=0.3, label='Constant prices', zorder=5, linestyle='solid', facecolor='k')
axs[1, 0].fill_between(chts_flex_per_daytime.index,
                    chts_flex_per_daytime['P_pos_sum_const_mi'],
                    chts_flex_per_daytime['P_neg_sum_const_mi'],
                    alpha=0.3, label='Constant prices minimally increasing', zorder=0,
                    linestyle='dashdot', facecolor='xkcd:purple')
axs[1, 0].fill_between(chts_flex_per_daytime.index,
                    chts_flex_per_daytime['P_pos_sum_tou'],
                    chts_flex_per_daytime['P_neg_sum_tou'],
                    alpha=0.3, label='ToU prices', zorder=5, linestyle='dashed', facecolor='b')
axs[1, 0].fill_between(chts_flex_per_daytime.index,
                    chts_flex_per_daytime['P_pos_sum_tou_mi'],
                    chts_flex_per_daytime['P_neg_sum_tou_mi'],
                    alpha=0.3, label='ToU prices minimally increasing', zorder=0,
                    linestyle='dotted', facecolor='g')
axs[1, 0].fill_between(chts_flex_per_daytime.index,
                    chts_flex_per_daytime['P_pos_sum_rtp'],
                    chts_flex_per_daytime['P_neg_sum_rtp'],
                    alpha=0.3, label='Real-time prices', zorder=0,
                    linestyle='dotted', facecolor='xkcd:orange')
axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_const'], color='k', zorder=0,
            linestyle='solid')        # label='Constant prices')
axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_const_mi'], color='xkcd:purple', zorder=0,
            linestyle='dashdot')      # label='Constant prices minimally increasing'
axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_tou'], color='b', zorder=0,
            linestyle='dashed')       # label='ToU prices'
axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_tou_mi'], color='g', zorder=0,
            linestyle='dotted')       # label='ToU prices minimally increasing'
axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_rtp'], color='xkcd:orange', zorder=0,
            linestyle='solid')        # label='Real-time prices',
axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_const'],
            color='k', zorder=5, linestyle='solid')
axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_const_mi'],
            color='xkcd:purple', zorder=0, linestyle='dashdot')
axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_tou'],
            color='b', zorder=5, linestyle='dashed')
axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_tou_mi'],
            color='g', zorder=0, linestyle='dotted')
axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_rtp'],
            color='xkcd:orange', zorder=0, linestyle='solid')
axs[1, 0].set_ylabel('Flexible power [kW]')
axs[1, 0].grid()
axs[1, 0].legend()
# MP
axs[1, 1].fill_between(mp_flex_per_daytime.index,
                       mp_flex_per_daytime['P_pos_sum_const'],
                       mp_flex_per_daytime['P_neg_sum_const'],
                       alpha=0.3, label='Constant prices', zorder=5, linestyle='solid', facecolor='k')
axs[1, 1].fill_between(mp_flex_per_daytime.index,
                       mp_flex_per_daytime['P_pos_sum_const_mi'],
                       mp_flex_per_daytime['P_neg_sum_const_mi'],
                       alpha=0.3, label='Constant prices minimally increasing', zorder=0,
                       linestyle='dashdot', facecolor='xkcd:purple')
axs[1, 1].fill_between(mp_flex_per_daytime.index,
                       mp_flex_per_daytime['P_pos_sum_tou'],
                       mp_flex_per_daytime['P_neg_sum_tou'],
                       alpha=0.3, label='ToU prices', zorder=5, linestyle='dashed', facecolor='b')
axs[1, 1].fill_between(mp_flex_per_daytime.index,
                       mp_flex_per_daytime['P_pos_sum_tou_mi'],
                       mp_flex_per_daytime['P_neg_sum_tou_mi'],
                       alpha=0.3, label='ToU prices minimally increasing', zorder=0,
                       linestyle='dotted', facecolor='g')
axs[1, 1].fill_between(mp_flex_per_daytime.index,
                       mp_flex_per_daytime['P_pos_sum_rtp'],
                       mp_flex_per_daytime['P_neg_sum_rtp'],
                       alpha=0.3, label='Real-time prices', zorder=0,
                       linestyle='dotted', facecolor='xkcd:orange')
axs[1, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_const'], color='k', zorder=0,
               linestyle='solid')        # label='Constant prices')
axs[1, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_const_mi'], color='xkcd:purple', zorder=0,
               linestyle='dashdot')      # label='Constant prices minimally increasing'
axs[1, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_tou'], color='b', zorder=0,
               linestyle='dashed')       # label='ToU prices'
axs[1, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_tou_mi'], color='g', zorder=0,
               linestyle='dotted')       # label='ToU prices minimally increasing'
axs[1, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_rtp'], color='xkcd:orange', zorder=0,
               linestyle='solid')        # label='Real-time prices',
axs[1, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_neg_sum_const'],
               color='k', zorder=5, linestyle='solid')
axs[1, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_neg_sum_const_mi'],
               color='xkcd:purple', zorder=0, linestyle='dashdot')
axs[1, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_neg_sum_tou'],
               color='b', zorder=5, linestyle='dashed')
axs[1, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_neg_sum_tou_mi'],
               color='g', zorder=0, linestyle='dotted')
axs[1, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_neg_sum_rtp'],
               color='xkcd:orange', zorder=0, linestyle='solid')
axs[1, 1].set_ylabel('Flexible power [kW]')
axs[1, 1].grid()
axs[1, 1].legend()
plt.xlim([0, 672])
n_ticks = 14
tick_range = np.linspace(start=0, stop=624, num=n_ticks)
axs[1, 0].set_xticks(tick_range)
axs[1, 1].set_xticks(tick_range)
axs[1, 0].set_xticklabels(chts_flex_per_daytime.loc[tick_range, 'Daytime_ID'], rotation=45)
axs[1, 1].set_xticklabels(chts_flex_per_daytime.loc[tick_range, 'Daytime_ID'], rotation=45)



# """
# ####################################################################
# # Optimal charging schedule analysis ###############################
# ####################################################################
# """
# # Subplots
# fig1, axs = plt.subplots(nrows=4, ncols=1, sharex=True)
# # number of available vehicles
# axs[0].plot(opt_sum_df['n_veh_avail'], color='k')
# axs[0].set_ylabel('# of available vehicles')
# axs[0].grid()
# # Electricity cost
# axs[1].plot(opt_sum_df['c_elect_in_const'], color='k', label='Constant prices', zorder=10)
# axs[1].plot(opt_sum_df['c_elect_in_tou'], color='g', label='ToU prices', zorder=5)
# axs[1].plot(opt_sum_df['c_elect_in_rtp'], color='b', label='Real-time prices', zorder=0)
# axs[1].set_ylabel('Electricity cost [$/kWh]')
# axs[1].grid()
# axs[1].legend()
# axs[1].set_xlabel('Date')
# # Cumulated power for ev charging
# axs[2].plot(opt_sum_df['P_ev_opt_sum_const'], color='k', label='Constant prices', zorder=5, linestyle='solid')
# axs[2].plot(opt_sum_df['P_ev_opt_sum_tou'], color='g', label='ToU prices', zorder=0, linestyle='dashed')
# axs[2].plot(opt_sum_df['P_ev_opt_sum_const_mi'], color='k', label='Constant prices minimally increasing',
#             zorder=5, linestyle='dashdot')
# axs[2].plot(opt_sum_df['P_ev_opt_sum_tou_mi'], color='g', label='ToU prices minimally increasing',
#             zorder=0, linestyle='dotted')
# axs[2].plot(opt_sum_df['P_ev_opt_sum_rtp'], color='b', label='RTP',
#             zorder=0, linestyle='solid')
# axs[2].hlines((opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_const_mi')['P_ev_opt_sum_const_mi'] /
#                opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_const_mi')['n_veh_avail']).mean() *
#               opt_sum_df['n_veh_avail'].max(),
#               t_min, t_max, color='black', linestyle='dashdot')
# axs[2].hlines((opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_tou_mi')['P_ev_opt_sum_tou_mi'] /
#                opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_tou_mi')['n_veh_avail']).mean() *
#               opt_sum_df['n_veh_avail'].max(),
#               t_min, t_max, color='g', linestyle='dotted')
# axs[2].hlines((opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_const')['P_ev_opt_sum_const'] /
#                opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_const')['n_veh_avail']).mean() *
#               opt_sum_df['n_veh_avail'].max(),
#               t_min, t_max, color='black', linestyle='solid')
# axs[2].hlines((opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_tou')['P_ev_opt_sum_tou'] /
#                opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_tou')['n_veh_avail']).mean() *
#               opt_sum_df['n_veh_avail'].max(),
#               t_min, t_max, color='g', linestyle='dashed')
# axs[2].hlines((opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_rtp')['P_ev_opt_sum_rtp'] /
#                opt_sum_df.nlargest(round(len(t_range) * 0.005), 'P_ev_opt_sum_rtp')['n_veh_avail']).mean() *
#               opt_sum_df['n_veh_avail'].max(),
#               t_min, t_max, color='b', linestyle='solid')
# axs[2].set_ylabel('Charging power [kW]')
# axs[2].grid()
# axs[2].legend()
# # Cumulated flexible power for ev charging
# axs[3].plot(flex_sum_df['P_pos_sum_const'], color='k', label='Constant prices', zorder=5, linestyle='solid')
# axs[3].plot(flex_sum_df['P_pos_sum_const_mi'], color='g', label='ToU prices', zorder=0, linestyle='dashdot')
# axs[3].plot(flex_sum_df['P_pos_sum_tou'], color='k', label='Constant prices minimally increasing',
#             zorder=5, linestyle='dashed')
# axs[3].plot(flex_sum_df['P_pos_sum_tou_mi'], color='g', label='ToU prices minimally increasing',
#             zorder=0, linestyle='dotted')
# axs[3].plot(flex_sum_df['P_pos_sum_rtp'], color='b', label='Real-time prices',
#             zorder=0, linestyle='solid')
# axs[3].plot(flex_sum_df['P_neg_sum_const'], color='k', zorder=5, linestyle='solid')
# axs[3].plot(flex_sum_df['P_neg_sum_const_mi'], color='g', zorder=0, linestyle='dashdot')
# axs[3].plot(flex_sum_df['P_neg_sum_tou'], color='k', zorder=5, linestyle='dashed')
# axs[3].plot(flex_sum_df['P_neg_sum_tou_mi'], color='g', zorder=0, linestyle='dotted')
# axs[3].plot(flex_sum_df['P_neg_sum_rtp'], color='b', zorder=0, linestyle='solid')
# axs[3].set_ylabel('Flexible power [kW]')
# axs[3].grid()
# axs[3].legend()
# """
# ################################################################
# # Plot optimal charging power with percentiles #################
# ################################################################
# """
# # Subplots
# fig5, axs = plt.subplots(nrows=5, ncols=1, sharex=True, sharey=True)
# # Cumulated power for ev charging
# axs[0].plot(opt_per_daytime.index, opt_per_daytime['P_ev_opt_sum_const'], color='k',
#             label='Constant prices', zorder=5, linestyle='solid')
# n_qt_plots = int((n_percentiles-1)/2)
# for i in range(n_qt_plots):
#     axs[0].fill_between(opt_per_daytime.index,
#                         opt_per_daytime_qt[opt_per_daytime_qt['level_1'] == percentiles[i]]['P_ev_opt_sum_const'],
#                         opt_per_daytime_qt[opt_per_daytime_qt['level_1'] == percentiles[-1-i]]['P_ev_opt_sum_const'],
#                         facecolors=cmap.Greys((i+1)/(n_qt_plots+1)),
#                         label=str(round(percentiles[i], 1)*100) + '-' + str(round(percentiles[-1-i], 1)*100) + '%-ile')
# axs[0].plot(opt_per_daytime.index, opt_per_daytime_qt[opt_per_daytime_qt['level_1'] ==
#                                                                 percentiles[int((n_percentiles-1)/2)]]['P_ev_opt_sum_const'],
#             color='k', label='Median')
# axs[0].grid()
# axs[0].legend()
# axs[1].plot(opt_per_daytime.index, opt_per_daytime['P_ev_opt_sum_const_mi'], color='k',
#             label='Constant prices minimally increasing', zorder=5, linestyle='solid')
# n_qt_plots = int((n_percentiles-1)/2)
# for i in range(n_qt_plots):
#     axs[1].fill_between(opt_per_daytime.index,
#                         opt_per_daytime_qt[opt_per_daytime_qt['level_1'] == percentiles[i]]['P_ev_opt_sum_const_mi'],
#                         opt_per_daytime_qt[opt_per_daytime_qt['level_1'] == percentiles[-1-i]]['P_ev_opt_sum_const_mi'],
#                         facecolors=cmap.Purples((i+1)/(n_qt_plots+1)),
#                         label=str(round(percentiles[i], 1)*100) + '-' + str(round(percentiles[-1-i], 1)*100) + '%-ile')
# axs[1].plot(opt_per_daytime.index, opt_per_daytime_qt[opt_per_daytime_qt['level_1'] ==
#                                                                 percentiles[int((n_percentiles-1)/2)]]['P_ev_opt_sum_const_mi'],
#             color='k', label='Median')
# axs[1].grid()
# axs[1].legend()
# axs[2].plot(opt_per_daytime.index, opt_per_daytime['P_ev_opt_sum_tou'], color='k',
#             label='ToU prices', zorder=5, linestyle='solid')
# n_qt_plots = int((n_percentiles-1)/2)
# for i in range(n_qt_plots):
#     axs[2].fill_between(opt_per_daytime.index,
#                         opt_per_daytime_qt[opt_per_daytime_qt['level_1'] == percentiles[i]]['P_ev_opt_sum_tou'],
#                         opt_per_daytime_qt[opt_per_daytime_qt['level_1'] == percentiles[-1-i]]['P_ev_opt_sum_tou'],
#                         facecolors=cmap.Blues((i+1)/(n_qt_plots+1)),
#                         label=str(round(percentiles[i], 1)*100) + '-' + str(round(percentiles[-1-i], 1)*100) + '%-ile')
# axs[2].plot(opt_per_daytime.index, opt_per_daytime_qt[opt_per_daytime_qt['level_1'] ==
#                                                                 percentiles[int((n_percentiles-1)/2)]]['P_ev_opt_sum_tou'],
#             color='k', label='Median')
# axs[2].grid()
# axs[2].legend()
# axs[3].plot(opt_per_daytime.index, opt_per_daytime['P_ev_opt_sum_tou_mi'], color='k',
#             label='ToU prices minimally increasing', zorder=5, linestyle='solid')
# n_qt_plots = int((n_percentiles-1)/2)
# for i in range(n_qt_plots):
#     axs[3].fill_between(opt_per_daytime.index,
#                         opt_per_daytime_qt[opt_per_daytime_qt['level_1'] == percentiles[i]]['P_ev_opt_sum_tou_mi'],
#                         opt_per_daytime_qt[opt_per_daytime_qt['level_1'] == percentiles[-1-i]]['P_ev_opt_sum_tou_mi'],
#                         facecolors=cmap.Greens((i+1)/(n_qt_plots+1)),
#                         label=str(round(percentiles[i], 1)*100) + '-' + str(round(percentiles[-1-i], 1)*100) + '%-ile')
# axs[3].plot(opt_per_daytime.index, opt_per_daytime_qt[opt_per_daytime_qt['level_1'] ==
#                                                                 percentiles[int((n_percentiles-1)/2)]]['P_ev_opt_sum_tou_mi'],
#             color='k', label='Median')
# axs[3].grid()
# axs[3].legend()
# axs[4].plot(opt_per_daytime.index, opt_per_daytime['P_ev_opt_sum_rtp'], color='k',
#             label='Real-time prices', zorder=5, linestyle='solid')
# n_qt_plots = int((n_percentiles-1)/2)
# for i in range(n_qt_plots):
#     axs[4].fill_between(opt_per_daytime.index,
#                         opt_per_daytime_qt[opt_per_daytime_qt['level_1'] == percentiles[i]]['P_ev_opt_sum_rtp'],
#                         opt_per_daytime_qt[opt_per_daytime_qt['level_1'] == percentiles[-1-i]]['P_ev_opt_sum_rtp'],
#                         facecolors=cmap.Oranges((i+1)/(n_qt_plots+1)),
#                         label=str(round(percentiles[i], 1)*100) + '-' + str(round(percentiles[-1-i], 1)*100) + '%-ile')
# axs[4].plot(opt_per_daytime.index, opt_per_daytime_qt[opt_per_daytime_qt['level_1'] ==
#                                                                 percentiles[int((n_percentiles-1)/2)]]['P_ev_opt_sum_rtp'],
#             color='k', label='Median')
# axs[4].grid()
# axs[4].legend()
# axs[2].set_ylabel('Charging power [kW]')
# plt.xlim([0, 672])
# n_ticks = 14
# tick_range = np.linspace(start=0, stop=624, num=n_ticks)
# plt.xticks(tick_range, flex_per_daytime.loc[tick_range, 'Daytime_ID'], rotation=45)

# """
# ################################################################
# # Plot number of available vehicles and electricity prices #####
# ################################################################
# """
# # Subplots
# fig4, axs = plt.subplots(nrows=2, ncols=1, sharex=True)
# # number of available vehicles
# axs[0].plot(opt_per_daytime.index, opt_per_daytime['n_veh_avail'], color='k', label='Mean')
# n_qt_plots = int((n_percentiles-1)/2)
# for i in range(n_qt_plots):
#     axs[0].fill_between(opt_per_daytime.index,
#                         opt_per_daytime_qt[opt_per_daytime_qt['level_1'] == percentiles[i]]['n_veh_avail'],
#                         opt_per_daytime_qt[opt_per_daytime_qt['level_1'] == percentiles[-1-i]]['n_veh_avail'],
#                         facecolors=cmap.YlGn((i+1)/(n_qt_plots+1)),
#                         label=str(int(percentiles[i]*100)) + '-' + str(int(percentiles[-1-i]*100)) + '%-ile')
# axs[0].plot(opt_per_daytime.index, opt_per_daytime_qt[opt_per_daytime_qt['level_1'] ==
#                                                                 percentiles[int((n_percentiles-1)/2)]]['n_veh_avail'],
#             color='k', label='Median')
# axs[0].set_ylabel('# of available vehicles')
# axs[0].grid()
# axs[0].legend()
# # Electricity cost
# axs[1].plot(opt_per_daytime.index, opt_per_daytime['c_elect_in_const'], color='k',
#             label='Constant prices', zorder=5)
# axs[1].plot(opt_per_daytime.index, opt_per_daytime['c_elect_in_tou'], color='b',
#             label='ToU prices', zorder=0, linestyle='dashed')
# axs[1].plot(opt_per_daytime.index, opt_per_daytime['c_elect_in_rtp'], color='xkcd:orange',
#             label='Real-time prices', zorder=0, linestyle='solid')
# axs[1].set_ylabel('Electricity cost [$/kWh]')
# axs[1].grid()
# axs[1].legend()
# axs[1].set_xlabel('Date')
# plt.xlim([0, 672])
# n_ticks = 14
# tick_range = np.linspace(start=0, stop=624, num=n_ticks)
# plt.xticks(tick_range, flex_per_daytime.loc[tick_range, 'Daytime_ID'], rotation=45)
#
#
# """
# ################################################################
# # Plot mean charging power and flexibility #####################
# ################################################################
# """
# fig4, axs = plt.subplots(nrows=2, ncols=1, sharex=True)
# # Cumulated power for ev charging
# axs[0].plot(opt_per_daytime.index, opt_per_daytime['P_ev_opt_sum_const'], color='k',
#             label='Constant prices', zorder=5, linestyle='solid')
# axs[0].plot(opt_per_daytime.index, opt_per_daytime['P_ev_opt_sum_const_mi'], color='xkcd:purple',
#             label='Constant prices minimally increasing', zorder=5, linestyle='dashdot')
# axs[0].plot(opt_per_daytime.index, opt_per_daytime['P_ev_opt_sum_tou'], color='b',
#             label='ToU prices', zorder=0, linestyle='dashed')
# axs[0].plot(opt_per_daytime.index, opt_per_daytime['P_ev_opt_sum_tou_mi'], color='g',
#             label='ToU prices minimally increasing', zorder=0, linestyle='dotted')
# axs[0].plot(opt_per_daytime.index, opt_per_daytime['P_ev_opt_sum_rtp'], color='xkcd:orange',
#             label='Real-time prices', zorder=0, linestyle='solid')
# axs[0].set_ylabel('Average charging power [kW]')
# axs[0].grid()
# axs[0].legend()
# # Cumulated power for ev charging with minimal price increments
# axs[1].fill_between(flex_per_daytime.index,
#                     flex_per_daytime['P_pos_sum_const'],
#                     flex_per_daytime['P_neg_sum_const'],
#                     alpha=0.3, label='Constant prices', zorder=5, linestyle='solid', facecolor='k')
# axs[1].fill_between(flex_per_daytime.index,
#                     flex_per_daytime['P_pos_sum_const_mi'],
#                     flex_per_daytime['P_neg_sum_const_mi'],
#                     alpha=0.3, label='Constant prices minimally increasing', zorder=0,
#                     linestyle='dashdot', facecolor='xkcd:purple')
# axs[1].fill_between(flex_per_daytime.index,
#                     flex_per_daytime['P_pos_sum_tou'],
#                     flex_per_daytime['P_neg_sum_tou'],
#                     alpha=0.3, label='ToU prices', zorder=5, linestyle='dashed', facecolor='b')
# axs[1].fill_between(flex_per_daytime.index,
#                     flex_per_daytime['P_pos_sum_tou_mi'],
#                     flex_per_daytime['P_neg_sum_tou_mi'],
#                     alpha=0.3, label='ToU prices minimally increasing', zorder=0,
#                     linestyle='dotted', facecolor='g')
# axs[1].fill_between(flex_per_daytime.index,
#                     flex_per_daytime['P_pos_sum_rtp'],
#                     flex_per_daytime['P_neg_sum_rtp'],
#                     alpha=0.3, label='Real-time prices', zorder=0,
#                     linestyle='dotted', facecolor='xkcd:orange')
# axs[1].plot(flex_per_daytime.index, flex_per_daytime['P_pos_sum_const'], color='k', zorder=0,
#             linestyle='solid')        # label='Constant prices')
# axs[1].plot(flex_per_daytime.index, flex_per_daytime['P_pos_sum_const_mi'], color='xkcd:purple', zorder=0,
#             linestyle='dashdot')      # label='Constant prices minimally increasing'
# axs[1].plot(flex_per_daytime.index, flex_per_daytime['P_pos_sum_tou'], color='b', zorder=0,
#             linestyle='dashed')       # label='ToU prices'
# axs[1].plot(flex_per_daytime.index, flex_per_daytime['P_pos_sum_tou_mi'], color='g', zorder=0,
#             linestyle='dotted')       # label='ToU prices minimally increasing'
# axs[1].plot(flex_per_daytime.index, flex_per_daytime['P_pos_sum_rtp'], color='xkcd:orange', zorder=0,
#             linestyle='solid')        # label='Real-time prices',
# axs[1].plot(flex_per_daytime.index, flex_per_daytime['P_neg_sum_const'],
#             color='k', zorder=5, linestyle='solid')
# axs[1].plot(flex_per_daytime.index, flex_per_daytime['P_neg_sum_const_mi'],
#             color='xkcd:purple', zorder=0, linestyle='dashdot')
# axs[1].plot(flex_per_daytime.index, flex_per_daytime['P_neg_sum_tou'],
#             color='b', zorder=5, linestyle='dashed')
# axs[1].plot(flex_per_daytime.index, flex_per_daytime['P_neg_sum_tou_mi'],
#             color='g', zorder=0, linestyle='dotted')
# axs[1].plot(flex_per_daytime.index, flex_per_daytime['P_neg_sum_rtp'],
#             color='xkcd:orange', zorder=0, linestyle='solid')
# axs[1].set_ylabel('Flexible power [kW]')
# axs[1].grid()
# axs[1].legend()
# plt.xlim([0, 672])
# n_ticks = 14
# tick_range = np.linspace(start=0, stop=624, num=n_ticks)
# plt.xticks(tick_range, flex_per_daytime.loc[tick_range, 'Daytime_ID'], rotation=45)


# """
# ################################################################
# # Plot average flexibility over time ###########################
# ################################################################
# """
# # Subplots
# fig4, axs = plt.subplots(nrows=4, ncols=1, sharex=True)
# # number of available vehicles
# axs[0].plot(opt_per_daytime.index, opt_per_daytime['n_veh_avail'], color='k')
# axs[0].set_ylabel('# of available vehicles')
# axs[0].grid()
# # Electricity cost
# axs[1].plot(opt_per_daytime.index, opt_per_daytime['c_elect_in_const'], color='k',
#             label='Constant prices', zorder=5)
# axs[1].plot(opt_per_daytime.index, opt_per_daytime['c_elect_in_tou'], color='g',
#             label='ToU prices', zorder=0, linestyle='dashed')
# axs[1].plot(opt_per_daytime.index, opt_per_daytime['c_elect_in_rtp'], color='b',
#             label='Real-time prices', zorder=0, linestyle='solid')
# axs[1].set_ylabel('Electricity cost [$/kWh]')
# axs[1].grid()
# axs[1].legend()
# axs[1].set_xlabel('Date')
# # Cumulated power for ev charging
# axs[2].plot(opt_per_daytime.index, opt_per_daytime['P_ev_opt_sum_const'], color='k',
#             label='Constant prices', zorder=5, linestyle='solid')
# axs[2].plot(opt_per_daytime.index, opt_per_daytime['P_ev_opt_sum_const_mi'], color='k',
#             label='Constant prices minimally increasing', zorder=5, linestyle='dashdot')
# axs[2].plot(opt_per_daytime.index, opt_per_daytime['P_ev_opt_sum_tou'], color='g',
#             label='ToU prices', zorder=0, linestyle='dashed')
# axs[2].plot(opt_per_daytime.index, opt_per_daytime['P_ev_opt_sum_tou_mi'], color='g',
#             label='ToU prices minimally increasing', zorder=0, linestyle='dotted')
# axs[2].plot(opt_per_daytime.index, opt_per_daytime['P_ev_opt_sum_rtp'], color='b',
#             label='Real-time prices', zorder=0, linestyle='solid')
# axs[2].set_ylabel('Charging power [kW]')
# axs[2].grid()
# axs[2].legend()
# # Cumulated power for ev charging with minimal price increments
# axs[3].fill_between(flex_per_daytime.index,
#                     flex_per_daytime['P_pos_sum_const'],
#                     flex_per_daytime['P_neg_sum_const'],
#                     alpha=0.3, color='k', label='Constant prices', zorder=5, linestyle='solid', edgecolor='k')
# axs[3].fill_between(flex_per_daytime.index,
#                     flex_per_daytime['P_pos_sum_const_mi'],
#                     flex_per_daytime['P_neg_sum_const_mi'],
#                     alpha=0.3, color='k', label='Constant prices minimally increasing', zorder=0,
#                     linestyle='dashdot', edgecolor='k')
# axs[3].fill_between(flex_per_daytime.index,
#                     flex_per_daytime['P_pos_sum_tou'],
#                     flex_per_daytime['P_neg_sum_tou'],
#                     alpha=0.3, color='g', label='ToU prices', zorder=5, linestyle='dashed', edgecolor='g')
# axs[3].fill_between(flex_per_daytime.index,
#                     flex_per_daytime['P_pos_sum_tou_mi'],
#                     flex_per_daytime['P_neg_sum_tou_mi'],
#                     alpha=0.3, color='g', label='ToU prices minimally increasing', zorder=0,
#                     linestyle='dotted', edgecolor='g')
# axs[3].fill_between(flex_per_daytime.index,
#                     flex_per_daytime['P_pos_sum_rtp'],
#                     flex_per_daytime['P_neg_sum_rtp'],
#                     alpha=0.3, color='b', label='Real-time prices', zorder=0,
#                     linestyle='dotted', edgecolor='b')
# axs[3].plot(flex_per_daytime.index, flex_per_daytime['P_pos_sum_const'], color='k', zorder=0,
#             linestyle='solid')        # label='Constant prices')
# axs[3].plot(flex_per_daytime.index, flex_per_daytime['P_pos_sum_const_mi'], color='k', zorder=0,
#             linestyle='dashdot')      # label='Constant prices minimally increasing'
# axs[3].plot(flex_per_daytime.index, flex_per_daytime['P_pos_sum_tou'], color='g', zorder=0,
#             linestyle='dashed')       # label='ToU prices'
# axs[3].plot(flex_per_daytime.index, flex_per_daytime['P_pos_sum_tou_mi'], color='g', zorder=0,
#             linestyle='dotted')       # label='ToU prices minimally increasing'
# axs[3].plot(flex_per_daytime.index, flex_per_daytime['P_pos_sum_rtp'], color='b', zorder=0,
#             linestyle='solid')        # label='Real-time prices',
# axs[3].plot(flex_per_daytime.index, flex_per_daytime['P_neg_sum_const'],
#             color='k', zorder=5, linestyle='solid')
# axs[3].plot(flex_per_daytime.index, flex_per_daytime['P_neg_sum_const_mi'],
#             color='k', zorder=0, linestyle='dashdot')
# axs[3].plot(flex_per_daytime.index, flex_per_daytime['P_neg_sum_tou'],
#             color='g', zorder=5, linestyle='dashed')
# axs[3].plot(flex_per_daytime.index, flex_per_daytime['P_neg_sum_tou_mi'],
#             color='g', zorder=0, linestyle='dotted')
# axs[3].plot(flex_per_daytime.index, flex_per_daytime['P_neg_sum_rtp'],
#             color='b', zorder=0, linestyle='solid')
# axs[3].set_ylabel('Flexible power [kW]')
# axs[3].grid()
# axs[3].legend()
# n_ticks = 14
# tick_range = np.linspace(start=0, stop=624, num=n_ticks)
# plt.xlim([0, 672])
# plt.xticks(tick_range, flex_per_daytime.loc[tick_range, 'Daytime_ID'], rotation=45)


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
# # plt.plot(opt_per_daytime['n_veh_avail'])
