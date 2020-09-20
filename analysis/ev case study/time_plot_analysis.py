import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm as cmap
from matplotlib import rcParams
import os
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

"""
####################################################################
# Read data from hdf files #########################################
####################################################################
"""
# Output and input path
chts_output_path = 'C:/Users/ga47num/PycharmProjects/US CHTS - OpenTUMFlex - EV/Output/11/'
chts_input_path = 'C:/Users/ga47num/PycharmProjects/US CHTS - OpenTUMFlex - EV/Input/'
# Read data
chts_flex_sum_df = pd.read_hdf(chts_output_path + 'Aggregated Data/flex_sum_data.h5', key='df')
chts_opt_sum_df = pd.read_hdf(chts_output_path + 'Aggregated Data/opt_sum_data.h5', key='df')
chts_opt_per_daytime = pd.read_hdf(chts_output_path + 'Aggregated Data/opt_per_daytime_data.h5', key='df')
chts_flex_per_daytime = pd.read_hdf(chts_output_path + 'Aggregated Data/flex_per_daytime_data.h5', key='df')
chts_opt_per_daytime_qt = pd.read_hdf(chts_output_path + 'Aggregated Data/opt_per_daytime_qt_data.h5', key='df')
chts_weekday_flex_per_daytime = pd.read_hdf(chts_output_path + 'Aggregated Data/weekday_flex_per_daytime_data.h5', key='df')
chts_weekend_opt_per_daytime = pd.read_hdf(chts_output_path + 'Aggregated Data/weekend_opt_per_daytime_data.h5', key='df')
chts_weekend_flex_per_daytime = pd.read_hdf(chts_output_path + 'Aggregated Data/weekend_flex_per_daytime_data.h5', key='df')
chts_weekday_opt_per_daytime = pd.read_hdf(chts_output_path + 'Aggregated Data/weekday_opt_per_daytime_data.h5', key='df')

# Output and input path
mp_output_path = 'C:/Users/ga47num/PycharmProjects/GER MP - OpenTUMFlex - EV/Output/11/'
mp_input_path = 'C:/Users/ga47num/PycharmProjects/GER MP - OpenTUMFlex - EV/Input/'
# Read data
mp_flex_sum_df = pd.read_hdf(mp_output_path + 'Aggregated Data/flex_sum_data.h5', key='df')
mp_opt_sum_df = pd.read_hdf(mp_output_path + 'Aggregated Data/opt_sum_data.h5', key='df')
mp_opt_per_daytime = pd.read_hdf(mp_output_path + 'Aggregated Data/opt_per_daytime_data.h5', key='df')
mp_flex_per_daytime = pd.read_hdf(mp_output_path + 'Aggregated Data/flex_per_daytime_data.h5', key='df')
mp_opt_per_daytime_qt = pd.read_hdf(mp_output_path + 'Aggregated Data/opt_per_daytime_qt_data.h5', key='df')
mp_weekday_flex_per_daytime = pd.read_hdf(mp_output_path + 'Aggregated Data/weekday_flex_per_daytime_data.h5', key='df')
mp_weekend_opt_per_daytime = pd.read_hdf(mp_output_path + 'Aggregated Data/weekend_opt_per_daytime_data.h5', key='df')
mp_weekend_flex_per_daytime = pd.read_hdf(mp_output_path + 'Aggregated Data/weekend_flex_per_daytime_data.h5', key='df')
mp_weekday_opt_per_daytime = pd.read_hdf(mp_output_path + 'Aggregated Data/weekday_opt_per_daytime_data.h5', key='df')

# Define figure path
figure_path = 'X:\Projekte\SINTEG Csells\80 Veröffentlichungen\\2020-05 - OpenTUMFlex - EV Case Study\Figures\\'

# Set font/figure style
rcParams["font.family"] = "Times New Roman"
rcParams["font.size"] = 10
rcParams["figure.figsize"] = [11.69, 8.27]
chts_color = 'tab:blue'
mp_color = 'brown'

# Subplots
fig1 = plt.figure(figsize=[3.5, 3.5])
# Number of available vehicles ##############################################
plt.plot(mp_opt_per_daytime.index, mp_opt_per_daytime['n_veh_avail'] /
         mp_opt_per_daytime['n_veh_avail'].max() * 100,
         label='GER MOP', linestyle='solid', color=mp_color)
plt.plot(chts_opt_per_daytime.index, chts_opt_per_daytime['n_veh_avail'] /
         chts_opt_per_daytime['n_veh_avail'].max() * 100,
         label='US CHTS', linestyle='dashed', color=chts_color)
