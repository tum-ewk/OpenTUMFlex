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


def plot_flex_prices(power, output_path, save_figure=True, figure_path='figures/', ylims=None):
    """
    This function plots the flexibility prices of a study over time

    :param save_figure: boolean whether to save figure or not
    :param output_path: path to results of the  case study
    :param figure_path: folder where figures are stored
    :param power: current power level
    :param ylims: dictionary with max/min y-limit values for the plots, default None
    :return:
    """

    # Set font/figure style
    rcParams["font.family"] = "Times New Roman"
    rcParams["font.size"] = 10
    rcParams["figure.figsize"] = [25, 11]
    plot_color = 'tab:blue'

    # Read aggregated all seasons data from hdf files #########################################
    flex_per_daytime = pd.read_hdf(output_path + '/Aggregated Data/flex_per_daytime_data.h5', key='df')

    # allseason files
    day_flex_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/allseasons_day_flex_per_daytime_data.h5', key='df')
    weekday_flex_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/allseasons_weekday_flex_per_daytime_data.h5', key='df')
    weekend_opt_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/allseasons_weekend_opt_per_daytime_data.h5', key='df')
    day_opt_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/allseasons_day_opt_per_daytime_data.h5', key='df')
    weekday_opt_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/allseasons_weekday_opt_per_daytime_data.h5', key='df')
    weekend_flex_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/allseasons_weekend_flex_per_daytime_data.h5', key='df')
    day_flex_prices = pd.read_hdf(output_path + 'Aggregated Data/allseasons_day_flex_prices_data.h5', key='df')
    weekday_flex_prices = pd.read_hdf(output_path + 'Aggregated Data/allseasons_weekday_flex_prices_data.h5', key='df')
    weekend_flex_prices = pd.read_hdf(output_path + 'Aggregated Data/allseasons_weekend_flex_prices_data.h5', key='df')
    all_opt_dfs = [day_opt_per_daytime, weekday_opt_per_daytime, weekend_opt_per_daytime]
    all_flex_dfs = [day_flex_per_daytime, weekday_flex_per_daytime, weekend_flex_per_daytime]
    all_price_dfs = [day_flex_prices, weekday_flex_prices, weekend_flex_prices]
    all_agg_type_l = ['allseasons_day', 'allseasons_weekday', 'allseasons_weekend']
    all_title_l = ['Day', 'Weekday', 'Weekend']

    # Check whether winter/summer files exist (if one exists, all exist) and read data from hdf files
    # seasons = ['winter', 'summer']
    # for season in seasons: # found no solution for not being able to name variables in loop (variable variables)
    winter_path = Path(output_path + 'Aggregated Data/winter_day_flex_per_daytime_data.h5')
    summer_path = Path(output_path + 'Aggregated Data/summer_day_flex_per_daytime_data.h5')
    opt_dfs = []
    flex_dfs = []
    agg_type_l = []
    title_l = []
    if winter_path.is_file():
        wi_weekday_flex_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/winter_weekday_flex_per_daytime_data.h5', key='df')
        wi_weekend_opt_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/winter_weekend_opt_per_daytime_data.h5', key='df')
        wi_weekend_flex_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/winter_weekend_flex_per_daytime_data.h5', key='df')
        wi_weekday_opt_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/winter_weekday_opt_per_daytime_data.h5', key='df')
        wi_day_flex_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/winter_day_flex_per_daytime_data.h5', key='df')
        wi_day_opt_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/winter_day_opt_per_daytime_data.h5', key='df')
        wi_day_flex_prices = pd.read_hdf(output_path + 'Aggregated Data/winter_day_flex_prices_data.h5', key='df')
        wi_weekday_flex_prices = pd.read_hdf(output_path + 'Aggregated Data/winter_weekday_flex_prices_data.h5', key='df')
        wi_weekend_flex_prices = pd.read_hdf(output_path + 'Aggregated Data/winter_weekend_flex_prices_data.h5', key='df')

        wi_opt_dfs = [wi_day_opt_per_daytime, wi_weekday_opt_per_daytime, wi_weekend_opt_per_daytime]
        wi_flex_dfs = [wi_day_flex_per_daytime, wi_weekday_flex_per_daytime, wi_weekend_flex_per_daytime]
        wi_price_dfs = [wi_day_flex_prices, wi_weekday_flex_prices, wi_weekend_flex_prices]
        wi_agg_type_l = ['winter_day', 'winter_weekday', 'winter_weekend']
        wi_title_l = ['Day in Winter', 'Weekday in Winter', 'Weekend Day in Winter']

    else:
        wi_opt_dfs = []
        wi_flex_dfs = []
        wi_price_dfs = []
        wi_agg_type_l = []
        wi_title_l = []

    if summer_path.is_file():
        su_weekday_flex_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/summer_weekday_flex_per_daytime_data.h5', key='df')
        su_weekend_opt_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/summer_weekend_opt_per_daytime_data.h5', key='df')
        su_weekend_flex_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/summer_weekend_flex_per_daytime_data.h5', key='df')
        su_weekday_opt_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/summer_weekday_opt_per_daytime_data.h5', key='df')
        su_day_flex_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/summer_day_flex_per_daytime_data.h5', key='df')
        su_day_opt_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/summer_day_opt_per_daytime_data.h5', key='df')
        su_day_flex_prices = pd.read_hdf(output_path + 'Aggregated Data/summer_day_flex_prices_data.h5', key='df')
        su_weekday_flex_prices = pd.read_hdf(output_path + 'Aggregated Data/summer_weekday_flex_prices_data.h5', key='df')
        su_weekend_flex_prices = pd.read_hdf(output_path + 'Aggregated Data/summer_weekend_flex_prices_data.h5', key='df')

        su_opt_dfs = [su_day_opt_per_daytime, su_weekday_opt_per_daytime, su_weekend_opt_per_daytime]
        su_flex_dfs = [su_day_flex_per_daytime, su_weekday_flex_per_daytime, su_weekend_flex_per_daytime]
        su_price_dfs = [su_day_flex_prices, su_weekday_flex_prices, su_weekend_flex_prices]
        su_agg_type_l = ['summer_day', 'summer_weekday', 'summer_weekend']
        su_title_l = ['Day in Summer', 'Weekday in Summer', 'Weekend Day in Summer']
    else:
        su_opt_dfs = []
        su_flex_dfs = []
        su_price_dfs = []
        # su_seasons_list = []
        su_agg_type_l = []
        su_title_l = []

    # Plot preparations
    tick_range = np.linspace(start=0, stop=96, num=96)
    # Figure settings
    rcParams["font.family"] = "Times New Roman"
    rcParams["mathtext.default"] = "regular"
    font_size = rcParams["font.size"] = 10
    rcParams["figure.figsize"] = [15, 11]

    # define number of subplots
    nrows = 3
    ncols = 5
    # percentage from highest (max & min) y value that is added to it to get the y-lim when ylims is not None
    ylim_spacing = 0.1

    # lists for outer for loop (day, weekday, weekend for summer & winter each, depending on whether su and/or wi exist)
    opt_dfs = wi_opt_dfs + su_opt_dfs + all_opt_dfs
    flex_dfs = wi_flex_dfs + su_flex_dfs + all_flex_dfs
    price_dfs = wi_price_dfs + su_price_dfs + all_price_dfs
    agg_type_l = wi_agg_type_l + su_agg_type_l + all_agg_type_l
    title_l = wi_title_l + su_title_l + all_title_l

    # dicts for inner for loops (subplots, what column of dataframe is called)
    fc_plot_dict = {0: {'price_tariff': 'Con', 'fc_kwh': 'c_con_kwh'},
                    1: {'price_tariff': 'Con + MI', 'fc_kwh': 'c_con_mi_kwh'},
                    2: {'price_tariff': 'ToU', 'fc_kwh': 'c_tou_kwh'},
                    3: {'price_tariff': 'ToU + MI', 'fc_kwh': 'c_tou_mi_kwh'},
                    4: {'price_tariff': 'RTP', 'fc_kwh': 'c_rtp_kwh'}}
    pow_plot_dict = {0: {'p_pos_sum': 'P_pos_sum_con', 'p_neg_sum': 'P_neg_sum_con', 'p_opt_sum': 'P_ev_opt_sum_con'},
                     1: {'p_pos_sum': 'P_pos_sum_con_mi', 'p_neg_sum': 'P_neg_sum_con_mi', 'p_opt_sum': 'P_ev_opt_sum_con_mi'},
                     2: {'p_pos_sum': 'P_pos_sum_tou', 'p_neg_sum': 'P_neg_sum_tou', 'p_opt_sum': 'P_ev_opt_sum_tou'},
                     3: {'p_pos_sum': 'P_pos_sum_tou_mi', 'p_neg_sum': 'P_neg_sum_tou_mi', 'p_opt_sum': 'P_ev_opt_sum_tou_mi'},
                     4: {'p_pos_sum': 'P_pos_sum_rtp', 'p_neg_sum': 'P_neg_sum_rtp', 'p_opt_sum': 'P_ev_opt_sum_rtp'}}
    flex_prices_dict = {0: {'max_pr_pos': 'max_c_flex_pos_con', 'max_pr_neg': 'max_c_flex_neg_con',
                            'min_pr_pos': 'min_c_flex_pos_con', 'min_pr_neg': 'min_c_flex_neg_con'},
                        1: {'max_pr_pos': 'max_c_flex_pos_con_mi', 'max_pr_neg': 'max_c_flex_neg_con_mi',
                            'min_pr_pos': 'min_c_flex_pos_con_mi', 'min_pr_neg': 'min_c_flex_neg_con_mi'},
                        2: {'max_pr_pos': 'max_c_flex_pos_tou', 'max_pr_neg': 'max_c_flex_neg_tou',
                            'min_pr_pos': 'min_c_flex_pos_tou', 'min_pr_neg': 'min_c_flex_neg_tou'},
                        3: {'max_pr_pos': 'max_c_flex_pos_tou_mi', 'max_pr_neg': 'max_c_flex_neg_tou_mi',
                            'min_pr_pos': 'min_c_flex_pos_tou_mi', 'min_pr_neg': 'min_c_flex_neg_tou_mi'},
                        4: {'max_pr_pos': 'max_c_flex_pos_rtp', 'max_pr_neg': 'max_c_flex_neg_rtp',
                            'min_pr_pos': 'min_c_flex_pos_rtp', 'min_pr_neg': 'min_c_flex_neg_rtp'}}

    # for flex_per_daytime_df, opt_per_daytime_df, plottype, title in zip(flex_dfs, opt_dfs, plottype_l, title_l):
    for flex_per_daytime_df, opt_per_daytime_df, price_df, agg_type, title in zip(flex_dfs, opt_dfs, price_dfs, agg_type_l, title_l):

        # create figure with nrows * ncols subplots
        fig1, axs = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, sharey='row')
        fig1.suptitle('Price Forecast, Flexible and Scheduled Power and Flexibility Prices for an Average ' +
                      str(title) + ' at ' + str(power) + ' kW', fontsize=16, y=0.98)

        # Price Forecast Subplots
        # for i, pricefcast, tariff in zip(*forecast_lists):
        for i, value in fc_plot_dict.items():
            axs[0, i].plot(tick_range, opt_per_daytime_df[value['fc_kwh']], color=plot_color,
                           linestyle='solid', label='Forecast price\nmean')
            axs[0, i].grid()
            # set subplot columns title
            axs[0, i].set_title(value['price_tariff'], fontsize=font_size)
            # plot legend only for last subplot in row, to the right of the row
            if i == ncols - 1:
                axs[0, i].legend(bbox_to_anchor=(1.03, .6), loc='upper left', frameon=False)

        # Flexibility (area plot) + Optimal power (red line on top) subplots
        for i, value in pow_plot_dict.items():
            axs[1, i].fill_between(tick_range,
                                   flex_per_daytime_df[value['p_pos_sum']]/opt_per_daytime_df['n_veh_avail'],
                                   flex_per_daytime_df[value['p_neg_sum']]/opt_per_daytime_df['n_veh_avail'],
                                   alpha=0.5, zorder=5, linestyle='solid', facecolor=plot_color,
                                   label='Positive and negative\nflexible power')
            axs[1, i].plot(tick_range,
                           flex_per_daytime_df[value['p_pos_sum']]/opt_per_daytime_df['n_veh_avail'],
                           color=plot_color, linestyle='solid')
            axs[1, i].plot(tick_range,
                           flex_per_daytime_df[value['p_neg_sum']]/opt_per_daytime_df['n_veh_avail'],
                           color=plot_color, linestyle='solid')
            axs[1, i].plot(tick_range,
                           opt_per_daytime_df[value['p_opt_sum']]/opt_per_daytime_df['n_veh_avail'],
                           color='r', alpha=0.5, zorder=10, linestyle='solid', label='Optimal scheduled\npower')
            axs[1, i].grid()
            if i == ncols - 1:
                axs[1, i].legend(bbox_to_anchor=(1.03, .69), loc='upper left', frameon=False)

        # Flexibility Prices and weighted average price subplots
        for i, value in flex_prices_dict.items():
            axs[2, i].fill_between(tick_range,
                                   price_df[value['max_pr_pos']], price_df[value['min_pr_pos']],
                                   alpha=0.5, label='Price for\npositive flexibility', zorder=5, linestyle='solid',
                                   facecolor='g')
            axs[2, i].plot(tick_range,
                           price_df[value['max_pr_pos']], color='g', linestyle='solid')
            axs[2, i].plot(tick_range,
                           price_df[value['min_pr_pos']], color='g', linestyle='solid')
            axs[2, i].fill_between(tick_range,
                                   price_df[value['max_pr_neg']], price_df[value['min_pr_neg']],
                                   alpha=0.5, label='Price for\nnegative flexibility', zorder=5, linestyle='solid',
                                   facecolor=plot_color)
            axs[2, i].plot(tick_range,
                           price_df[value['max_pr_neg']], color=plot_color, linestyle='solid')
            axs[2, i].plot(tick_range,
                           price_df[value['min_pr_neg']], color=plot_color, linestyle='solid')
            axs[2, i].grid()
            if i == ncols - 1:
                axs[2, i].legend(bbox_to_anchor=(1.03, .72), loc='upper left', frameon=False)

        # Set labels
        axs[0, 0].set_ylabel('Price Forecast $(€ \cdot kWh^{-1})$')
        axs[1, 0].set_ylabel('Flexible Power per Available\n '
                             'Vehicle $(kW \cdot EV^{-1})$ (area)\n '
                             'Optimal Scheduled Power $(kW \cdot EV^{-1})$ (line)')
        axs[2, 0].set_ylabel('Price Ranges for Positive and Negative Flexibility $(€ \cdot kW^{-1})$\n '
                             'Weighted Average (by Offered Flex Power) of\n '
                             'Flexibility Price $(€ \cdot kW^{-1})$')
        n_ticks = 5
        ticks = [int(x) for x in np.linspace(start=0, stop=96, num=n_ticks)]
        tick_labels = pd.date_range(start='2020-01-01 00:00', end='2020-01-02 00:00', freq='15Min').strftime(
            '%H:%M').to_list()
        resulting_labels = [tick_labels[i] for i in ticks]
        if ylims is None:
            axs[0, 0].set_ylim([0, .5])
            axs[1, 0].set_ylim([-10, 17])
            axs[2, 0].set_ylim([-.55, .55])
        else:
            if ylims['forecast']['min'] >= 0:
                axs[0, 0].set_ylim([0, ylims['forecast']['max'] * (1 + ylim_spacing)])
            else:
                axs[0, 0].set_ylim([ylims['forecast']['min'] * (1 + ylim_spacing),
                                    ylims['forecast']['max'] * (1 + ylim_spacing)])
            axs[2, 0].set_ylim(ylims['flex price']['min'] * (1 + ylim_spacing),
                               ylims['flex price']['max'] * (1 + ylim_spacing))
            axs[1, 0].set_ylim(ylims['flex power']['min'] * (1 + ylim_spacing),
                               ylims['flex power']['max'] * (1 + ylim_spacing))
        axs[0, 0].set_xlim([0, 97])
        axs[0, 0].set_xticks(ticks)

        for i in range(ncols):
            axs[nrows - 1, i].set_xticklabels(resulting_labels, rotation=45)

        plt.subplots_adjust(left=0.09, bottom=0.05, right=0.87, top=0.92, wspace=0.25, hspace=0.2)

        if save_figure:
            plt.savefig(figure_path + str(power) + '_' + agg_type + '_flex_prices_plots.png', dpi=600)

        plt.show()


if __name__ == '__main__':
    # plot_n_avail_veh(output_path='../output/3.7/', figure_path='../figures/')
    # ylim_dict for testing
    ylim_dict = {'forecast': {'max': 0.36, 'min': 0.13},
                 'flex power': {'max': 12, 'min': -16},
                 'flex price': {'max': .6, 'min': -0.4}}
    # plot_flex_prices(power='3.7', output_path='../output/3.7/', figure_path='../figures/', ylims=None)
    # plot_flex_prices(power='11', output_path='../output/11/', figure_path='../figures/', ylims=None)
    # plot_flex_prices(power='22', output_path='../output/22/', figure_path='../figures/', ylims=None)
    plot_flex_prices(power='3.7', output_path='../output/3.7/', figure_path='../figures/', ylims=ylim_dict)
    plot_flex_prices(power='11', output_path='../output/11/', figure_path='../figures/', ylims=ylim_dict)
    plot_flex_prices(power='22', output_path='../output/22/', figure_path='../figures/', ylims=ylim_dict)
