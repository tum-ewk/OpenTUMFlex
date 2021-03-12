"""
This module visualizes the flexibility prices and for a better overview includes the price forecast as well as the
calculated flexibility power in combination with the scheduled optimal charging power over time.
"""

__author__ = "Helena Hahne"
__copyright__ = "2021 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "0"
__maintainer__ = "?"
__email__ = "?"
__status__ = "Development"

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
from pandas.plotting import register_matplotlib_converters
from pathlib import Path

register_matplotlib_converters()

'''
def plot_n_avail_veh(output_path, save_figure=True, figure_path='../figures/'):
    """
    Plots the vehicle availabilities of a case study.

    :param save_figure: boolean whether to save figure or not
    :param output_path: path to results of the case study
    :param figure_path: folder where figures are stored
    :return:
    """
    # Read data from files
    opt_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/opt_per_daytime_data.h5', key='df')
    flex_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/flex_per_daytime_data.h5', key='df')
    # Set font/figure style
    rcParams["font.family"] = "Times New Roman"
    # rcParams["font.size"] = 10
    # rcParams["figure.figsize"] = [11.69, 8.27]
    plot_color = 'brown'

    # Subplots
    fig1 = plt.figure(figsize=[6, 3.5])
    # Number of available vehicles ##############################################
    plt.plot(opt_per_daytime.index, opt_per_daytime['n_veh_avail'] /
             opt_per_daytime['n_veh_avail'].max() * 100, linestyle='solid', color=plot_color)
    plt.ylabel('Available vehicles (%)')
    plt.grid()
    plt.xlim([0, 672])
    plt.ylim([0, 100])
    n_ticks = 7
    tick_range = np.linspace(start=0, stop=576, num=n_ticks)
    plt.xticks(tick_range, labels=flex_per_daytime.loc[tick_range, 'Daytime_ID'], rotation=45)
    fig1.subplots_adjust(bottom=0.30, right=0.95, left=0.16, top=0.95)
    if save_figure:
        plt.savefig(figure_path + 'veh_availabilities_time.png', dpi=600)

    # print('Maximum number of available vehicles:', opt_per_daytime['n_veh_avail'].max())
'''
'''
def plot_opt_flex_timeseries(power, cs1_output_path, cs2_output_path, save_figure=True, figure_path='../figures/'):
    """
    This function plots the flexibility results of two case studies over time

    :param save_figure: boolean whether to save figure or not
    :param cs1_output_path: path to results of the first case study
    :param cs2_output_path: path to results of the second case study
    :param figure_path: folder where figures are stored
    :param power: current power level
    :return:
    """

    # Set font/figure style
    rcParams["font.family"] = "Times New Roman"
    rcParams["font.size"] = 10
    rcParams["figure.figsize"] = [11.69, 8.27]
    chts_color = 'tab:blue'
    mp_color = 'brown'

    # Read aggregated data from hdf files #########################################
    # US CHTS
    chts_opt_per_daytime = pd.read_hdf(cs1_output_path + 'Aggregated Data/opt_per_daytime_data.h5', key='df')
    chts_flex_per_daytime = pd.read_hdf(cs1_output_path + 'Aggregated Data/flex_per_daytime_data.h5', key='df')
    chts_weekday_flex_per_daytime = pd.read_hdf(cs1_output_path + 'Aggregated Data/weekday_flex_per_daytime_data.h5', key='df')
    chts_weekend_opt_per_daytime = pd.read_hdf(cs1_output_path + 'Aggregated Data/weekend_opt_per_daytime_data.h5', key='df')
    chts_weekend_flex_per_daytime = pd.read_hdf(cs1_output_path + 'Aggregated Data/weekend_flex_per_daytime_data.h5', key='df')
    chts_weekday_opt_per_daytime = pd.read_hdf(cs1_output_path + 'Aggregated Data/weekday_opt_per_daytime_data.h5', key='df')
    # GER MP
    mp_opt_per_daytime = pd.read_hdf(cs2_output_path + 'Aggregated Data/opt_per_daytime_data.h5', key='df')
    mp_flex_per_daytime = pd.read_hdf(cs2_output_path + 'Aggregated Data/flex_per_daytime_data.h5', key='df')
    mp_weekday_flex_per_daytime = pd.read_hdf(cs2_output_path + 'Aggregated Data/weekday_flex_per_daytime_data.h5', key='df')
    mp_weekend_opt_per_daytime = pd.read_hdf(cs2_output_path + 'Aggregated Data/weekend_opt_per_daytime_data.h5', key='df')
    mp_weekend_flex_per_daytime = pd.read_hdf(cs2_output_path + 'Aggregated Data/weekend_flex_per_daytime_data.h5', key='df')
    mp_weekday_opt_per_daytime = pd.read_hdf(cs2_output_path + 'Aggregated Data/weekday_opt_per_daytime_data.h5', key='df')

    # Subplots
    fig4, axs = plt.subplots(nrows=2, ncols=2, sharex=True)
    # Cumulated power for ev charging ######################
    # CHTS
    axs[0, 0].set_title('California household travel survey, US')
    axs[0, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_con'], color='k',
                   label='Constant prices', zorder=5, linestyle='solid')
    axs[0, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_con_mi'], color='xkcd:purple',
                   label='Constant prices minimally increasing', zorder=5, linestyle='dashdot')
    axs[0, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_tou'], color='b',
                   label='ToU prices', zorder=0, linestyle='solid')
    axs[0, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_tou_mi'], color='g',
                   label='ToU prices minimally increasing', zorder=0, linestyle='dotted')
    axs[0, 0].plot(chts_opt_per_daytime.index, chts_opt_per_daytime['P_ev_opt_sum_rtp'], color='xkcd:orange',
                   label='Real-time prices', zorder=0, linestyle='solid')
    axs[0, 0].set_ylabel('Average charging power [kW]')
    axs[0, 0].grid()
    axs[0, 0].legend()
    # MP
    axs[0, 1].set_title('German Mobility Panel, GER')
    axs[0, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['P_ev_opt_sum_con'], color='k',
                   label='Constant prices', zorder=5, linestyle='solid')
    axs[0, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['P_ev_opt_sum_con_mi'], color='xkcd:purple',
                   label='Constant prices minimally increasing', zorder=5, linestyle='dashdot')
    axs[0, 1].plot(mp_opt_per_daytime.index, mp_opt_per_daytime['P_ev_opt_sum_tou'], color='b',
                   label='ToU prices', zorder=0, linestyle='solid')
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
                           chts_flex_per_daytime['P_pos_sum_con'],
                           chts_flex_per_daytime['P_neg_sum_con'],
                           alpha=0.3, label='Constant prices', zorder=5, linestyle='solid', facecolor='k')
    axs[1, 0].fill_between(chts_flex_per_daytime.index,
                           chts_flex_per_daytime['P_pos_sum_con_mi'],
                           chts_flex_per_daytime['P_neg_sum_con_mi'],
                           alpha=0.3, label='Constant prices minimally increasing', zorder=0,
                           linestyle='dashdot', facecolor='xkcd:purple')
    axs[1, 0].fill_between(chts_flex_per_daytime.index,
                        chts_flex_per_daytime['P_pos_sum_tou'],
                        chts_flex_per_daytime['P_neg_sum_tou'],
                        alpha=0.3, label='ToU prices', zorder=5, linestyle='solid', facecolor='b')
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
    axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_con'], color='k', zorder=0,
                linestyle='solid')        # label='Constant prices')
    axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_con_mi'], color='xkcd:purple', zorder=0,
                linestyle='dashdot')      # label='Constant prices minimally increasing'
    axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_tou'], color='b', zorder=0,
                linestyle='solid')       # label='ToU prices'
    axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_tou_mi'], color='g', zorder=0,
                linestyle='dotted')       # label='ToU prices minimally increasing'
    axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_pos_sum_rtp'], color='xkcd:orange', zorder=0,
                linestyle='solid')        # label='Real-time prices',
    axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_con'],
                color='k', zorder=5, linestyle='solid')
    axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_con_mi'],
                color='xkcd:purple', zorder=0, linestyle='dashdot')
    axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_tou'],
                color='b', zorder=5, linestyle='solid')
    axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_tou_mi'],
                color='g', zorder=0, linestyle='dotted')
    axs[1, 0].plot(chts_flex_per_daytime.index, chts_flex_per_daytime['P_neg_sum_rtp'],
                color='xkcd:orange', zorder=0, linestyle='solid')
    axs[1, 0].set_ylabel('Flexible power [kW]')
    axs[1, 0].grid()
    axs[1, 0].legend()
    # MP
    axs[1, 1].fill_between(mp_flex_per_daytime.index,
                           mp_flex_per_daytime['P_pos_sum_con'],
                           mp_flex_per_daytime['P_neg_sum_con'],
                           alpha=0.3, label='Constant prices', zorder=5, linestyle='solid', facecolor='k')
    axs[1, 1].fill_between(mp_flex_per_daytime.index,
                           mp_flex_per_daytime['P_pos_sum_con_mi'],
                           mp_flex_per_daytime['P_neg_sum_con_mi'],
                           alpha=0.3, label='Constant prices minimally increasing', zorder=0,
                           linestyle='dashdot', facecolor='xkcd:purple')
    axs[1, 1].fill_between(mp_flex_per_daytime.index,
                           mp_flex_per_daytime['P_pos_sum_tou'],
                           mp_flex_per_daytime['P_neg_sum_tou'],
                           alpha=0.3, label='ToU prices', zorder=5, linestyle='solid', facecolor='b')
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
    axs[1, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_con'], color='k', zorder=0,
                   linestyle='solid')        # label='Constant prices')
    axs[1, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_con_mi'], color='xkcd:purple', zorder=0,
                   linestyle='dashdot')      # label='Constant prices minimally increasing'
    axs[1, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_tou'], color='b', zorder=0,
                   linestyle='solid')       # label='ToU prices'
    axs[1, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_tou_mi'], color='g', zorder=0,
                   linestyle='dotted')       # label='ToU prices minimally increasing'
    axs[1, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_pos_sum_rtp'], color='xkcd:orange', zorder=0,
                   linestyle='solid')        # label='Real-time prices',
    axs[1, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_neg_sum_con'],
                   color='k', zorder=5, linestyle='solid')
    axs[1, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_neg_sum_con_mi'],
                   color='xkcd:purple', zorder=0, linestyle='dashdot')
    axs[1, 1].plot(mp_flex_per_daytime.index, mp_flex_per_daytime['P_neg_sum_tou'],
                   color='b', zorder=5, linestyle='solid')
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
    axs[0, 0].plot(tick_range, mp_weekday_opt_per_daytime['P_ev_opt_sum_con'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid', label='GER MP')
    axs[0, 0].plot(tick_range, chts_weekday_opt_per_daytime['P_ev_opt_sum_con'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid', label='US CHTS')
    axs[0, 0].grid()
    axs[0, 0].set_ylim([0, 7])
    axs[0, 0].set_title('Con', fontsize=font_size)
    axs[1, 0].plot(tick_range, mp_weekend_opt_per_daytime['P_ev_opt_sum_con'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid', label='GER MP')
    axs[1, 0].plot(tick_range, chts_weekend_opt_per_daytime['P_ev_opt_sum_con'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid', label='US CHTS')
    axs[1, 0].grid()
    axs[1, 0].set_ylim([0, 7])

    # ToU
    axs[0, 1].plot(tick_range, mp_weekday_opt_per_daytime['P_ev_opt_sum_tou'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid', label='GER MP')
    axs[0, 1].plot(tick_range, chts_weekday_opt_per_daytime['P_ev_opt_sum_tou'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid', label='US CHTS')
    axs[0, 1].grid()
    axs[0, 1].set_title('ToU', fontsize=font_size)
    axs[1, 1].plot(tick_range, mp_weekend_opt_per_daytime['P_ev_opt_sum_tou'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid', label='GER MP')
    axs[1, 1].plot(tick_range, chts_weekend_opt_per_daytime['P_ev_opt_sum_tou'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid', label='US CHTS')
    axs[1, 1].grid()

    # Con + MI
    axs[0, 2].plot(tick_range, mp_weekday_opt_per_daytime['P_ev_opt_sum_con_mi'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid', label='GER MP')
    axs[0, 2].plot(tick_range, chts_weekday_opt_per_daytime['P_ev_opt_sum_con_mi'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid', label='US CHTS')
    axs[0, 2].grid()
    axs[0, 2].legend(loc='upper center')

    axs[0, 2].set_title('Con + MI', fontsize=font_size)
    axs[1, 2].plot(tick_range, mp_weekend_opt_per_daytime['P_ev_opt_sum_con_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid', label='GER MP')
    axs[1, 2].plot(tick_range, chts_weekend_opt_per_daytime['P_ev_opt_sum_con_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid', label='US CHTS')
    axs[1, 2].grid()
    # ToU + MI
    axs[0, 3].plot(tick_range, mp_weekday_opt_per_daytime['P_ev_opt_sum_tou_mi'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid', label='GER MP')
    axs[0, 3].plot(tick_range, chts_weekday_opt_per_daytime['P_ev_opt_sum_tou_mi'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid', label='US CHTS')
    axs[0, 3].grid()
    axs[0, 3].set_title('ToU + MI', fontsize=font_size)
    axs[1, 3].plot(tick_range, mp_weekend_opt_per_daytime['P_ev_opt_sum_tou_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid', label='GER MP')
    axs[1, 3].plot(tick_range, chts_weekend_opt_per_daytime['P_ev_opt_sum_tou_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid', label='US CHTS')
    axs[1, 3].grid()
    # RTP
    axs[0, 4].plot(tick_range, mp_weekday_opt_per_daytime['P_ev_opt_sum_rtp'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid', label='GER MP Weekday')
    axs[0, 4].plot(tick_range, chts_weekday_opt_per_daytime['P_ev_opt_sum_rtp'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid', label='US CHTS Weekday')
    axs[0, 4].grid()
    axs[0, 4].set_title('RTP', fontsize=font_size)
    axs[1, 4].plot(tick_range, mp_weekend_opt_per_daytime['P_ev_opt_sum_rtp'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid', label='GER MP')
    axs[1, 4].plot(tick_range, chts_weekend_opt_per_daytime['P_ev_opt_sum_rtp'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid', label='US CHTS')
    axs[1, 4].grid()
    # Flexibility
    # Con on weekdays
    axs[2, 0].fill_between(tick_range,
                           mp_weekday_flex_per_daytime['P_pos_sum_con'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                           mp_weekday_flex_per_daytime['P_neg_sum_con'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                           alpha=0.5, label='GER MP', zorder=5, linestyle='solid', facecolor=mp_color)
    axs[2, 0].fill_between(tick_range,
                           chts_weekday_flex_per_daytime['P_pos_sum_con'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                           chts_weekday_flex_per_daytime['P_neg_sum_con'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                           alpha=0.5, label='US CHTS', zorder=5, linestyle='solid', facecolor=chts_color)
    axs[2, 0].plot(tick_range,
                   chts_weekday_flex_per_daytime['P_pos_sum_con'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
    axs[2, 0].plot(tick_range,
                   mp_weekday_flex_per_daytime['P_pos_sum_con'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid')
    axs[2, 0].plot(tick_range,
                   chts_weekday_flex_per_daytime['P_neg_sum_con'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
    axs[2, 0].plot(tick_range,
                   mp_weekday_flex_per_daytime['P_neg_sum_con'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid')
    axs[2, 0].grid()
    # Con on weekends
    axs[3, 0].fill_between(tick_range,
                           mp_weekend_flex_per_daytime['P_pos_sum_con'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                           mp_weekend_flex_per_daytime['P_neg_sum_con'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                           alpha=0.5, label='GER MP', zorder=5, linestyle='solid', facecolor=mp_color)
    axs[3, 0].fill_between(tick_range,
                           chts_weekend_flex_per_daytime['P_pos_sum_con'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                           chts_weekend_flex_per_daytime['P_neg_sum_con'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                           alpha=0.5, label='US CHTS', zorder=5, linestyle='solid', facecolor=chts_color)
    axs[3, 0].plot(tick_range,
                   chts_weekend_flex_per_daytime['P_pos_sum_con'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
    axs[3, 0].plot(tick_range,
                   mp_weekend_flex_per_daytime['P_pos_sum_con'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid')
    axs[3, 0].plot(tick_range,
                   chts_weekend_flex_per_daytime['P_neg_sum_con'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
    axs[3, 0].plot(tick_range,
                   mp_weekend_flex_per_daytime['P_neg_sum_con'] / mp_weekend_opt_per_daytime['n_veh_avail'],
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
                           alpha=0.5, label='US CHTS', zorder=5, linestyle='solid', facecolor=chts_color)
    axs[2, 1].plot(tick_range,
                   chts_weekday_flex_per_daytime['P_pos_sum_tou'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
    axs[2, 1].plot(tick_range,
                   mp_weekday_flex_per_daytime['P_pos_sum_tou'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid')
    axs[2, 1].plot(tick_range,
                   chts_weekday_flex_per_daytime['P_neg_sum_tou'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
    axs[2, 1].plot(tick_range,
                   mp_weekday_flex_per_daytime['P_neg_sum_tou'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid')
    axs[2, 1].grid()
    # ToU on weekends
    axs[3, 1].fill_between(tick_range,
                           mp_weekend_flex_per_daytime['P_pos_sum_tou'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                           mp_weekend_flex_per_daytime['P_neg_sum_tou'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                           alpha=0.5, label='GER MP', zorder=5, linestyle='solid', facecolor=mp_color)
    axs[3, 1].fill_between(tick_range,
                           chts_weekend_flex_per_daytime['P_pos_sum_tou'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                           chts_weekend_flex_per_daytime['P_neg_sum_tou'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                           alpha=0.5, label='US CHTS', zorder=5, linestyle='solid', facecolor=chts_color)
    axs[3, 1].plot(tick_range,
                   chts_weekend_flex_per_daytime['P_pos_sum_tou'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
    axs[3, 1].plot(tick_range,
                   mp_weekend_flex_per_daytime['P_pos_sum_tou'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid')
    axs[3, 1].plot(tick_range,
                   chts_weekend_flex_per_daytime['P_neg_sum_tou'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
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
                           alpha=0.5, label='US CHTS', zorder=5, linestyle='solid', facecolor=chts_color)
    axs[2, 3].plot(tick_range,
                   chts_weekday_flex_per_daytime['P_pos_sum_tou_mi'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
    axs[2, 3].plot(tick_range,
                   mp_weekday_flex_per_daytime['P_pos_sum_tou_mi'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid')
    axs[2, 3].plot(tick_range,
                   chts_weekday_flex_per_daytime['P_neg_sum_tou_mi'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
    axs[2, 3].plot(tick_range,
                   mp_weekday_flex_per_daytime['P_neg_sum_tou_mi'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid')
    axs[2, 3].grid()
    # Con + MI on weekdays
    axs[2, 2].fill_between(tick_range,
                           mp_weekday_flex_per_daytime['P_pos_sum_con_mi'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                           mp_weekday_flex_per_daytime['P_neg_sum_con_mi'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                           alpha=0.5, label='GER MP', zorder=5, linestyle='solid', facecolor=mp_color)
    axs[2, 2].fill_between(tick_range,
                           chts_weekday_flex_per_daytime['P_pos_sum_con_mi'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                           chts_weekday_flex_per_daytime['P_neg_sum_con_mi'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                           alpha=0.5, label='US CHTS', zorder=5, linestyle='solid', facecolor=chts_color)
    axs[2, 2].plot(tick_range,
                   chts_weekday_flex_per_daytime['P_pos_sum_con_mi'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
    axs[2, 2].plot(tick_range,
                   mp_weekday_flex_per_daytime['P_pos_sum_con_mi'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid')
    axs[2, 2].plot(tick_range,
                   chts_weekday_flex_per_daytime['P_neg_sum_con_mi'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
    axs[2, 2].plot(tick_range,
                   mp_weekday_flex_per_daytime['P_neg_sum_con_mi'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid')
    axs[2, 2].grid()
    axs[2, 2].legend(loc='lower center')
    # Con + MI on weekends
    axs[3, 2].fill_between(tick_range,
                           mp_weekend_flex_per_daytime['P_pos_sum_con_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                           mp_weekend_flex_per_daytime['P_neg_sum_con_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                           alpha=0.5, label='GER MP Con+MI', zorder=5, linestyle='solid', facecolor=mp_color)
    axs[3, 2].fill_between(tick_range,
                           chts_weekend_flex_per_daytime['P_pos_sum_con_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                           chts_weekend_flex_per_daytime['P_neg_sum_con_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                           alpha=0.5, label='US CHTS Con+MI', zorder=5, linestyle='solid', facecolor=chts_color)
    axs[3, 2].plot(tick_range,
                   chts_weekend_flex_per_daytime['P_pos_sum_con_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
    axs[3, 2].plot(tick_range,
                   mp_weekend_flex_per_daytime['P_pos_sum_con_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid')
    axs[3, 2].plot(tick_range,
                   chts_weekend_flex_per_daytime['P_neg_sum_con_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
    axs[3, 2].plot(tick_range,
                   mp_weekend_flex_per_daytime['P_neg_sum_con_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid')
    axs[3, 2].grid()
    # ToU + MI on weekends
    axs[3, 3].fill_between(tick_range,
                           mp_weekend_flex_per_daytime['P_pos_sum_tou_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                           mp_weekend_flex_per_daytime['P_neg_sum_tou_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                           alpha=0.5, label='GER MP ToU+MI', zorder=5, linestyle='solid', facecolor=mp_color)
    axs[3, 3].fill_between(tick_range,
                           chts_weekend_flex_per_daytime['P_pos_sum_tou_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                           chts_weekend_flex_per_daytime['P_neg_sum_tou_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                           alpha=0.5, label='US CHTS ToU+MI', zorder=5, linestyle='solid', facecolor=chts_color)
    axs[3, 3].plot(tick_range,
                   chts_weekend_flex_per_daytime['P_pos_sum_tou_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
    axs[3, 3].plot(tick_range,
                   mp_weekend_flex_per_daytime['P_pos_sum_tou_mi'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid')
    axs[3, 3].plot(tick_range,
                   chts_weekend_flex_per_daytime['P_neg_sum_tou_mi'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
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
                           alpha=0.5, label='US CHTS RTP', zorder=5, linestyle='solid', facecolor=chts_color)
    axs[2, 4].plot(tick_range,
                   chts_weekday_flex_per_daytime['P_pos_sum_rtp'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
    axs[2, 4].plot(tick_range,
                   mp_weekday_flex_per_daytime['P_pos_sum_rtp'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid')
    axs[2, 4].plot(tick_range,
                   chts_weekday_flex_per_daytime['P_neg_sum_rtp'] / chts_weekday_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
    axs[2, 4].plot(tick_range,
                   mp_weekday_flex_per_daytime['P_neg_sum_rtp'] / mp_weekday_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid')
    axs[2, 4].grid()
    axs[2, 4].set_ylim([-10, 7])
    # RTP on weekends
    axs[3, 4].fill_between(tick_range,
                           mp_weekend_flex_per_daytime['P_pos_sum_rtp'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                           mp_weekend_flex_per_daytime['P_neg_sum_rtp'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                           alpha=0.5, label='GER MP RTP', zorder=5, linestyle='solid', facecolor=mp_color)
    axs[3, 4].fill_between(tick_range,
                           chts_weekend_flex_per_daytime['P_pos_sum_rtp'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                           chts_weekend_flex_per_daytime['P_neg_sum_rtp'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                           alpha=0.5, label='US CHTS RTP', zorder=5, linestyle='solid', facecolor=chts_color)
    axs[3, 4].plot(tick_range,
                   chts_weekend_flex_per_daytime['P_pos_sum_rtp'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
    axs[3, 4].plot(tick_range,
                   mp_weekend_flex_per_daytime['P_pos_sum_rtp'] / mp_weekend_opt_per_daytime['n_veh_avail'],
                   color=mp_color, linestyle='solid')
    axs[3, 4].plot(tick_range,
                   chts_weekend_flex_per_daytime['P_neg_sum_rtp'] / chts_weekend_opt_per_daytime['n_veh_avail'],
                   color=chts_color, linestyle='solid')
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
    if save_figure:
        plt.savefig(figure_path + str(power) + '_opt_flex_average_day_plots.png', dpi=600)
'''