plt.ylabel('Available vehicles (%)')
plt.grid()
plt.legend()
plt.xlim([0, 672])
plt.ylim([0, 100])
n_ticks = 7
tick_range = np.linspace(start=0, stop=576, num=n_ticks)
plt.xticks(tick_range, labels=chts_flex_per_daytime.loc[tick_range, 'Daytime_ID'], rotation=45)
fig1.subplots_adjust(bottom=0.30, right=0.95, left=0.16, top=0.95)
plt.savefig(figure_path + 'Veh_availabilities_time.png', dpi=600)

print('mp_per_daytime[n_veh_avail]:', mp_opt_per_daytime['n_veh_avail'].max())
print('chts_per_daytime[n_veh_avail]:', chts_opt_per_daytime['n_veh_avail'].max())

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

##########################################################
# Plot only weekdays and weekends
##########################################################
n_ticks = 14
tick_range = np.linspace(start=0, stop=96, num=96)
# Figure settings
rcParams["font.family"] = "Times New Roman"
font_size = rcParams["font.size"] = 10
rcParams["figure.figsize"] = [9.5, 7.16]
#
fig5, axs = plt.subplots(nrows=4, ncols=5, sharex=True, sharey='row')
# Con
axs[0, 0].plot(tick_range, mp_weekday_opt_per_daytime['P_ev_opt_sum_const'] / mp_weekday_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid', label='GER MOP')
axs[0, 0].plot(tick_range, chts_weekday_opt_per_daytime['P_ev_opt_sum_const'] / chts_weekday_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed', label='US CHTS')
axs[0, 0].grid()
axs[0, 0].set_ylim([0, 7])
axs[0, 0].set_title('Con', fontsize=font_size)
axs[1, 0].plot(tick_range, mp_weekend_opt_per_daytime['P_ev_opt_sum_const'] / mp_weekend_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid', label='GER MOP')
axs[1, 0].plot(tick_range, chts_weekend_opt_per_daytime['P_ev_opt_sum_const'] / chts_weekend_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed', label='US CHTS')
axs[1, 0].grid()
axs[1, 0].set_ylim([0, 7])

# ToU
axs[0, 1].plot(tick_range, mp_weekday_opt_per_daytime['P_ev_opt_sum_tou'] / mp_weekday_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid', label='GER MOP')
axs[0, 1].plot(tick_range, chts_weekday_opt_per_daytime['P_ev_opt_sum_tou'] / chts_weekday_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed', label='US CHTS')
axs[0, 1].grid()
axs[0, 1].set_title('ToU', fontsize=font_size)
axs[1, 1].plot(tick_range, mp_weekend_opt_per_daytime['P_ev_opt_sum_tou'] / mp_weekend_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid', label='GER MOP')
axs[1, 1].plot(tick_range, chts_weekend_opt_per_daytime['P_ev_opt_sum_tou'] / chts_weekend_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed', label='US CHTS')
axs[1, 1].grid()

# Con + MI
axs[0, 2].plot(tick_range, mp_weekday_opt_per_daytime['P_ev_opt_sum_const_mi'] / mp_weekday_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid', label='GER MOP')
axs[0, 2].plot(tick_range, chts_weekday_opt_per_daytime['P_ev_opt_sum_const_mi'] / chts_weekday_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed', label='US CHTS')
axs[0, 2].grid()
axs[0, 2].legend(loc='upper center')

axs[0, 2].set_title('Con + MI', fontsize=font_size)
axs[1, 2].plot(tick_range, mp_weekend_opt_per_daytime['P_ev_opt_sum_const_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid', label='GER MOP')
axs[1, 2].plot(tick_range, chts_weekend_opt_per_daytime['P_ev_opt_sum_const_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed', label='US CHTS')
axs[1, 2].grid()
# ToU + MI
axs[0, 3].plot(tick_range, mp_weekday_opt_per_daytime['P_ev_opt_sum_tou_mi'] / mp_weekday_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid', label='GER MOP')
axs[0, 3].plot(tick_range, chts_weekday_opt_per_daytime['P_ev_opt_sum_tou_mi'] / chts_weekday_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed', label='US CHTS')
axs[0, 3].grid()
axs[0, 3].set_title('ToU + MI', fontsize=font_size)
axs[1, 3].plot(tick_range, mp_weekend_opt_per_daytime['P_ev_opt_sum_tou_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid', label='GER MOP')
axs[1, 3].plot(tick_range, chts_weekend_opt_per_daytime['P_ev_opt_sum_tou_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed', label='US CHTS')
axs[1, 3].grid()
# RTP
axs[0, 4].plot(tick_range, mp_weekday_opt_per_daytime['P_ev_opt_sum_rtp'] / mp_weekday_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid', label='GER MOP Weekday')
axs[0, 4].plot(tick_range, chts_weekday_opt_per_daytime['P_ev_opt_sum_rtp'] / chts_weekday_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed', label='US CHTS Weekday')
axs[0, 4].grid()
axs[0, 4].set_title('RTP', fontsize=font_size)
axs[1, 4].plot(tick_range, mp_weekend_opt_per_daytime['P_ev_opt_sum_rtp'] / mp_weekend_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid', label='GER MOP')
axs[1, 4].plot(tick_range, chts_weekend_opt_per_daytime['P_ev_opt_sum_rtp'] / chts_weekend_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed', label='US CHTS')
axs[1, 4].grid()
# Flexibility
# Con on weekdays
axs[2, 0].fill_between(tick_range,
                       mp_weekday_flex_per_daytime['P_pos_sum_const'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                       mp_weekday_flex_per_daytime['P_neg_sum_const'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='GER MOP', zorder=5, linestyle='solid', facecolor=mp_color)
axs[2, 0].fill_between(tick_range,
                       chts_weekday_flex_per_daytime['P_pos_sum_const'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                       chts_weekday_flex_per_daytime['P_neg_sum_const'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='US CHTS', zorder=5, linestyle='dashed', facecolor=chts_color)
axs[2, 0].plot(tick_range,
               chts_weekday_flex_per_daytime['P_pos_sum_const'] / chts_weekday_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[2, 0].plot(tick_range,
               mp_weekday_flex_per_daytime['P_pos_sum_const'] / mp_weekday_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[2, 0].plot(tick_range,
               chts_weekday_flex_per_daytime['P_neg_sum_const'] / chts_weekday_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[2, 0].plot(tick_range,
               mp_weekday_flex_per_daytime['P_neg_sum_const'] / mp_weekday_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[2, 0].grid()
# Con on weekends
axs[3, 0].fill_between(tick_range,
                       mp_weekend_flex_per_daytime['P_pos_sum_const'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                       mp_weekend_flex_per_daytime['P_neg_sum_const'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='GER MOP', zorder=5, linestyle='solid', facecolor=mp_color)
axs[3, 0].fill_between(tick_range,
                       chts_weekend_flex_per_daytime['P_pos_sum_const'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                       chts_weekend_flex_per_daytime['P_neg_sum_const'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='US CHTS', zorder=5, linestyle='dashed', facecolor=chts_color)
axs[3, 0].plot(tick_range,
               chts_weekend_flex_per_daytime['P_pos_sum_const'] / chts_weekend_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[3, 0].plot(tick_range,
               mp_weekend_flex_per_daytime['P_pos_sum_const'] / mp_weekend_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[3, 0].plot(tick_range,
               chts_weekend_flex_per_daytime['P_neg_sum_const'] / chts_weekend_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[3, 0].plot(tick_range,
               mp_weekend_flex_per_daytime['P_neg_sum_const'] / mp_weekend_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[3, 0].grid()
# ToU on weekdays
axs[2, 1].fill_between(tick_range,
                       mp_weekday_flex_per_daytime['P_pos_sum_tou'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                       mp_weekday_flex_per_daytime['P_neg_sum_tou'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='GER MP', zorder=5, linestyle='solid', facecolor=mp_color)
axs[2, 1].fill_between(tick_range,
                       chts_weekday_flex_per_daytime['P_pos_sum_tou'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                       chts_weekday_flex_per_daytime['P_neg_sum_tou'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='US CHTS', zorder=5, linestyle='dashed', facecolor=chts_color)
axs[2, 1].plot(tick_range,
               chts_weekday_flex_per_daytime['P_pos_sum_tou'] / chts_weekday_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[2, 1].plot(tick_range,
               mp_weekday_flex_per_daytime['P_pos_sum_tou'] / mp_weekday_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[2, 1].plot(tick_range,
               chts_weekday_flex_per_daytime['P_neg_sum_tou'] / chts_weekday_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[2, 1].plot(tick_range,
               mp_weekday_flex_per_daytime['P_neg_sum_tou'] / mp_weekday_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[2, 1].grid()
# ToU on weekends
axs[3, 1].fill_between(tick_range,
                       mp_weekend_flex_per_daytime['P_pos_sum_tou'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                       mp_weekend_flex_per_daytime['P_neg_sum_tou'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='GER MOP', zorder=5, linestyle='solid', facecolor=mp_color)
axs[3, 1].fill_between(tick_range,
                       chts_weekend_flex_per_daytime['P_pos_sum_tou'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                       chts_weekend_flex_per_daytime['P_neg_sum_tou'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='US CHTS', zorder=5, linestyle='dashed', facecolor=chts_color)
axs[3, 1].plot(tick_range,
               chts_weekend_flex_per_daytime['P_pos_sum_tou'] / chts_weekend_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[3, 1].plot(tick_range,
               mp_weekend_flex_per_daytime['P_pos_sum_tou'] / mp_weekend_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[3, 1].plot(tick_range,
               chts_weekend_flex_per_daytime['P_neg_sum_tou'] / chts_weekend_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[3, 1].plot(tick_range,
               mp_weekend_flex_per_daytime['P_neg_sum_tou'] / mp_weekend_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[3, 1].grid()
# ToU + MI on weekdays
axs[2, 3].fill_between(tick_range,
                       mp_weekday_flex_per_daytime['P_pos_sum_tou_mi'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                       mp_weekday_flex_per_daytime['P_neg_sum_tou_mi'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='GER MP', zorder=5, linestyle='solid', facecolor=mp_color)
axs[2, 3].fill_between(tick_range,
                       chts_weekday_flex_per_daytime['P_pos_sum_tou_mi'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                       chts_weekday_flex_per_daytime['P_neg_sum_tou_mi'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='US CHTS', zorder=5, linestyle='dashed', facecolor=chts_color)
axs[2, 3].plot(tick_range,
               chts_weekday_flex_per_daytime['P_pos_sum_tou_mi'] / chts_weekday_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[2, 3].plot(tick_range,
               mp_weekday_flex_per_daytime['P_pos_sum_tou_mi'] / mp_weekday_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[2, 3].plot(tick_range,
               chts_weekday_flex_per_daytime['P_neg_sum_tou_mi'] / chts_weekday_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[2, 3].plot(tick_range,
               mp_weekday_flex_per_daytime['P_neg_sum_tou_mi'] / mp_weekday_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[2, 3].grid()
# Con + MI on weekdays
axs[2, 2].fill_between(tick_range,
                       mp_weekday_flex_per_daytime['P_pos_sum_const_mi'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                       mp_weekday_flex_per_daytime['P_neg_sum_const_mi'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='GER MOP', zorder=5, linestyle='solid', facecolor=mp_color)
axs[2, 2].fill_between(tick_range,
                       chts_weekday_flex_per_daytime['P_pos_sum_const_mi'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                       chts_weekday_flex_per_daytime['P_neg_sum_const_mi'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='US CHTS', zorder=5, linestyle='dashed', facecolor=chts_color)
axs[2, 2].plot(tick_range,
               chts_weekday_flex_per_daytime['P_pos_sum_const_mi'] / chts_weekday_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[2, 2].plot(tick_range,
               mp_weekday_flex_per_daytime['P_pos_sum_const_mi'] / mp_weekday_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[2, 2].plot(tick_range,
               chts_weekday_flex_per_daytime['P_neg_sum_const_mi'] / chts_weekday_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[2, 2].plot(tick_range,
               mp_weekday_flex_per_daytime['P_neg_sum_const_mi'] / mp_weekday_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[2, 2].grid()
axs[2, 2].legend(loc='lower center')
# Con + MI on weekends
axs[3, 2].fill_between(tick_range,
                       mp_weekend_flex_per_daytime['P_pos_sum_const_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                       mp_weekend_flex_per_daytime['P_neg_sum_const_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='GER MOP Con+MI', zorder=5, linestyle='solid', facecolor=mp_color)
axs[3, 2].fill_between(tick_range,
                       chts_weekend_flex_per_daytime['P_pos_sum_const_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                       chts_weekend_flex_per_daytime['P_neg_sum_const_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='US CHTS Con+MI', zorder=5, linestyle='dashed', facecolor=chts_color)
axs[3, 2].plot(tick_range,
               chts_weekend_flex_per_daytime['P_pos_sum_const_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[3, 2].plot(tick_range,
               mp_weekend_flex_per_daytime['P_pos_sum_const_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[3, 2].plot(tick_range,
               chts_weekend_flex_per_daytime['P_neg_sum_const_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[3, 2].plot(tick_range,
               mp_weekend_flex_per_daytime['P_neg_sum_const_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[3, 2].grid()
# ToU + MI on weekends
axs[3, 3].fill_between(tick_range,
                       mp_weekend_flex_per_daytime['P_pos_sum_tou_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                       mp_weekend_flex_per_daytime['P_neg_sum_tou_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='GER MOP ToU+MI', zorder=5, linestyle='solid', facecolor=mp_color)
axs[3, 3].fill_between(tick_range,
                       chts_weekend_flex_per_daytime['P_pos_sum_tou_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                       chts_weekend_flex_per_daytime['P_neg_sum_tou_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='US CHTS ToU+MI', zorder=5, linestyle='dashed', facecolor=chts_color)
axs[3, 3].plot(tick_range,
               chts_weekend_flex_per_daytime['P_pos_sum_tou_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[3, 3].plot(tick_range,
               mp_weekend_flex_per_daytime['P_pos_sum_tou_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[3, 3].plot(tick_range,
               chts_weekend_flex_per_daytime['P_neg_sum_tou_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[3, 3].plot(tick_range,
               mp_weekend_flex_per_daytime['P_neg_sum_tou_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[3, 3].grid()
# RTP on weekdays
axs[2, 4].fill_between(tick_range,
                       mp_weekday_flex_per_daytime['P_pos_sum_rtp'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                       mp_weekday_flex_per_daytime['P_neg_sum_rtp'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='GER MP RTP', zorder=5, linestyle='solid', facecolor=mp_color)
axs[2, 4].fill_between(tick_range,
                       chts_weekday_flex_per_daytime['P_pos_sum_rtp'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                       chts_weekday_flex_per_daytime['P_neg_sum_rtp'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='US CHTS RTP', zorder=5, linestyle='dashed', facecolor=chts_color)
axs[2, 4].plot(tick_range,
               chts_weekday_flex_per_daytime['P_pos_sum_rtp'] / chts_weekday_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[2, 4].plot(tick_range,
               mp_weekday_flex_per_daytime['P_pos_sum_rtp'] / mp_weekday_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[2, 4].plot(tick_range,
               chts_weekday_flex_per_daytime['P_neg_sum_rtp'] / chts_weekday_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[2, 4].plot(tick_range,
               mp_weekday_flex_per_daytime['P_neg_sum_rtp'] / mp_weekday_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[2, 4].grid()
axs[2, 4].set_ylim([-10, 7])
# RTP on weekends
axs[3, 4].fill_between(tick_range,
                       mp_weekend_flex_per_daytime['P_pos_sum_rtp'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                       mp_weekend_flex_per_daytime['P_neg_sum_rtp'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='GER MOP RTP', zorder=5, linestyle='solid', facecolor=mp_color)
axs[3, 4].fill_between(tick_range,
                       chts_weekend_flex_per_daytime['P_pos_sum_rtp'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                       chts_weekend_flex_per_daytime['P_neg_sum_rtp'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                       alpha=0.5, label='US CHTS RTP', zorder=5, linestyle='dashed', facecolor=chts_color)
axs[3, 4].plot(tick_range,
               chts_weekend_flex_per_daytime['P_pos_sum_rtp'] / chts_weekend_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[3, 4].plot(tick_range,
               mp_weekend_flex_per_daytime['P_pos_sum_rtp'] / mp_weekend_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[3, 4].plot(tick_range,
               chts_weekend_flex_per_daytime['P_neg_sum_rtp'] / chts_weekend_opt_per_daytime['n_veh_avail'],
               color=chts_color, linestyle='dashed')
axs[3, 4].plot(tick_range,
               mp_weekend_flex_per_daytime['P_neg_sum_rtp'] / mp_weekend_opt_per_daytime['n_veh_avail'],
               color=mp_color, linestyle='solid')
axs[3, 4].grid()
axs[3, 4].set_ylim([-10, 7])


axs[0, 0].set_ylabel('Charging power per available vehicle $(kW \cdot EV^{-1})$ \n '
                     'Weekend                              Weekday',
                     position=(0, -0.1))
axs[2, 0].set_ylabel('Flexible power per available vehicle $(kW \cdot EV^{-1})$ \n '
                     'Weekend                              Weekday',
                     position=(0, -0.1))
n_ticks = 5
ticks = [int(x) for x in np.linspace(start=0, stop=96, num=n_ticks)]
tick_labels = pd.date_range(start='2020-01-01 00:00', end='2020-01-02 00:00', freq='15Min').strftime('%H:%M').to_list()
resulting_labels = [tick_labels[i] for i in ticks]
axs[0, 0].set_xlim([0, 97])
axs[0, 0].set_xticks(ticks)
axs[0, 0].set_xticklabels(resulting_labels, rotation=45)
plt.subplots_adjust(left=0.08, bottom=0.05, right=0.98, top=0.95, wspace=0.25, hspace=0.2)
plt.savefig(figure_path + 'opt_flex_average_day_plots.png', dpi=600)

# # Set figure size
# rcParams["figure.figsize"] = [11.69, 8.27]
#
# """
# ##################################################################
# # Week long time series ##########################################
# ##################################################################
# """
# n_percentiles = 9           # Define number of percentiles
# percentiles = np.linspace(start=0.1, stop=0.9, num=n_percentiles).round(decimals=1)
# chts_opt_per_daytime_qt['level_1'] = chts_opt_per_daytime_qt['level_1'].round(decimals=1)
# mp_opt_per_daytime_qt['level_1'] = mp_opt_per_daytime_qt['level_1'].round(decimals=1)
# # Subplots
# fig4, axs = plt.subplots(nrows=4, ncols=2, sharex=True)
# # Number of available vehicles ##############################################
# # CHTS
# axs[0, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['n_veh_avail'], color='k', label='Mean')
# n_qt_plots = int((n_percentiles-1)/2)
# for i in range(n_qt_plots):
#     axs[0, 0].fill_between(chts_opt_per_daytime.index,
#                            chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] == percentiles[i]]['n_veh_avail'],
#                            chts_opt_per_daytime_qt[chts_opt_per_daytime_qt['level_1'] == percentiles[-1-i]]['n_veh_avail'],
#                            facecolors=cmap.YlGn((i+1)/(n_qt_plots+1)),
#                            label=str(int(percentiles[i]*100)) + '-' + str(int(percentiles[-1-i]*100)) + '%-ile')
# # axs[0].plot(opt_per_daytime.index, opt_per_daytime_qt[opt_per_daytime_qt['level_1'] ==
# #                                                                 percentiles[int((n_percentiles-1)/2)]]['n_veh_avail'],
# #             color='k', label='Median')
# axs[0, 0].set_ylabel('# of available vehicles')
# axs[0, 0].grid()
# axs[0, 0].legend()
# # MP
# axs[0, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['n_veh_avail'], color='k', label='Mean')
# n_qt_plots = int((n_percentiles-1)/2)
# for i in range(n_qt_plots):
#     axs[0, 1].fill_between(mp_opt_per_daytime.index,
#                            mp_opt_per_daytime_qt[mp_opt_per_daytime_qt['level_1'] == percentiles[i]]['n_veh_avail'],
#                            mp_opt_per_daytime_qt[mp_opt_per_daytime_qt['level_1'] == percentiles[-1-i]]['n_veh_avail'],
#                            facecolors=cmap.YlGn((i+1)/(n_qt_plots+1)),
#                            label=str(int(percentiles[i]*100)) + '-' + str(int(percentiles[-1-i]*100)) + '%-ile')
# # axs[0].plot(opt_per_daytime.index, opt_per_daytime_qt[opt_per_daytime_qt['level_1'] ==
# #                                                                 percentiles[int((n_percentiles-1)/2)]]['n_veh_avail'],
# #             color='k', label='Median')
# axs[0, 1].set_ylabel('# of available vehicles')
# axs[0, 1].grid()
# axs[0, 1].legend()
# # Electricity cost ##########################
# # CHTS
# axs[1, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['c_elect_in_const'], color='k',
#                label='Constant prices', zorder=5)
# axs[1, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['c_elect_in_tou'], color='b',
#                label='ToU prices', zorder=0, linestyle='dashed')
# axs[1, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['c_elect_in_rtp'], color='xkcd:orange',
#                label='Real-time prices', zorder=0, linestyle='solid')
# axs[1, 0].set_ylabel('Electricity cost [$/kWh]')
# axs[1, 0].grid()
# axs[1, 0].legend()
# # MP
# axs[1, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['c_elect_in_const'], color='k',
#                label='Constant prices', zorder=5)
# axs[1, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['c_elect_in_tou'], color='b',
#                label='ToU prices', zorder=0, linestyle='dashed')
# axs[1, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['c_elect_in_rtp'], color='xkcd:orange',
#                label='Real-time prices', zorder=0, linestyle='solid')
# axs[1, 1].set_ylabel('Electricity cost [$/kWh]')
# axs[1, 1].grid()
# axs[1, 1].legend()
# # Cumulated power for ev charging ######################
# # CHTS
# axs[2, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_const'], color='k',
#                label='Constant prices', zorder=5, linestyle='solid')
# axs[2, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_const_mi'], color='xkcd:purple',
#                label='Constant prices minimally increasing', zorder=5, linestyle='dashdot')
# axs[2, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_tou'], color='b',
#                label='ToU prices', zorder=0, linestyle='dashed')
# axs[2, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_tou_mi'], color='g',
#                label='ToU prices minimally increasing', zorder=0, linestyle='dotted')
# axs[2, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_rtp'], color='xkcd:orange',
#                label='Real-time prices', zorder=0, linestyle='solid')
# axs[2, 0].set_ylabel('Average charging power [kW]')
# axs[2, 0].grid()
# axs[2, 0].legend()
# # MP
# axs[2, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['P_ev_opt_sum_const'], color='k',
#                label='Constant prices', zorder=5, linestyle='solid')
# axs[2, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['P_ev_opt_sum_const_mi'], color='xkcd:purple',
#                label='Constant prices minimally increasing', zorder=5, linestyle='dashdot')
# axs[2, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['P_ev_opt_sum_tou'], color='b',
#                label='ToU prices', zorder=0, linestyle='dashed')
# axs[2, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['P_ev_opt_sum_tou_mi'], color='g',
#                label='ToU prices minimally increasing', zorder=0, linestyle='dotted')
# axs[2, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['P_ev_opt_sum_rtp'], color='xkcd:orange',
#                label='Real-time prices', zorder=0, linestyle='solid')
# axs[2, 1].set_ylabel('Average charging power [kW]')
# axs[2, 1].grid()
# axs[2, 1].legend()
# # Flexible Power ###########################################
# # CHTS
# axs[3, 0].fill_between(chts_flex_per_daytime.index,
#                        chts_flex_per_daytime['P_pos_sum_const'],
#                        chts_flex_per_daytime['P_neg_sum_const'],
#                        alpha=0.3, label='Constant prices', zorder=5, linestyle='solid', facecolor='k')
# axs[3, 0].fill_between(chts_flex_per_daytime.index,
#                     chts_flex_per_daytime['P_pos_sum_const_mi'],
#                     chts_flex_per_daytime['P_neg_sum_const_mi'],
#                     alpha=0.3, label='Constant prices minimally increasing', zorder=0,
#                     linestyle='dashdot', facecolor='xkcd:purple')
# axs[3, 0].fill_between(chts_flex_per_daytime.index,
#                     chts_flex_per_daytime['P_pos_sum_tou'],
#                     chts_flex_per_daytime['P_neg_sum_tou'],
#                     alpha=0.3, label='ToU prices', zorder=5, linestyle='dashed', facecolor='b')
# axs[3, 0].fill_between(chts_flex_per_daytime.index,
#                     chts_flex_per_daytime['P_pos_sum_tou_mi'],
#                     chts_flex_per_daytime['P_neg_sum_tou_mi'],
#                     alpha=0.3, label='ToU prices minimally increasing', zorder=0,
#                     linestyle='dotted', facecolor='g')
# axs[3, 0].fill_between(chts_flex_per_daytime.index,
#                     chts_flex_per_daytime['P_pos_sum_rtp'],
#                     chts_flex_per_daytime['P_neg_sum_rtp'],
#                     alpha=0.3, label='Real-time prices', zorder=0,
#                     linestyle='dotted', facecolor='xkcd:orange')
# axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_const'], color='k', zorder=0,
#             linestyle='solid')        # label='Constant prices')
# axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_const_mi'], color='xkcd:purple', zorder=0,
#             linestyle='dashdot')      # label='Constant prices minimally increasing'
# axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_tou'], color='b', zorder=0,
#             linestyle='dashed')       # label='ToU prices'
# axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_tou_mi'], color='g', zorder=0,
#             linestyle='dotted')       # label='ToU prices minimally increasing'
# axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_rtp'], color='xkcd:orange', zorder=0,
#             linestyle='solid')        # label='Real-time prices',
# axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_const'],
#             color='k', zorder=5, linestyle='solid')
# axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_const_mi'],
#             color='xkcd:purple', zorder=0, linestyle='dashdot')
# axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_tou'],
#             color='b', zorder=5, linestyle='dashed')
# axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_tou_mi'],
#             color='g', zorder=0, linestyle='dotted')
# axs[3, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_rtp'],
#             color='xkcd:orange', zorder=0, linestyle='solid')
# axs[3, 0].set_ylabel('Flexible power [kW]')
# axs[3, 0].grid()
# axs[3, 0].legend()
# # MP
# axs[3, 1].fill_between(mp_flex_per_daytime.index,
#                        mp_flex_per_daytime['P_pos_sum_const'],
#                        mp_flex_per_daytime['P_neg_sum_const'],
#                        alpha=0.3, label='Constant prices', zorder=5, linestyle='solid', facecolor='k')
# axs[3, 1].fill_between(mp_flex_per_daytime.index,
#                        mp_flex_per_daytime['P_pos_sum_const_mi'],
#                        mp_flex_per_daytime['P_neg_sum_const_mi'],
#                        alpha=0.3, label='Constant prices minimally increasing', zorder=0,
#                        linestyle='dashdot', facecolor='xkcd:purple')
# axs[3, 1].fill_between(mp_flex_per_daytime.index,
#                        mp_flex_per_daytime['P_pos_sum_tou'],
#                        mp_flex_per_daytime['P_neg_sum_tou'],
#                        alpha=0.3, label='ToU prices', zorder=5, linestyle='dashed', facecolor='b')
# axs[3, 1].fill_between(mp_flex_per_daytime.index,
#                        mp_flex_per_daytime['P_pos_sum_tou_mi'],
#                        mp_flex_per_daytime['P_neg_sum_tou_mi'],
#                        alpha=0.3, label='ToU prices minimally increasing', zorder=0,
#                        linestyle='dotted', facecolor='g')
# axs[3, 1].fill_between(mp_flex_per_daytime.index,
#                        mp_flex_per_daytime['P_pos_sum_rtp'],
#                        mp_flex_per_daytime['P_neg_sum_rtp'],
#                        alpha=0.3, label='Real-time prices', zorder=0,
#                        linestyle='dotted', facecolor='xkcd:orange')
# axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_const'], color='k', zorder=0,
#                linestyle='solid')        # label='Constant prices')
# axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_const_mi'], color='xkcd:purple', zorder=0,
#                linestyle='dashdot')      # label='Constant prices minimally increasing'
# axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_tou'], color='b', zorder=0,
#                linestyle='dashed')       # label='ToU prices'
# axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_tou_mi'], color='g', zorder=0,
#                linestyle='dotted')       # label='ToU prices minimally increasing'
# axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_rtp'], color='xkcd:orange', zorder=0,
#                linestyle='solid')        # label='Real-time prices',
# axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_neg_sum_const'],
#                color='k', zorder=5, linestyle='solid')
# axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_neg_sum_const_mi'],
#                color='xkcd:purple', zorder=0, linestyle='dashdot')
# axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_neg_sum_tou'],
#                color='b', zorder=5, linestyle='dashed')
# axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_neg_sum_tou_mi'],
#                color='g', zorder=0, linestyle='dotted')
# axs[3, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_neg_sum_rtp'],
#                color='xkcd:orange', zorder=0, linestyle='solid')
# axs[3, 1].set_ylabel('Flexible power [kW]')
# axs[3, 1].grid()
# axs[3, 1].legend()
# plt.xlim([0, 672])
# n_ticks = 14
# tick_range = np.linspace(start=0, stop=624, num=n_ticks)
# axs[3, 0].set_xticks(tick_range)
# axs[3, 1].set_xticks(tick_range)
# axs[3, 0].set_xticklabels(chts_flex_per_daytime.loc[tick_range, 'Daytime_ID'], rotation=45)
# axs[3, 1].set_xticklabels(chts_flex_per_daytime.loc[tick_range, 'Daytime_ID'], rotation=45)


# # Subplots
# fig1 = plt.figure(figsize=[7, 4.5])
# # Number of available vehicles ##############################################
# plt.plot(mp_opt_per_daytime.index, mp_opt_per_daytime['n_veh_avail'], label='GER MP')
# plt.plot(chts_opt_per_daytime.index, chts_opt_per_daytime['n_veh_avail'], label='US CHTS')
# plt.ylabel('# of available vehicles')
# plt.grid()
# plt.legend()
# plt.xlim([0, 672])
# n_ticks = 14
# tick_range = np.linspace(start=0, stop=624, num=n_ticks)
# plt.xticks(tick_range, labels=chts_flex_per_daytime.loc[tick_range, 'Daytime_ID'], rotation=45)
# fig1.subplots_adjust(bottom=0.30)
# plt.savefig(figure_path + 'Veh_availabilities_time.png', dpi=600)

