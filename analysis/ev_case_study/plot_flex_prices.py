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


def plot_flex_prices(power, output_path, save_figure=True, figure_path='figures/', ylims={}):
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
    rcParams["figure.figsize"] = [13, 11]
    plot_color = 'tab:blue'

    # Read aggregated all seasons data from hdf files #########################################
    flex_per_daytime = pd.read_hdf(output_path + '/Aggregated Data/flex_per_daytime_data.h5', key='df')

    weekday_flex_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/allseasons_weekday_flex_per_daytime_data.h5', key='df')
    weekend_opt_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/allseasons_weekend_opt_per_daytime_data.h5', key='df')
    weekend_flex_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/allseasons_weekend_flex_per_daytime_data.h5', key='df')
    weekday_opt_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/allseasons_weekday_opt_per_daytime_data.h5', key='df')
    day_flex_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/allseasons_day_flex_per_daytime_data.h5', key='df')
    day_opt_per_daytime = pd.read_hdf(output_path + 'Aggregated Data/allseasons_day_opt_per_daytime_data.h5', key='df')

    # Check whether winter/summer files exist (if one exists, all exist) and read data from hdf files
    # seasons = ['winter', 'summer']
    # for season in seasons: # found no solution for not being able to name variables in loop (variable variables)
    winter_path = Path(output_path + 'Aggregated Data/winter_day_flex_per_daytime_data.h5')
    summer_path = Path(output_path + 'Aggregated Data/summer_day_flex_per_daytime_data.h5')
    opt_dfs = []
    flex_dfs = []
    seasons_list = []
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
        # wi_seasons_list = ['winter']
        wi_agg_type_l = ['winter_day', 'winter_weekday', 'winter_weekend']
        wi_title_l = ['Day in Winter', 'Weekday in Winter', 'Weekend Day in Winter']

    else:
        wi_opt_dfs = []
        wi_flex_dfs = []
        wi_price_dfs = []
        # wi_seasons_list = []
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
        # su_seasons_list = ['summer']
        su_agg_type_l = ['summer_day', 'summer_weekday', 'summer_weekend']
        su_title_l = ['Day in Summer', 'Weekday in Summer', 'Weekend Day in Summer']
    else:
        su_opt_dfs = []
        su_flex_dfs = []
        su_price_dfs = []
        # su_seasons_list = []
        su_agg_type_l = []
        su_title_l = []

    flex_sum_df = pd.read_hdf(output_path + 'Aggregated Data/flex_sum_data.h5', key='df')
    opt_sum_df = pd.read_hdf(output_path + 'Aggregated Data/opt_sum_data.h5', key='df')

    # Plot preparations
    tick_range = np.linspace(start=0, stop=96, num=96)
    # Figure settings
    rcParams["font.family"] = "Times New Roman"
    rcParams["mathtext.default"] = "regular"
    font_size = rcParams["font.size"] = 10
    rcParams["figure.figsize"] = [13, 11]

    # define number of subplots
    nrows = 3
    ncols = 5
    # lists for outer for loop (day, weekday, weekend) - without summer/winter
    # flex_dfs = [day_flex_per_daytime, weekday_flex_per_daytime, weekend_flex_per_daytime]
    # opt_dfs = [day_opt_per_daytime, weekday_opt_per_daytime, weekend_opt_per_daytime]
    # agg_type_l = ['day', 'weekday', 'weekend']
    # title_l = ['Day', 'Weekday', 'Weekend Day']

    # lists for outer for loop (day, weekday, weekend for summer & winter each, depending on whether su and/or wi exist)
    opt_dfs = wi_opt_dfs + su_opt_dfs
    flex_dfs = wi_flex_dfs + su_flex_dfs
    price_dfs = wi_price_dfs + su_price_dfs
    # seasons_list = wi_seasons_list + su_seasons_list
    agg_type_l = wi_agg_type_l + su_agg_type_l
    title_l = wi_title_l + su_title_l

    # lists for inner for loop (subplots, what column of df is called)
    range_cols = range(ncols)
    price_tariff_l = ['Con', 'Con + MI', 'ToU', 'ToU + MI', 'RTP']
    price_fcast_l = ['c_con_kwh', 'c_con_mi_kwh', 'c_tou_kwh', 'c_tou_mi_kwh', 'c_rtp_kwh']
    fc_plot_dict = {0: {'price_tariff': 'Con', 'fc_kwh': 'c_con_kwh'},
                    1: {'price_tariff': 'Con + MI', 'fc_kwh': 'c_con_mi_kwh'},
                    2: {'price_tariff': 'ToU', 'fc_kwh': 'c_tou_kwh'},
                    3: {'price_tariff': 'ToU + MI', 'fc_kwh': 'c_tou_mi_kwh'},
                    4: {'price_tariff': 'RTP', 'fc_kwh': 'c_rtp_kwh'}}
    p_pos_sum_l = ['P_pos_sum_con', 'P_pos_sum_con_mi', 'P_pos_sum_tou', 'P_pos_sum_tou_mi', 'P_pos_sum_rtp']
    p_neg_sum_l = ['P_neg_sum_con', 'P_neg_sum_con_mi', 'P_neg_sum_tou', 'P_neg_sum_tou_mi', 'P_neg_sum_rtp']
    p_opt_sum_l = ['P_ev_opt_sum_con', 'P_ev_opt_sum_con_mi', 'P_ev_opt_sum_tou', 'P_ev_opt_sum_tou_mi',
                   'P_ev_opt_sum_rtp']
    max_pr_pos_l = ['max_c_flex_pos_con', 'max_c_flex_pos_con_mi', 'max_c_flex_pos_tou', 'max_c_flex_pos_tou_mi',
                    'max_c_flex_pos_rtp']
    max_pr_neg_l = ['max_c_flex_neg_con', 'max_c_flex_neg_con_mi', 'max_c_flex_neg_tou', 'max_c_flex_neg_tou_mi',
                    'max_c_flex_neg_rtp']
    min_pr_pos_l = ['min_c_flex_pos_con', 'min_c_flex_pos_con_mi', 'min_c_flex_pos_tou', 'min_c_flex_pos_tou_mi',
                    'min_c_flex_pos_rtp']
    min_pr_neg_l = ['min_c_flex_neg_con', 'min_c_flex_neg_con_mi', 'min_c_flex_neg_tou', 'min_c_flex_neg_tou_mi',
                    'min_c_flex_neg_rtp']
    forecast_lists = [range_cols, price_fcast_l, price_tariff_l]
    power_lists = [range_cols, p_pos_sum_l, p_neg_sum_l, p_opt_sum_l]
    flex_price_lists = [range_cols, max_pr_pos_l,  min_pr_pos_l, max_pr_neg_l, min_pr_neg_l]

    # for loop without summer/winter
    # for flex_per_daytime_df, opt_per_daytime_df, plottype, title in zip(flex_dfs, opt_dfs, plottype_l, title_l):
    for flex_per_daytime_df, opt_per_daytime_df, price_df, agg_type, title in zip(flex_dfs, opt_dfs, price_dfs, agg_type_l, title_l):

        # create figure with nrows * ncols subplots
        fig1, axs = plt.subplots(nrows=nrows, ncols=ncols, sharex=True, sharey='row')
        fig1.suptitle('Price Forecast, Flexible and Scheduled Power and Flexibility Prices for an Average ' +
                      str(title) + ' at ' + str(power) + ' kW', fontsize=16, y=0.98)

        # Price Forecast Subplots
        # for i, pricefcast, tariff in zip(*forecast_lists):
        for i, value in fc_plot_dict.items():
            axs[0, i].plot(tick_range, opt_per_daytime_df[value['fc_kwh']], color=plot_color, linestyle='solid')
            axs[0, i].grid()
            axs[0, i].set_title(value['price_tariff'], fontsize=font_size)
            axs[0, 0].set_ylim([0, .5])

        # Flexibility (area plot) + Optimal power (red line on top) subplots
        for i, p_pos_sum, p_neg_sum, p_opt_sum in zip(*power_lists):
            axs[1, i].fill_between(tick_range,
                                   flex_per_daytime_df[p_pos_sum] / opt_per_daytime_df['n_veh_avail'],
                                   flex_per_daytime_df[p_neg_sum] / opt_per_daytime_df['n_veh_avail'],
                                   alpha=0.5, zorder=5, linestyle='solid', facecolor=plot_color)
            axs[1, i].plot(tick_range,
                           flex_per_daytime_df[p_pos_sum] / opt_per_daytime_df['n_veh_avail'],
                           color=plot_color, linestyle='solid')
            axs[1, i].plot(tick_range,
                           flex_per_daytime_df[p_neg_sum] / opt_per_daytime_df['n_veh_avail'],
                           color=plot_color, linestyle='solid')
            axs[1, i].plot(tick_range,
                           opt_per_daytime_df[p_opt_sum] / opt_per_daytime_df['n_veh_avail'],
                           color='r', alpha=0.5, zorder=10, linestyle='solid')
            axs[1, i].grid()
            # if ylim_power != None:
            # axs[1, 0].set_ylim(ylim_power)

        # Flexibility Prices and weighted average price subplots
        # for i, max_pr_pos, min_pr_pos, max_pr_neg, min_pr_neg in zip(*flex_price_lists):
        #     # tick_range2 = np.linspace(0, 15, 46)
        #     # [0:96]
        #     axs[2, i].fill_between(tick_range,
        #                            flex_per_daytime[max_pr_pos].iloc[0:96], flex_per_daytime[min_pr_pos].iloc[0:96],
        #                            alpha=0.5, zorder=5, linestyle='solid', facecolor='g')
        #     axs[2, i].plot(tick_range,
        #                    flex_per_daytime[max_pr_pos].iloc[0:96], color='g', linestyle='solid')
        #     axs[2, i].plot(tick_range,
        #                    flex_per_daytime[min_pr_pos].iloc[0:96], color='g', linestyle='solid')
        #     axs[2, i].fill_between(tick_range,
        #                            flex_per_daytime[max_pr_neg].iloc[0:96], flex_per_daytime[min_pr_neg].iloc[0:96],
        #                            alpha=0.5, zorder=5, linestyle='solid', facecolor=plot_color)
        #     axs[2, i].plot(tick_range,
        #                    flex_per_daytime[max_pr_neg].iloc[0:96], color='r', linestyle='solid')
        #     axs[2, i].plot(tick_range,
        #                    flex_per_daytime[min_pr_neg].iloc[0:96], color='r', linestyle='solid')
        #     axs[2, i].grid()
        #     axs[2, 0].set_ylim([-1, 1])

        # # Flexibility Prices and weighted average price subplots
        for i, max_pr_pos, min_pr_pos, max_pr_neg, min_pr_neg in zip(*flex_price_lists):
            axs[2, i].fill_between(tick_range,
                                   price_df[max_pr_pos], price_df[min_pr_pos],
                                   alpha=0.5, label='RTP', zorder=5, linestyle='solid', facecolor='g')
            axs[2, i].plot(tick_range,
                           price_df[max_pr_pos], color='g', linestyle='solid')
            axs[2, i].plot(tick_range,
                           price_df[min_pr_pos], color='g', linestyle='solid')
            axs[2, i].fill_between(tick_range,
                                   price_df[max_pr_neg], price_df[min_pr_neg],
                                   alpha=0.5, label='RTP', zorder=5, linestyle='solid', facecolor=plot_color)
            axs[2, i].plot(tick_range,
                           price_df[max_pr_neg], color=plot_color, linestyle='solid')
            axs[2, i].plot(tick_range,
                           price_df[min_pr_neg], color=plot_color, linestyle='solid')
            axs[2, i].grid()
            axs[2, 0].set_ylim([-0.55, 0.55])

        # Set labels
        axs[0, 0].set_ylabel('Price Forecast $(€ \cdot kWh^{-1})$')
        axs[1, 0].set_ylabel('Flexible Power per Available \n '
                             'Vehicle $(kW \cdot EV^{-1})$ (area) \n '
                             'Optimal Scheduled Power $(kW \cdot EV^{-1})$ (line)')
        axs[2, 0].set_ylabel('Price Ranges for Positive and Negative Flexibility $(€ \cdot kW^{-1})$ \n '
                             'Weighted Average (by Offered Flex Power) of \n '
                             'Flexibility Price $(€ \cdot kW^{-1})$')
        n_ticks = 5
        ticks = [int(x) for x in np.linspace(start=0, stop=96, num=n_ticks)]
        tick_labels = pd.date_range(start='2020-01-01 00:00', end='2020-01-02 00:00', freq='15Min').strftime(
            '%H:%M').to_list()
        resulting_labels = [tick_labels[i] for i in ticks]
        axs[0, 0].set_xlim([0, 97])
        axs[0, 0].set_xticks(ticks)

        for i in range(ncols):
            axs[nrows - 1, i].set_xticklabels(resulting_labels, rotation=45)

        plt.subplots_adjust(left=0.09, bottom=0.05, right=0.98, top=0.92, wspace=0.25, hspace=0.2)

        if save_figure:
            plt.savefig(figure_path + str(power) + '_' + agg_type + '_flex_prices_plots333.png', dpi=600)

        plt.show()


if __name__ == '__main__':
    # plot_n_avail_veh(output_path='../output/3.7/', figure_path='../figures/')
    plot_flex_prices(power='3.7', output_path='../output/3.7/', figure_path='../figures/')
