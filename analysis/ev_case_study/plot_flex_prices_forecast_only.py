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

    # Plot only weekdays and weekends
    tick_range = np.linspace(start=0, stop=96, num=96)
    # Figure settings
    rcParams["font.family"] = "Times New Roman"
    rcParams["mathtext.default"] = "regular"
    font_size = rcParams["font.size"] = 10
    rcParams["figure.figsize"] = [13, 9]
    #
    nrows = 3
    ncols = 5
    fig1, axs = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, sharey='row')

    # # Price Forecast Weekday
    # Con
    axs[0, 0].plot(tick_range, weekday_opt_per_daytime['c_con_kwh'], color=plot_color, linestyle='solid')
    axs[0, 0].grid()
    axs[0, 0].set_ylim([0, .5])
    axs[0, 0].set_title('Con', fontsize=font_size)

    # ToU
    axs[0, 1].plot(tick_range, weekday_opt_per_daytime['c_tou_kwh'], color=plot_color, linestyle='solid')
    axs[0, 1].grid()
    axs[0, 1].set_title('ToU', fontsize=font_size)

    # Con + MI
    axs[0, 2].plot(tick_range, weekday_opt_per_daytime['c_con_mi_kwh'], color=plot_color, linestyle='solid')
    axs[0, 2].grid()
    axs[0, 2].set_title('Con + MI', fontsize=font_size)

    # ToU + MI
    axs[0, 3].plot(tick_range, weekday_opt_per_daytime['c_tou_mi_kwh'], color=plot_color, linestyle='solid')
    axs[0, 3].grid()
    axs[0, 3].set_title('ToU + MI', fontsize=font_size)

    # RTP
    axs[0, 4].plot(tick_range, weekday_opt_per_daytime['c_rtp_kwh'], color=plot_color, linestyle='solid')
    axs[0, 4].grid()
    axs[0, 4].set_title('RTP', fontsize=font_size)

    # Price Forecast general
    # Con
    axs[2, 0].plot(tick_range, day_opt_per_daytime['c_con_kwh'], color=plot_color, linestyle='solid')
    axs[2, 0].grid()
    axs[2, 0].set_ylim([0, .5])
    axs[2, 0].set_title('Con', fontsize=font_size)

    # ToU
    axs[2, 1].plot(tick_range, day_opt_per_daytime['c_tou_kwh'], color=plot_color, linestyle='solid')
    axs[2, 1].grid()
    axs[2, 1].set_title('ToU', fontsize=font_size)

    # Con + MI
    axs[2, 2].plot(tick_range, day_opt_per_daytime['c_con_mi_kwh'], color=plot_color, linestyle='solid')
    axs[2, 2].grid()
    axs[2, 2].set_title('Con + MI', fontsize=font_size)

    # ToU + MI
    axs[2, 3].plot(tick_range, day_opt_per_daytime['c_tou_mi_kwh'], color=plot_color, linestyle='solid')
    axs[2, 3].grid()
    axs[2, 3].set_title('ToU + MI', fontsize=font_size)

    # RTP
    axs[2, 4].plot(tick_range, day_opt_per_daytime['c_rtp_kwh'], color=plot_color, linestyle='solid')
    axs[2, 4].grid()
    axs[2, 4].set_title('RTP', fontsize=font_size)

    # Price Forecast Weekend
    # Con
    axs[1, 0].plot(tick_range, weekend_opt_per_daytime['c_con_kwh'], color=plot_color, linestyle='solid')
    axs[1, 0].grid()
    axs[1, 0].set_ylim([0, .5])
    axs[1, 0].set_title('Con', fontsize=font_size)

    # ToU
    axs[1, 1].plot(tick_range, weekend_opt_per_daytime['c_tou_kwh'], color=plot_color, linestyle='solid')
    axs[1, 1].grid()
    axs[1, 1].set_title('ToU', fontsize=font_size)

    # Con + MI
    axs[1, 2].plot(tick_range, weekend_opt_per_daytime['c_con_mi_kwh'], color=plot_color, linestyle='solid')
    axs[1, 2].grid()
    axs[1, 2].set_title('Con + MI', fontsize=font_size)

    # ToU + MI
    axs[1, 3].plot(tick_range, weekend_opt_per_daytime['c_tou_mi_kwh'], color=plot_color, linestyle='solid')
    axs[1, 3].grid()
    axs[1, 3].set_title('ToU + MI', fontsize=font_size)

    # RTP
    axs[1, 4].plot(tick_range, weekend_opt_per_daytime['c_rtp_kwh'], color=plot_color, linestyle='solid')
    axs[1, 4].grid()
    axs[1, 4].set_title('RTP', fontsize=font_size)

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
    #axs[2, :].set_xticklabels(resulting_labels, rotation=45)
    plt.subplots_adjust(left=0.08, bottom=0.05, right=0.98, top=0.95, wspace=0.25, hspace=0.2)

    if save_figure:
        plt.savefig(figure_path + str(power) + '_flex_prices_plots_forecast.png', dpi=600)

    plt.show()


if __name__ == '__main__':
    # plot_n_avail_veh(output_path='../output/3.7/', figure_path='../figures/')
    plot_flex_prices(power = '3.7', output_path='../output/3.7/', figure_path='../figures/')