def plot_flex_prices(power, output_path, save_figure=True, figure_path='figures/'):
    """
    This function plots the flexibility prices of a study over time

    :param save_figure: boolean whether to save figure or not
    :param output_path: path to results of the  case study
    :param figure_path: folder where figures are stored
    :param power: current power level
    :return:
    """

    # Set font/figure style
    rcParams["font.family"] = "Times New Roman"
    rcParams["font.size"] = 10
    rcParams["figure.figsize"] = [11.69, 8.27]
    plot_color = 'tab:blue'

    # Read aggregated data from hdf files #########################################
    weekday_flex_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/weekday_flex_per_daytime_data.h5', key='df')
    weekend_opt_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/weekend_opt_per_daytime_data.h5', key='df')
    weekend_flex_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/weekend_flex_per_daytime_data.h5', key='df')
    weekday_opt_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/weekday_opt_per_daytime_data.h5', key='df')
    day_flex_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/day_flex_per_daytime_data.h5', key='df')
    day_opt_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/day_opt_per_daytime_data.h5', key='df')

    flex_sum_df = pd.read_hdf(output_path + 'Aggregated Data/flex_sum_data.h5', key='df')
    opt_sum_df = pd.read_hdf(output_path + 'Aggregated Data/opt_sum_data.h5', key='df')

    # Plot preparations
    tick_range = np.linspace(start=0, stop=96, num=96)
    # Figure settings
    rcParams["font.family"] = "Times New Roman"
    rcParams["mathtext.default"] = "regular"
    font_size = rcParams["font.size"] = 10
    rcParams["figure.figsize"] = [13, 9]

    # define number of subplots
    nrows = 3
    ncols = 5

    # lists for for loops
    range_cols = range(ncols)
    price_tariff_l = ['Con', 'Con + MI', 'ToU', 'ToU + MI', 'RTP']
    price_fcast_l = ['c_con_kwh', 'c_con_mi_kwh', 'c_tou_kwh', 'c_tou_mi_kwh', 'c_rtp_kwh']
    p_pos_sum_l = ['P_pos_sum_con', 'P_pos_sum_con_mi', 'P_pos_sum_tou', 'P_pos_sum_tou_mi', 'P_pos_sum_rtp']
    p_neg_sum_l = ['P_neg_sum_con', 'P_neg_sum_con_mi', 'P_neg_sum_tou', 'P_neg_sum_tou_mi', 'P_neg_sum_rtp']
    p_opt_sum_l = ['P_ev_opt_sum_con', 'P_ev_opt_sum_con_mi', 'P_ev_opt_sum_tou', 'P_ev_opt_sum_tou_mi', 'P_ev_opt_sum_rtp']
    opt_per_daytime_l = [weekday_opt_per_daytime, weekend_opt_per_daytime, day_opt_per_daytime]
    flex_per_daytime_l = [weekday_flex_per_daytime, weekend_flex_per_daytime, day_flex_per_daytime]
    forecast_lists = [range_cols, price_fcast_l, price_tariff_l]
    flex_opt_p_list = [range_cols, p_pos_sum_l, p_neg_sum_l, p_opt_sum_l]

    # create figure with nrows * ncols subplots
    fig1, axs = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, sharey='row')

    # Price Forecast avg day - has to be moved to separate figure
    # Con
    # for i, pricefcast, tariff in zip(*forecast_lists):
    #     axs[0, i].plot(tick_range, day_opt_per_daytime[pricefcast], color=plot_color, linestyle='solid')
    #     axs[0, i].grid()
    #     axs[0, i].set_title(tariff, fontsize=font_size)
    # axs[2, 0].set_ylim([0, .5])

    # Price Forecast Weekend - has to be moved to separate figure
    # Con
    # for i, pricefcast, tariff in zip(*forecast_lists):
    #     axs[0, i].plot(tick_range, weekend_opt_per_daytime[pricefcast], color=plot_color, linestyle='solid')
    #     axs[0, i].grid()
    #     axs[0, i].set_title(tariff, fontsize=font_size)
    # axs[0, i].set_ylim([0, .5])

    # # Price Forecast Weekday
    # Con
    for i, pricefcast, tariff in zip(*forecast_lists):
        axs[0, i].plot(tick_range, weekday_opt_per_daytime[pricefcast], color=plot_color, linestyle='solid')
        axs[0, i].grid()
        axs[0, i].set_title(tariff, fontsize=font_size)
        axs[0, 0].set_ylim([0, .5])

    # Flexibility (area plot) + Optimal power (red line on top)
    # on avg day
    for i, p_pos_sum, p_neg_sum, p_opt_sum in zip(*flex_opt_p_list):
        axs[1, i].fill_between(tick_range,
                               day_flex_per_daytime[p_pos_sum] / day_opt_per_daytime['n_veh_avail'],
                               day_flex_per_daytime[p_neg_sum] / day_opt_per_daytime['n_veh_avail'],
                               alpha=0.5, zorder=5, linestyle='solid', facecolor=plot_color)
        axs[1, i].plot(tick_range,
                       day_flex_per_daytime[p_pos_sum] / day_opt_per_daytime['n_veh_avail'],
                       color=plot_color, linestyle='solid')
        axs[1, i].plot(tick_range,
                       day_flex_per_daytime[p_neg_sum] / day_opt_per_daytime['n_veh_avail'],
                       color=plot_color, linestyle='solid')
        axs[1, i].plot(tick_range,
                       day_opt_per_daytime[p_opt_sum] / day_opt_per_daytime['n_veh_avail'],
                       color='r', alpha=0.5, zorder=10, linestyle='solid')
        axs[1, i].grid()
        axs[1, 0].set_ylim([-7.5, 7.5])

    # # on weekday
    # for i, p_pos_sum, p_neg_sum, p_opt_sum in zip(*flex_opt_p_list):
    #     axs[1, i].fill_between(tick_range,
    #                            weekday_flex_per_daytime[p_pos_sum] / weekday_opt_per_daytime['n_veh_avail'],
    #                            weekday_flex_per_daytime[p_neg_sum] / weekday_opt_per_daytime['n_veh_avail'],
    #                            alpha=0.5, zorder=5, linestyle='solid', facecolor=plot_color)
    #     axs[1, i].plot(tick_range,
    #                    weekday_flex_per_daytime[p_pos_sum] / weekday_opt_per_daytime['n_veh_avail'],
    #                    color=plot_color, linestyle='solid')
    #     axs[1, i].plot(tick_range,
    #                    weekday_flex_per_daytime[p_neg_sum] / weekday_opt_per_daytime['n_veh_avail'],
    #                    color=plot_color, linestyle='solid')
    #     axs[1, i].plot(tick_range,
    #                    weekday_opt_per_daytime[p_opt_sum] / weekday_opt_per_daytime['n_veh_avail'],
    #                    color='r', alpha=0.5, zorder=10, linestyle='solid')
    #     axs[1, i].grid()
    #     axs[1, 0].set_ylim([-10, 7])
    #
    # # on weekend
    # for i, p_pos_sum, p_neg_sum, p_opt_sum in zip(*flex_opt_p_list):
    #     axs[1, i].fill_between(tick_range,
    #                            weekend_flex_per_daytime[p_pos_sum] / weekend_opt_per_daytime['n_veh_avail'],
    #                            weekend_flex_per_daytime[p_neg_sum] / weekend_opt_per_daytime['n_veh_avail'],
    #                            alpha=0.5, zorder=5, linestyle='solid', facecolor=plot_color)
    #     axs[1, i].plot(tick_range,
    #                    weekend_flex_per_daytime[p_pos_sum] / weekend_opt_per_daytime['n_veh_avail'],
    #                    color=plot_color, linestyle='solid')
    #     axs[1, i].plot(tick_range,
    #                    weekend_flex_per_daytime[p_neg_sum] / weekend_opt_per_daytime['n_veh_avail'],
    #                    color=plot_color, linestyle='solid')
    #     axs[1, i].plot(tick_range,
    #                    weekend_opt_per_daytime[p_opt_sum] / weekend_opt_per_daytime['n_veh_avail'],
    #                    color='r', alpha=0.5, zorder=10, linestyle='solid')
    #     axs[1, i].grid()
    #     axs[1, 0].set_ylim([-10, 7])

    # Flexibility Prices and weighted average price
    # Con on weekdays
    # ToU on weekdays
    # Con + MI on weekdays
    # ToU + MI on weekdays
    # RTP on weekdays - muss noch angepasst werden!
    for i in zip(*):
        axs[2, i].fill_between(tick_range,
                               weekend_flex_per_daytime['P_pos_sum_rtp'] / weekend_opt_per_daytime['n_veh_avail'],
                               weekend_flex_per_daytime['P_neg_sum_rtp'] / weekend_opt_per_daytime['n_veh_avail'],
                               alpha=0.5, label='RTP', zorder=5, linestyle='solid', facecolor='r')
        axs[2, i].plot(tick_range,
                       weekend_flex_per_daytime['P_pos_sum_rtp'] / weekend_opt_per_daytime['n_veh_avail'],
                       color='r', linestyle='solid')
        axs[2, i].plot(tick_range,
                       weekend_flex_per_daytime['P_neg_sum_rtp'] / weekend_opt_per_daytime['n_veh_avail'],
                       color='r', linestyle='solid')
        axs[2, i].fill_between(tick_range,
                               weekend_flex_per_daytime['P_pos_sum_rtp'] / weekend_opt_per_daytime['n_veh_avail'],
                               weekend_flex_per_daytime['P_neg_sum_rtp'] / weekend_opt_per_daytime['n_veh_avail'],
                               alpha=0.5, label='RTP', zorder=5, linestyle='solid', facecolor=plot_color)
        axs[2, i].plot(tick_range,
                       weekend_flex_per_daytime['P_pos_sum_rtp'] / weekend_opt_per_daytime['n_veh_avail'],
                       color=plot_color, linestyle='solid')
        axs[2, i].plot(tick_range,
                       weekend_flex_per_daytime['P_neg_sum_rtp'] / weekend_opt_per_daytime['n_veh_avail'],
                       color=plot_color, linestyle='solid')
        axs[2, i].grid()
        axs[2, i].set_ylim([-10, 7])

    # Set labels
    axs[0, 0].set_ylabel('Price forecast $(€ \cdot kWh^{-1})$')
    axs[1, 0].set_ylabel('Flexible power per available vehicle $(kW \cdot EV^{-1})$ \n '
                         'Optimal scheduled power $(kW) \cdot EV^{-1})$')
    axs[2, 0].set_ylabel('Flexibility price per available vehicle $(€ \cdot (EV \cdot kW^{-1})$')
    n_ticks = 5
    ticks = [int(x) for x in np.linspace(start=0, stop=96, num=n_ticks)]
    tick_labels = pd.date_range(start='2020-01-01 00:00', end='2020-01-02 00:00', freq='15Min').strftime(
        '%H:%M').to_list()
    resulting_labels = [tick_labels[i] for i in ticks]
    axs[0, 0].set_xlim([0, 97])
    axs[0, 0].set_xticks(ticks)

    for i in range(ncols):
        axs[nrows-1, i].set_xticklabels(resulting_labels, rotation=45)
    plt.subplots_adjust(left=0.08, bottom=0.05, right=0.98, top=0.95, wspace=0.25, hspace=0.2)

    if save_figure:
        plt.savefig(figure_path + str(power) + 'test_flex_prices_plots.png', dpi=600)

    plt.show()


if __name__ == '__main__':
    # plot_n_avail_veh(output_path='../output/3.7/', figure_path='../figures/')
    plot_flex_prices(power='3.7', output_path='../output/3.7/', figure_path='../figures/')