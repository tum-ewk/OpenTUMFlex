"""
The ev_opt_flex_aggregation module aggregates all optimal and flexible profiles of ev into an average week/day/weekday.
"""

__author__ = "Michel Zadé"
__copyright__ = "2020 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "1.0"
__maintainer__ = "Michel Zadé"
__email__ = "michel.zade@tum.de"
__status__ = "Development"

from pathlib import Path
from tqdm import tqdm
import pandas as pd
import os
import numpy as np
import opentumflex
import forecast


def aggregate_ev_flex(veh_availabilities, output_path='../output/', rtp_input_data_path='../input/RTP/'):
    """
    This function aggregates the flexibility offers to data frame for weekdays and weekends in 15 minute resolution

    :param veh_availabilities: vehicle availabilities
    :param output_path: path where aggregated results shall be stored
    :param rtp_input_data_path: real time prices input file in h5 file format
    :return: None
    """
    # Extract min and max time
    t_min = pd.Timestamp(veh_availabilities['t_arrival'].min()).floor('1d')
    t_max = pd.Timestamp(veh_availabilities['t_departure'].max()).ceil('1d')
    # Date range from minimal to maximal time
    t_range = pd.date_range(start=t_min, end=t_max, freq='15Min')
    """
    #################################################################
    # Preparation ###################################################
    #################################################################
    """
    # List all power levels
    power_levels = os.listdir(output_path)
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    # initialize variables for y-limits calculation (passed to plot function)
    max_forecast = max_power = max_price = -np.inf
    min_forecast = min_power = min_price = np.inf

    # Go through all power levels
    for power in tqdm(power_levels):
        # Create folder for aggregated data
        Path(output_path + str(power) + '/Aggregated Data').mkdir(parents=True, exist_ok=True)
        # List all pricing strategies
        pricing_strategies = os.listdir(output_path + power)
        if 'Aggregated Data' in pricing_strategies:
            pricing_strategies.remove('Aggregated Data')
        # List all ev flex offer files
        file_names = os.listdir(output_path + power + '/' + pricing_strategies[0])
        # Create df for sum of optimal charging plans
        opt_sum_df = pd.DataFrame(0, index=t_range, columns={'P_ev_opt_sum_tou',
                                                             'P_ev_opt_sum_con',
                                                             'P_ev_opt_sum_tou_mi',
                                                             'P_ev_opt_sum_con_mi',
                                                             'P_ev_opt_sum_rtp',
                                                             'n_veh_avail',
                                                             'c_tou_kwh',
                                                             'c_con_kwh',
                                                             'c_tou_mi_kwh',
                                                             'c_con_mi_kwh',
                                                             'c_rtp_kwh',
                                                             'c_tou_energy',
                                                             'c_con_energy',
                                                             'c_tou_mi_energy',
                                                             'c_con_mi_energy',
                                                             'c_rtp_energy',
                                                             'Daytime_ID'})
        # Create df for sum of flexibility
        flex_sum_df = pd.DataFrame(0, index=t_range, columns={'P_pos_sum_tou',
                                                              'P_pos_sum_tou_mi',
                                                              'P_pos_sum_con',
                                                              'P_pos_sum_con_mi',
                                                              'P_pos_sum_rtp',
                                                              'P_neg_sum_tou',
                                                              'P_neg_sum_tou_mi',
                                                              'P_neg_sum_con',
                                                              'P_neg_sum_con_mi',
                                                              'P_neg_sum_rtp',
                                                              'E_pos_sum_tou',
                                                              'E_pos_sum_tou_mi',
                                                              'E_pos_sum_con',
                                                              'E_pos_sum_con_mi',
                                                              'E_pos_sum_rtp',
                                                              'E_neg_sum_tou',
                                                              'E_neg_sum_tou_mi',
                                                              'E_neg_sum_con',
                                                              'E_neg_sum_con_mi',
                                                              'E_neg_sum_rtp',
                                                              'c_flex_pos_tou',
                                                              'max_c_flex_pos_tou',
                                                              'min_c_flex_pos_tou',
                                                              'c_flex_pos_tou_mi',
                                                              'max_c_flex_pos_tou_mi',
                                                              'min_c_flex_pos_tou_mi',
                                                              'c_flex_pos_con',
                                                              'max_c_flex_pos_con',
                                                              'min_c_flex_pos_con',
                                                              'c_flex_pos_con_mi',
                                                              'max_c_flex_pos_con_mi',
                                                              'min_c_flex_pos_con_mi',
                                                              'c_flex_pos_rtp',
                                                              'max_c_flex_pos_rtp',
                                                              'min_c_flex_pos_rtp',
                                                              'c_flex_neg_tou',
                                                              'max_c_flex_neg_tou',
                                                              'min_c_flex_neg_tou',
                                                              'c_flex_neg_tou_mi',
                                                              'max_c_flex_neg_tou_mi',
                                                              'min_c_flex_neg_tou_mi',
                                                              'c_flex_neg_con',
                                                              'max_c_flex_neg_con',
                                                              'min_c_flex_neg_con',
                                                              'c_flex_neg_con_mi',
                                                              'max_c_flex_neg_con_mi',
                                                              'min_c_flex_neg_con_mi',
                                                              'c_flex_neg_rtp',
                                                              'max_c_flex_neg_rtp',
                                                              'min_c_flex_neg_rtp',
                                                              'Daytime_ID'})
        # Assigning -inf/inf to max/minprice columns for calculation of upper and lower bounds of the flexibility price
        max_prices_list = ['max_c_flex_pos_tou', 'max_c_flex_pos_tou_mi', 'max_c_flex_pos_con',
                           'max_c_flex_pos_con_mi', 'max_c_flex_pos_rtp', 'max_c_flex_neg_tou',
                           'max_c_flex_neg_tou_mi', 'max_c_flex_neg_con', 'max_c_flex_neg_con_mi',
                           'max_c_flex_neg_rtp']
        min_prices_list = ['min_c_flex_pos_tou', 'min_c_flex_pos_tou_mi', 'min_c_flex_pos_con',
                           'min_c_flex_pos_con_mi', 'min_c_flex_pos_rtp', 'min_c_flex_neg_tou',
                           'min_c_flex_neg_tou_mi', 'min_c_flex_neg_con', 'min_c_flex_neg_con_mi',
                           'min_c_flex_neg_rtp']
        for maxprice in max_prices_list:
            flex_sum_df[maxprice] = -np.inf
        for minprice in min_prices_list:
            flex_sum_df[minprice] = np.inf

        # Get forecast electricity prices for each time step
        price_forecast = forecast.simulate_elect_price_fcst(rtp_input_data_path=rtp_input_data_path,
                                                            t_start=t_min,
                                                            t_end=t_max,
                                                            pr_constant=0.19)
        opt_sum_df.loc[:, 'c_tou_kwh'] = price_forecast['ToU']
        opt_sum_df.loc[:, 'c_con_kwh'] = price_forecast['Constant']
        opt_sum_df.loc[:, 'c_tou_mi_kwh'] = price_forecast['ToU_mi']
        opt_sum_df.loc[:, 'c_con_mi_kwh'] = price_forecast['Con_mi']
        opt_sum_df.loc[:, 'c_rtp_kwh'] = price_forecast['RTP']
        # Create a daytime identifier for weekday and time for heat map
        opt_sum_df['Daytime_ID'] = opt_sum_df.index.day_name().array + ', ' + opt_sum_df.index.strftime('%H:%M').array
        flex_sum_df['Daytime_ID'] = opt_sum_df.index.day_name().array + ', ' + opt_sum_df.index.strftime('%H:%M').array
        # Go through all files
        for result_name in file_names:
            my_ems_tou_mi = opentumflex.init_ems_js(path=output_path + str(power) + '/ToU_mi/' + result_name)
            my_ems_tou = opentumflex.init_ems_js(path=output_path + str(power) + '/ToU/' + result_name)
            my_ems_con_mi = opentumflex.init_ems_js(path=output_path + str(power) + '/Con_mi/' + result_name)
            my_ems_con = opentumflex.init_ems_js(path=output_path + str(power) + '/Constant/' + result_name)
            my_ems_rtp = opentumflex.init_ems_js(path=output_path + str(power) + '/RTP/' + result_name)

            # Setting all flex prices that are zero & don't have a correlating flex power to NaN
            my_ems_list = [my_ems_tou_mi, my_ems_tou, my_ems_con_mi, my_ems_con, my_ems_rtp]
            price_l = ['Pos_Pr', 'Neg_Pr']
            power_l = ['Pos_P', 'Neg_P']
            # set_sign_l = [np.inf, -np.inf]
            for my_ems in my_ems_list:
                for pr, p in zip(price_l, power_l):
                    my_ems['flexopts']['ev'].loc[((my_ems['flexopts']['ev'][pr] == 0) &
                                                  (my_ems['flexopts']['ev'][p] == 0)), pr] = np.NAN
            # my_ems_con['flexopts']['ev'].loc[((my_ems_con['flexopts']['ev']['Pos_Pr'] == 0) &
            #                                   (my_ems_con['flexopts']['ev']['Pos_P'] == 0)), 'Pos_Pr'] = np.NAN

            opt_result_df = pd.DataFrame({'P_ev_opt_tou_mi': my_ems_tou_mi['optplan']['EV_power'],
                                          'P_ev_opt_tou': my_ems_tou['optplan']['EV_power'],
                                          'P_ev_opt_con_mi': my_ems_con_mi['optplan']['EV_power'],
                                          'P_ev_opt_con': my_ems_con['optplan']['EV_power'],
                                          'P_ev_opt_rtp': my_ems_rtp['optplan']['EV_power']},
                                         index=pd.date_range(start=my_ems_tou_mi['time_data']['time_slots'][0],
                                                             end=my_ems_tou_mi['time_data']['time_slots'][-1],
                                                             freq='15Min'))
            flex_result_df = pd.DataFrame({'P_pos_tou': my_ems_tou['flexopts']['ev']['Pos_P'],
                                           'P_pos_tou_mi': my_ems_tou_mi['flexopts']['ev']['Pos_P'],
                                           'P_pos_con': my_ems_con['flexopts']['ev']['Pos_P'],
                                           'P_pos_con_mi': my_ems_con_mi['flexopts']['ev']['Pos_P'],
                                           'P_pos_rtp': my_ems_rtp['flexopts']['ev']['Pos_P'],
                                           'P_neg_tou': my_ems_tou['flexopts']['ev']['Neg_P'],
                                           'P_neg_tou_mi': my_ems_tou_mi['flexopts']['ev']['Neg_P'],
                                           'P_neg_con': my_ems_con['flexopts']['ev']['Neg_P'],
                                           'P_neg_con_mi': my_ems_con_mi['flexopts']['ev']['Neg_P'],
                                           'P_neg_rtp': my_ems_rtp['flexopts']['ev']['Neg_P'],
                                           'E_pos_tou': my_ems_tou['flexopts']['ev']['Pos_E'],
                                           'E_pos_tou_mi': my_ems_tou_mi['flexopts']['ev']['Pos_E'],
                                           'E_pos_con': my_ems_con['flexopts']['ev']['Pos_E'],
                                           'E_pos_con_mi': my_ems_con_mi['flexopts']['ev']['Pos_E'],
                                           'E_pos_rtp': my_ems_rtp['flexopts']['ev']['Pos_E'],
                                           'E_neg_tou': my_ems_tou['flexopts']['ev']['Neg_E'],
                                           'E_neg_tou_mi': my_ems_tou_mi['flexopts']['ev']['Neg_E'],
                                           'E_neg_con': my_ems_con['flexopts']['ev']['Neg_E'],
                                           'E_neg_con_mi': my_ems_con_mi['flexopts']['ev']['Neg_E'],
                                           'E_neg_rtp': my_ems_rtp['flexopts']['ev']['Neg_E'],
                                           'c_flex_pos_tou': my_ems_tou['flexopts']['ev']['Pos_Pr'],
                                           'c_flex_pos_tou_mi': my_ems_tou_mi['flexopts']['ev']['Pos_Pr'],
                                           'c_flex_pos_con': my_ems_con['flexopts']['ev']['Pos_Pr'],
                                           'c_flex_pos_con_mi': my_ems_con_mi['flexopts']['ev']['Pos_Pr'],
                                           'c_flex_pos_rtp': my_ems_rtp['flexopts']['ev']['Pos_Pr'],
                                           'c_flex_neg_tou': my_ems_tou['flexopts']['ev']['Neg_Pr'],
                                           'c_flex_neg_tou_mi': my_ems_tou_mi['flexopts']['ev']['Neg_Pr'],
                                           'c_flex_neg_con': my_ems_con['flexopts']['ev']['Neg_Pr'],
                                           'c_flex_neg_con_mi': my_ems_con_mi['flexopts']['ev']['Neg_Pr'],
                                           'c_flex_neg_rtp': my_ems_rtp['flexopts']['ev']['Neg_Pr']
                                           },
                                          index=pd.date_range(start=my_ems_tou_mi['time_data']['time_slots'][0],
                                                              end=my_ems_tou_mi['time_data']['time_slots'][-1],
                                                              freq='15Min'))
            # Optimal charging power addition
            opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_tou_mi'] \
                += opt_result_df['P_ev_opt_tou_mi']
            opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_tou'] \
                += opt_result_df['P_ev_opt_tou']
            opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_con_mi'] \
                += opt_result_df['P_ev_opt_con_mi']
            opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_con'] \
                += opt_result_df['P_ev_opt_con']
            opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_rtp'] \
                += opt_result_df['P_ev_opt_rtp']
            opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'n_veh_avail'] += 1
            # Flexible power addition
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_tou'] \
                += flex_result_df['P_pos_tou']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_tou_mi'] \
                += flex_result_df['P_pos_tou_mi']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_con'] \
                += flex_result_df['P_pos_con']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_con_mi'] \
                += flex_result_df['P_pos_con_mi']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_rtp'] \
                += flex_result_df['P_pos_rtp']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_tou'] \
                += flex_result_df['P_neg_tou']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_tou_mi'] \
                += flex_result_df['P_neg_tou_mi']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_con'] \
                += flex_result_df['P_neg_con']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_con_mi'] \
                += flex_result_df['P_neg_con_mi']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_rtp'] \
                += flex_result_df['P_neg_rtp']
            # Flexible energy addition
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_tou'] \
                += flex_result_df['E_pos_tou']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_tou_mi'] \
                += flex_result_df['E_pos_tou_mi']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_con'] \
                += flex_result_df['E_pos_con']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_con_mi'] \
                += flex_result_df['E_pos_con_mi']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_rtp'] \
                += flex_result_df['E_pos_rtp']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_tou'] \
                += flex_result_df['E_neg_tou']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_tou_mi'] \
                += flex_result_df['E_neg_tou_mi']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_con'] \
                += flex_result_df['E_neg_con']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_con_mi'] \
                += flex_result_df['E_neg_con_mi']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_rtp'] \
                += flex_result_df['E_neg_rtp']

            # lists of all flex prices for combination in for loop, min/max NOT from absolute values, max/min already
            # assigned above
            flex_prices_list = ['c_flex_pos_tou', 'c_flex_pos_tou_mi', 'c_flex_pos_con',
                                'c_flex_pos_con_mi', 'c_flex_pos_rtp', 'c_flex_neg_tou',
                                'c_flex_neg_tou_mi', 'c_flex_neg_con', 'c_flex_neg_con_mi',
                                'c_flex_neg_rtp']
            # max_prices_list = ['max_c_flex_pos_tou', 'max_c_flex_pos_tou_mi', 'max_c_flex_pos_con',
            #                    'max_c_flex_pos_con_mi', 'max_c_flex_pos_rtp','max_c_flex_neg_tou',
            #                    'max_c_flex_neg_tou_mi', 'max_c_flex_neg_con', 'max_c_flex_neg_con_mi',
            #                    'max_c_flex_neg_rtp']
            # min_prices_list = ['min_c_flex_pos_tou', 'min_c_flex_pos_tou_mi', 'min_c_flex_pos_con',
            #                    'min_c_flex_pos_con_mi', 'min_c_flex_pos_rtp', 'min_c_flex_neg_tou',
            #                    'min_c_flex_neg_tou_mi', 'min_c_flex_neg_con', 'min_c_flex_neg_con_mi',
            #                    'min_c_flex_neg_rtp']

            # filling max/minprice columns, by only replacing when value from current availability is bigger/smaller
            ##### glz für pos/neg, weil ja nicht mehr "abs"
            # for maxprice, minprice in zip(max_prices_list, min_prices_list):
            #     flex_sum_df[maxprice] = -np.inf
            #     flex_sum_df[minprice] = np.inf
            for maxprice, flexprice in zip(max_prices_list, flex_prices_list):
                #flex_sum_df[maxprice] = 0 #scheint nicht nötig zu sein, würde auch sonst hier immer alles löschen
                # df_temp = flex_sum_df.loc[flex_result_df.index, :] # achtung falsch wsl!
                # flex_sum_df.loc[df_temp.index, maxprice] = np.where(
                #     df_temp[flexprice] <= flex_result_df[flexprice],
                #     flex_result_df[flexprice], df_temp[flexprice])
                df_temp = flex_sum_df.loc[flex_result_df.index, :]
                flex_sum_df.loc[df_temp.index, maxprice] = np.where(
                    df_temp[maxprice] <= flex_result_df[flexprice],
                    flex_result_df[flexprice], df_temp[maxprice])
            for minprice, flexprice in zip(min_prices_list, flex_prices_list):
                # df_temp = flex_sum_df.loc[flex_result_df.index, :] # alt und wsl falsch
                # flex_sum_df.loc[df_temp.index, minprice] = np.where(
                #     df_temp[flexprice] > flex_result_df[flexprice],
                #     flex_result_df[flexprice], df_temp[flexprice])
                df_temp = flex_sum_df.loc[flex_result_df.index, :]
                flex_sum_df.loc[df_temp.index, minprice] = np.where(
                    df_temp[minprice] >= flex_result_df[flexprice],
                    flex_result_df[flexprice], df_temp[minprice])
            # for flexprice in flex_prices_list:
            #     flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], flexprice] \
            #         += flex_result_df[flexprice]

        # Setting all flex prices in max/min price columns that are zero & don't have a correlating flex power to NaN

        # power_columns_list = ['P_pos_sum_tou', 'P_pos_sum_tou_mi', 'P_pos_sum_con', 'P_pos_sum_con_mi', 'P_pos_sum_rtp',
        #                       'P_neg_sum_tou', 'P_neg_sum_tou_mi', 'P_neg_sum_con', 'P_neg_sum_con_mi', 'P_neg_sum_rtp',]
        # for power_col, max_pr_col, min_pr_col in zip(power_columns_list, max_prices_list, min_prices_list):
        #     flex_sum_df.loc[((flex_sum_df[max_pr_col] == 0) &
        #                                   (flex_sum_df[power_col] == 0)), [max_pr_col]] = np.NAN
        #     flex_sum_df.loc[((flex_sum_df[min_pr_col] == 0) &
        #                                   (flex_sum_df[power_col] == 0)), [min_pr_col]] = np.NAN

        # replace all remaining inf values with NAN
        flex_sum_df.replace([np.inf, -np.inf], np.NAN, inplace=True)

        # Calculate energy costs
        opt_sum_df['c_tou_energy'] = opt_sum_df['c_tou_kwh'] * opt_sum_df['P_ev_opt_sum_tou'] \
                                     / my_ems_tou['time_data']['ntsteps']
        opt_sum_df['c_tou_mi_energy'] = opt_sum_df['c_tou_mi_kwh'] * opt_sum_df['P_ev_opt_sum_tou_mi'] \
                                        / my_ems_tou_mi['time_data']['ntsteps']
        opt_sum_df['c_con_energy'] = opt_sum_df['c_con_kwh'] * opt_sum_df['P_ev_opt_sum_con'] \
                                     / my_ems_con['time_data']['ntsteps']
        opt_sum_df['c_con_mi_energy'] = opt_sum_df['c_con_mi_kwh'] * opt_sum_df['P_ev_opt_sum_con_mi'] \
                                        / my_ems_con_mi['time_data']['ntsteps']
        opt_sum_df['c_rtp_energy'] = opt_sum_df['c_rtp_kwh'] * opt_sum_df['P_ev_opt_sum_rtp'] \
                                     / my_ems_rtp['time_data']['ntsteps']

        # Save data to hdf files for further analysis
        flex_sum_df.to_hdf(output_path + str(power) + '/Aggregated Data/flex_sum_data.h5', mode='w', key='df')
        opt_sum_df.to_hdf(output_path + str(power) + '/Aggregated Data/opt_sum_data.h5', mode='w', key='df')

        # # Read data if already processed
        # flex_sum_df = pd.read_hdf(output_path + 'Aggregated Data/flex_sum_data.h5')
        # opt_sum_df = pd.read_hdf(output_path + 'Aggregated Data/opt_sum_data.h5')

        # Calculate average, minimal and maximal number of vehicles
        n_veh_avail_mean = opt_sum_df['n_veh_avail'].mean()
        n_veh_avail_max = opt_sum_df['n_veh_avail'].max()
        n_veh_avail_min = opt_sum_df['n_veh_avail'].min()

        # Differentiating between summer, winter and all months with a for loop

        # create dict for for loop
        seasons_dict = {}
        # create winter/summer dataframes and update dict for for loop
        if any(x in opt_sum_df.index.month for x in [10, 11, 12, 1, 2, 3, 4, 5]):
            seasons_dict['winter'] = {}
            seasons_dict['winter']['opt_sum_df'] = opt_sum_df.loc[(opt_sum_df.index.month >= 10) | (opt_sum_df.index.month <= 5)]
            seasons_dict['winter']['flex_sum_df'] = flex_sum_df.loc[
                (flex_sum_df.index.month >= 10) | (flex_sum_df.index.month <= 5)]
        if any(x in opt_sum_df.index.month for x in [6, 7, 8, 9]):
            seasons_dict['summer'] = {}
            seasons_dict['summer']['opt_sum_df'] = opt_sum_df.loc[(opt_sum_df.index.month >= 6) | (opt_sum_df.index.month <= 9)]
            seasons_dict['summer']['flex_sum_df'] = flex_sum_df.loc[(flex_sum_df.index.month >= 6) | (flex_sum_df.index.month <= 9)]

        # add "all seasons" as last item in dict, as heatmap calculations after the for loop need data from all months
        seasons_dict['allseasons'] = {}
        seasons_dict['allseasons']['opt_sum_df'] = opt_sum_df
        seasons_dict['allseasons']['flex_sum_df'] = flex_sum_df

        # for loop over summer, winter and all seasons opt_sum and flex_sum dataframes
        for season, value in seasons_dict.items():
            season_opt_sum_df = value['opt_sum_df']
            season_flex_sum_df = value['flex_sum_df']

        # # for loop over summer, winter and all seasons opt_sum and flex_sum dataframes
        # for season_opt_sum_df, season_flex_sum_df, season in zip(seasons_opt_df_l, seasons_flex_df_l, seasons):

            """
            ####################################################################
            # Group optimal and flexible power schedules by daytime ID #########
            ####################################################################
            """
            # Prepare heat map for optimal charging power
            opt_per_daytime = pd.DataFrame()
            opt_per_daytime_temp = season_opt_sum_df.groupby(by='Daytime_ID').mean()
            opt_per_daytime = opt_per_daytime.append(opt_per_daytime_temp.iloc[96:192, :])
            opt_per_daytime = opt_per_daytime.append(opt_per_daytime_temp.iloc[480:, :])
            opt_per_daytime = opt_per_daytime.append(opt_per_daytime_temp.iloc[384:480, :])
            opt_per_daytime = opt_per_daytime.append(opt_per_daytime_temp.iloc[0:96, :])
            opt_per_daytime = opt_per_daytime.append(opt_per_daytime_temp.iloc[192:384, :])
            opt_per_daytime = opt_per_daytime.reset_index()

            # Calculate weekday and weekend and average day optimal schedule averages per daytime
            weekday_opt_per_daytime = (opt_per_daytime_temp.iloc[96:192, :] +
                                       opt_per_daytime_temp.iloc[480:576, :].values +
                                       opt_per_daytime_temp.iloc[576:, :].values +
                                       opt_per_daytime_temp.iloc[384:480, :].values +
                                       opt_per_daytime_temp.iloc[0:96, :].values) / 5
            weekday_opt_per_daytime = weekday_opt_per_daytime.set_index('Weekday, ' + pd.date_range(start='00:00',
                                                                                                    end='23:45',
                                                                                                    freq='15Min').strftime('%H:%M'))
            weekend_opt_per_daytime = (opt_per_daytime_temp.iloc[192:288, :] +
                                       opt_per_daytime_temp.iloc[288:384, :].values) / 2
            weekend_opt_per_daytime = weekend_opt_per_daytime.set_index('Weekend, ' + pd.date_range(start='00:00',
                                                                                                    end='23:45',
                                                                                                    freq='15Min').strftime('%H:%M'))
            day_opt_per_daytime = (opt_per_daytime_temp.iloc[96:192, :] +
                                   opt_per_daytime_temp.iloc[480:576, :].values +
                                   opt_per_daytime_temp.iloc[576:, :].values +
                                   opt_per_daytime_temp.iloc[384:480, :].values +
                                   opt_per_daytime_temp.iloc[0:96, :].values +
                                   opt_per_daytime_temp.iloc[192:288, :].values +
                                   opt_per_daytime_temp.iloc[288:384, :].values) / 7
            day_opt_per_daytime = day_opt_per_daytime.set_index('Day, ' + pd.date_range(start='00:00', end='23:45',
                                                                                        freq='15Min').strftime('%H:%M'))

            # Calculate percentiles per daytime
            opt_per_daytime_qt = pd.DataFrame()
            n_percentiles = 11           # Define number of percentiles
            percentiles = np.linspace(start=0, stop=1, num=n_percentiles)
            opt_per_daytime_temp = opt_sum_df.groupby(by='Daytime_ID').quantile(percentiles)
            opt_per_daytime_qt = opt_per_daytime_qt.append(opt_per_daytime_temp.iloc[96 * n_percentiles:192 * n_percentiles, :])
            opt_per_daytime_qt = opt_per_daytime_qt.append(opt_per_daytime_temp.iloc[480 * n_percentiles:, :])
            opt_per_daytime_qt = opt_per_daytime_qt.append(opt_per_daytime_temp.iloc[384 * n_percentiles:480 * n_percentiles, :])
            opt_per_daytime_qt = opt_per_daytime_qt.append(opt_per_daytime_temp.iloc[0:96 * n_percentiles, :])
            opt_per_daytime_qt = opt_per_daytime_qt.append(opt_per_daytime_temp.iloc[192 * n_percentiles:384 * n_percentiles, :])
            opt_per_daytime_qt = opt_per_daytime_qt.reset_index()
            # Prepare heat map for flexible power
            flex_per_daytime = pd.DataFrame()
            # flex_per_daytime_temp = flex_sum_df.groupby(by='Daytime_ID').mean()
            flex_per_daytime_temp = season_flex_sum_df.groupby(by='Daytime_ID').agg({'P_pos_sum_tou': 'mean',
                                                                                     'P_pos_sum_tou_mi': 'mean',
                                                                                     'P_pos_sum_con': 'mean',
                                                                                     'P_pos_sum_con_mi': 'mean',
                                                                                     'P_pos_sum_rtp': 'mean',
                                                                                     'P_neg_sum_tou': 'mean',
                                                                                     'P_neg_sum_tou_mi': 'mean',
                                                                                     'P_neg_sum_con': 'mean',
                                                                                     'P_neg_sum_con_mi': 'mean',
                                                                                     'P_neg_sum_rtp': 'mean',
                                                                                     'E_pos_sum_tou': 'mean',
                                                                                     'E_pos_sum_tou_mi': 'mean',
                                                                                     'E_pos_sum_con': 'mean',
                                                                                     'E_pos_sum_con_mi': 'mean',
                                                                                     'E_pos_sum_rtp': 'mean',
                                                                                     'E_neg_sum_tou': 'mean',
                                                                                     'E_neg_sum_tou_mi': 'mean',
                                                                                     'E_neg_sum_con': 'mean',
                                                                                     'E_neg_sum_con_mi': 'mean',
                                                                                     'E_neg_sum_rtp': 'mean',
                                                                                     'c_flex_pos_tou': 'mean',
                                                                                     'max_c_flex_pos_tou': 'max',
                                                                                     'min_c_flex_pos_tou': 'min',
                                                                                     'c_flex_pos_tou_mi': 'mean',
                                                                                     'max_c_flex_pos_tou_mi': 'max',
                                                                                     'min_c_flex_pos_tou_mi': 'min',
                                                                                     'c_flex_pos_con': 'mean',
                                                                                     'max_c_flex_pos_con': 'max',
                                                                                     'min_c_flex_pos_con': 'min',
                                                                                     'c_flex_pos_con_mi': 'mean',
                                                                                     'max_c_flex_pos_con_mi': 'max',
                                                                                     'min_c_flex_pos_con_mi': 'min',
                                                                                     'c_flex_pos_rtp': 'mean',
                                                                                     'max_c_flex_pos_rtp': 'max',
                                                                                     'min_c_flex_pos_rtp': 'min',
                                                                                     'c_flex_neg_tou': 'mean',
                                                                                     'max_c_flex_neg_tou': 'max',
                                                                                     'min_c_flex_neg_tou': 'min',
                                                                                     'c_flex_neg_tou_mi': 'mean',
                                                                                     'max_c_flex_neg_tou_mi': 'max',
                                                                                     'min_c_flex_neg_tou_mi': 'min',
                                                                                     'c_flex_neg_con': 'mean',
                                                                                     'max_c_flex_neg_con': 'max',
                                                                                     'min_c_flex_neg_con': 'min',
                                                                                     'c_flex_neg_con_mi': 'mean',
                                                                                     'max_c_flex_neg_con_mi': 'max',
                                                                                     'min_c_flex_neg_con_mi': 'min',
                                                                                     'c_flex_neg_rtp': 'mean',
                                                                                     'max_c_flex_neg_rtp': 'max',
                                                                                     'min_c_flex_neg_rtp': 'min'})
            flex_per_daytime = flex_per_daytime.append(flex_per_daytime_temp.iloc[96:192, :])
            flex_per_daytime = flex_per_daytime.append(flex_per_daytime_temp.iloc[480:, :])
            flex_per_daytime = flex_per_daytime.append(flex_per_daytime_temp.iloc[384:480, :])
            flex_per_daytime = flex_per_daytime.append(flex_per_daytime_temp.iloc[0:96, :])
            flex_per_daytime = flex_per_daytime.append(flex_per_daytime_temp.iloc[192:384, :])
            flex_per_daytime = flex_per_daytime.reset_index()

            # Calculate weekday and weekend and day flexibility averages per daytime
            weekday_flex_per_daytime = (flex_per_daytime_temp.iloc[96:192, :] +
                                        flex_per_daytime_temp.iloc[480:576, :].values +
                                        flex_per_daytime_temp.iloc[576:, :].values +
                                        flex_per_daytime_temp.iloc[384:480, :].values +
                                        flex_per_daytime_temp.iloc[0:96, :].values) / 5
            weekday_flex_per_daytime = weekday_flex_per_daytime.set_index('Weekday, ' + pd.date_range(start='00:00',
                                                                                                      end='23:45',
                                                                                                      freq='15Min').strftime('%H:%M'))
            weekend_flex_per_daytime = (flex_per_daytime_temp.iloc[192:288, :] +
                                        flex_per_daytime_temp.iloc[288:384, :].values) / 2
            weekend_flex_per_daytime = weekend_flex_per_daytime.set_index('Weekend, ' + pd.date_range(start='00:00',
                                                                                                      end='23:45',
                                                                                                      freq='15Min').strftime('%H:%M'))
            day_flex_per_daytime = (flex_per_daytime_temp.iloc[96:192, :] +
                                    flex_per_daytime_temp.iloc[480:576, :].values +
                                    flex_per_daytime_temp.iloc[576:, :].values +
                                    flex_per_daytime_temp.iloc[384:480, :].values +
                                    flex_per_daytime_temp.iloc[0:96, :].values +
                                    flex_per_daytime_temp.iloc[192:288, :].values +
                                    flex_per_daytime_temp.iloc[288:384, :].values) / 7
            day_flex_per_daytime = day_flex_per_daytime.set_index('Day, ' + pd.date_range(start='00:00', end='23:45',
                                                                                          freq='15Min').strftime('%H:%M'))

            # Calculate Weekday/Weekend/Day flex for Flex prices (adding and dividing by 2/5/7 does not work because of NANs)
            # list of columns that should be grouped/averaged by 15 min timestamp
            power_column_list = ['P_pos_sum_tou', 'P_pos_sum_tou_mi', 'P_pos_sum_con', 'P_pos_sum_con_mi',
                                 'P_pos_sum_rtp', 'P_neg_sum_tou', 'P_neg_sum_tou_mi', 'P_neg_sum_con',
                                 'P_neg_sum_con_mi', 'P_neg_sum_rtp']
            price_column_list = ['max_c_flex_pos_tou', 'min_c_flex_pos_tou',
                                 'max_c_flex_pos_tou_mi', 'min_c_flex_pos_tou_mi',
                                 'max_c_flex_pos_con', 'min_c_flex_pos_con',
                                 'max_c_flex_pos_con_mi', 'min_c_flex_pos_con_mi',
                                 'max_c_flex_pos_rtp', 'min_c_flex_pos_rtp',
                                 'max_c_flex_neg_tou', 'min_c_flex_neg_tou',
                                 'max_c_flex_neg_tou_mi', 'min_c_flex_neg_tou_mi',
                                 'max_c_flex_neg_con', 'min_c_flex_neg_con',
                                 'max_c_flex_neg_con_mi', 'min_c_flex_neg_con_mi',
                                 'max_c_flex_neg_rtp', 'min_c_flex_neg_rtp']

            # combining concat/join?
            # weekday_flex_prices = flex_per_daytime[column_list].iloc[[]]
            # weekend_flex_prices
            day_flex_prices = pd.DataFrame()
            weekday_flex_prices = pd.DataFrame()
            weekend_flex_prices = pd.DataFrame()
            test_flex_prices = pd.DataFrame()
            for i in range(96):
                day_flex_prices = pd.concat([day_flex_prices,
                                             pd.DataFrame(flex_per_daytime[price_column_list].iloc[i::96].mean(axis=0)).T],
                                            ignore_index=True, axis=0)
                weekday_flex_prices = pd.concat([weekday_flex_prices,
                                                 pd.DataFrame(flex_per_daytime[price_column_list].iloc[i:480:96].mean(
                                                     axis=0)).T],
                                                ignore_index=True, axis=0)
                weekend_flex_prices = pd.concat([weekend_flex_prices,
                                                 pd.DataFrame(flex_per_daytime[price_column_list].iloc[i+480::96].mean(
                                                     axis=0)).T],
                                                ignore_index=True, axis=0)

                test_flex_prices = pd.concat([test_flex_prices,
                                              pd.DataFrame(flex_per_daytime[power_column_list].iloc[i + 480::96].mean(
                                                  axis=0)).T],
                                             ignore_index=True, axis=0)

            # Save data to hdf files for further analysis
            if season == 'allseasons':
                opt_per_daytime.to_hdf(output_path + str(power) + '/Aggregated Data/opt_per_daytime_data.h5', mode='w', key='df')
                opt_per_daytime_qt.to_hdf(output_path + str(power) + '/Aggregated Data/opt_per_daytime_qt_data.h5', mode='w', key='df')
                flex_per_daytime.to_hdf(output_path + str(power) + '/Aggregated Data/flex_per_daytime_data.h5', mode='w', key='df')

            weekday_opt_per_daytime.to_hdf(output_path + str(power) + '/Aggregated Data/' + str(season) + '_weekday_opt_per_daytime_data.h5', mode='w', key='df')
            weekend_opt_per_daytime.to_hdf(output_path + str(power) + '/Aggregated Data/' + str(season) + '_weekend_opt_per_daytime_data.h5', mode='w', key='df')
            day_opt_per_daytime.to_hdf(output_path + str(power) + '/Aggregated Data/' + str(season) + '_day_opt_per_daytime_data.h5', mode='w', key='df')
            weekday_flex_per_daytime.to_hdf(output_path + str(power) + '/Aggregated Data/' + str(season) + '_weekday_flex_per_daytime_data.h5', mode='w', key='df')
            weekend_flex_per_daytime.to_hdf(output_path + str(power) + '/Aggregated Data/' + str(season) + '_weekend_flex_per_daytime_data.h5', mode='w', key='df')
            day_flex_per_daytime.to_hdf(output_path + str(power) + '/Aggregated Data/' + str(season) + '_day_flex_per_daytime_data.h5', mode='w', key='df')
            day_flex_prices.to_hdf(output_path + str(power) + '/Aggregated Data/' + str(season) + '_day_flex_prices_data.h5', mode='w', key='df')
            weekday_flex_prices.to_hdf(output_path + str(power) + '/Aggregated Data/' + str(season) + '_weekday_flex_prices_data.h5', mode='w', key='df')
            weekend_flex_prices.to_hdf(output_path + str(power) + '/Aggregated Data/' + str(season) + '_weekend_flex_prices_data.h5', mode='w', key='df')

        # Calculate ylims for flex price plots (no su/wi differentiation for comparability, so from allseason)
        # for price forecast
        for df in [day_opt_per_daytime, weekday_opt_per_daytime, weekend_opt_per_daytime]:
            max_forecast_temp = df[['c_tou_kwh', 'c_con_kwh', 'c_tou_mi_kwh', 'c_con_mi_kwh', 'c_rtp_kwh']].max().max()
            min_forecast_temp = df[['c_tou_kwh', 'c_con_kwh', 'c_tou_mi_kwh', 'c_con_mi_kwh', 'c_rtp_kwh']].min().min()
            if max_forecast < max_forecast_temp:
                max_forecast = max_forecast_temp
            if min_forecast > min_forecast_temp:
                min_forecast = min_forecast_temp

        # for flexibility power --> loop oder einfach die max/min limits vor dem zu Wochentag/... mean?
        flex_dfs_list = [day_flex_per_daytime, weekday_flex_per_daytime, weekend_flex_per_daytime]
        opt_dfs_list = [day_opt_per_daytime, weekday_opt_per_daytime, weekend_opt_per_daytime]
        for flex_df, opt_df in zip(flex_dfs_list, opt_dfs_list):
            max_power_temp = (flex_df[['P_pos_sum_tou', 'P_pos_sum_tou_mi', 'P_pos_sum_con', 'P_pos_sum_con_mi',
                                        'P_pos_sum_rtp']].div(opt_df['n_veh_avail'], axis=0)).max().max()
            min_power_temp = (flex_df[['P_neg_sum_tou', 'P_neg_sum_tou_mi', 'P_neg_sum_con', 'P_neg_sum_con_mi',
                                       'P_neg_sum_rtp']].div(opt_df['n_veh_avail'], axis=0)).min().min()
            if max_power < max_power_temp:
                max_power = max_power_temp
            if min_power > min_power_temp:
                min_power = min_power_temp

        for df in [day_flex_prices, weekday_flex_prices, weekend_flex_prices]:
            max_price_temp = df[['max_c_flex_pos_tou', 'max_c_flex_pos_tou_mi', 'max_c_flex_pos_con',
                                 'max_c_flex_pos_con_mi', 'max_c_flex_pos_rtp', 'max_c_flex_neg_tou',
                                 'max_c_flex_neg_tou_mi', 'max_c_flex_neg_con', 'max_c_flex_neg_con_mi',
                                 'max_c_flex_neg_rtp']].max().max()
            min_price_temp = df[['min_c_flex_pos_tou', 'min_c_flex_pos_tou_mi', 'min_c_flex_pos_con',
                                 'min_c_flex_pos_con_mi', 'min_c_flex_pos_rtp', 'min_c_flex_neg_tou',
                                 'min_c_flex_neg_tou_mi', 'min_c_flex_neg_con', 'min_c_flex_neg_con_mi',
                                 'min_c_flex_neg_rtp']].min().min()
            if max_price < max_price_temp:
                max_price = max_price_temp
            if min_price > min_price_temp:
                min_price = min_price_temp

        # prepare df for week heat map
        P_pos_tou_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                    columns=days)
        P_pos_con_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                      columns=days)
        P_pos_tou_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                       columns=days)
        P_pos_con_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                         columns=days)
        P_pos_rtp_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                    columns=days)
        P_neg_tou_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                    columns=days)
        P_neg_con_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                      columns=days)
        P_neg_tou_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                       columns=days)
        P_neg_con_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                         columns=days)
        P_neg_rtp_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                    columns=days)
        n_avail_veh_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                      columns=days)

        # Copy power to single day columns
        for i in range(7):
            P_pos_tou_hm[days[i]] = flex_per_daytime['P_pos_sum_tou'].iloc[i * 96:i * 96 + 96].values
            P_pos_con_hm[days[i]] = flex_per_daytime['P_pos_sum_con'].iloc[i * 96:i * 96 + 96].values
            P_pos_tou_mi_hm[days[i]] = flex_per_daytime['P_pos_sum_tou_mi'].iloc[i * 96:i * 96 + 96].values
            P_pos_con_mi_hm[days[i]] = flex_per_daytime['P_pos_sum_con_mi'].iloc[i * 96:i * 96 + 96].values
            P_pos_rtp_hm[days[i]] = flex_per_daytime['P_pos_sum_rtp'].iloc[i * 96:i * 96 + 96].values
            P_neg_tou_hm[days[i]] = flex_per_daytime['P_neg_sum_tou'].iloc[i * 96:i * 96 + 96].values
            P_neg_con_hm[days[i]] = flex_per_daytime['P_neg_sum_con'].iloc[i * 96:i * 96 + 96].values
            P_neg_tou_mi_hm[days[i]] = flex_per_daytime['P_neg_sum_tou_mi'].iloc[i * 96:i * 96 + 96].values
            P_neg_con_mi_hm[days[i]] = flex_per_daytime['P_neg_sum_con_mi'].iloc[i * 96:i * 96 + 96].values
            P_neg_rtp_hm[days[i]] = flex_per_daytime['P_neg_sum_rtp'].iloc[i * 96:i * 96 + 96].values
            n_avail_veh_hm[days[i]] = opt_per_daytime['n_veh_avail'].iloc[i * 96:i * 96 + 96].values

        # Save heat map dataframes to files
        P_pos_tou_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_pos_tou_hm_data.h5', mode='w', key='df')
        P_pos_con_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_pos_con_hm_data.h5', mode='w', key='df')
        P_pos_tou_mi_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_pos_tou_mi_hm_data.h5', mode='w', key='df')
        P_pos_con_mi_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_pos_con_mi_hm_data.h5', mode='w', key='df')
        P_pos_rtp_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_pos_rtp_hm_data.h5', mode='w', key='df')
        P_neg_tou_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_neg_tou_hm_data.h5', mode='w', key='df')
        P_neg_con_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_neg_con_hm_data.h5', mode='w', key='df')
        P_neg_tou_mi_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_neg_tou_mi_hm_data.h5', mode='w', key='df')
        P_neg_con_mi_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_neg_con_mi_hm_data.h5', mode='w', key='df')
        P_neg_rtp_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_neg_rtp_hm_data.h5', mode='w', key='df')
        n_avail_veh_hm.to_hdf(output_path + str(power) + '/Aggregated Data/n_veh_avail_hm_data.h5', mode='w', key='df')

    # create ylim-dict with overall maximum and minimum values to pass to plot flex prices function
    ylim_dict = {'forecast': {'max': max_forecast, 'min': min_forecast},
                 'flex power': {'max': max_power, 'min': min_power},
                 'flex price': {'max': max_price, 'min': min_price}}

    return ylim_dict


if __name__ == '__main__':
    # Read veh availabilities from file
    veh_avail = pd.read_csv('../input/chts_veh_availability.csv')
    # Extract a subsample for testing
    veh_avail = veh_avail[:]

    aggregate_ev_flex(veh_avail, output_path='../output/')

