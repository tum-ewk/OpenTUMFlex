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

import pandas as pd
import os
import numpy as np
import opentumflex
import forecast
from pathlib import Path


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
    """
    #################################################################
    # Preparation ###################################################
    #################################################################
    """
    # List all power levels
    power_levels = os.listdir(output_path)
    # List all pricing strategies
    pricing_strategies = os.listdir(output_path + power_levels[0])
    if 'Aggregated Data' in pricing_strategies: pricing_strategies.remove('Aggregated Data')
    # List all ev flex offer files
    file_names = os.listdir(output_path + power_levels[0] + '/' + pricing_strategies[0])
    # Date range from minimal to maximal time
    t_range = pd.date_range(start=t_min, end=t_max, freq='15Min')
    # Create df for sum of optimal charging plans
    opt_sum_df = pd.DataFrame(0, index=t_range, columns={'P_ev_opt_sum_tou',
                                                         'P_ev_opt_sum_const',
                                                         'P_ev_opt_sum_tou_mi',
                                                         'P_ev_opt_sum_const_mi',
                                                         'P_ev_opt_sum_rtp',
                                                         'n_veh_avail',
                                                         'c_elect_in_tou',
                                                         'c_elect_in_const',
                                                         'c_elect_in_tou_mi',
                                                         'c_elect_in_const_mi',
                                                         'c_elect_in_rtp',
                                                         'Daytime_ID'})
    # Create df for sum of flexibility
    flex_sum_df = pd.DataFrame(0, index=t_range, columns={'P_pos_sum_tou',
                                                          'P_pos_sum_tou_mi',
                                                          'P_pos_sum_const',
                                                          'P_pos_sum_const_mi',
                                                          'P_pos_sum_rtp',
                                                          'P_neg_sum_tou',
                                                          'P_neg_sum_tou_mi',
                                                          'P_neg_sum_const',
                                                          'P_neg_sum_const_mi',
                                                          'P_neg_sum_rtp',
                                                          'E_pos_sum_tou',
                                                          'E_pos_sum_tou_mi',
                                                          'E_pos_sum_const',
                                                          'E_pos_sum_const_mi',
                                                          'E_pos_sum_rtp',
                                                          'E_neg_sum_tou',
                                                          'E_neg_sum_tou_mi',
                                                          'E_neg_sum_const',
                                                          'E_neg_sum_const_mi',
                                                          'E_neg_sum_rtp',
                                                          'c_flex_pos_tou',
                                                          'c_flex_pos_tou_mi',
                                                          'c_flex_pos_const',
                                                          'c_flex_pos_const_mi',
                                                          'c_flex_pos_rtp',
                                                          'c_flex_neg_tou',
                                                          'c_flex_neg_tou_mi',
                                                          'c_flex_neg_const',
                                                          'c_flex_neg_const_mi',
                                                          'c_flex_neg_rtp',
                                                          'Daytime_ID'})
    # Get forecast electricity prices for each time step
    price_forecast = forecast.simulate_elect_price_fcst(rtp_input_data_path=rtp_input_data_path,
                                                        t_start=t_min,
                                                        t_end=t_max,
                                                        pr_constant=0.19)
    opt_sum_df.loc[:, 'c_elect_in_tou'] = price_forecast['ToU']
    opt_sum_df.loc[:, 'c_elect_in_const'] = price_forecast['Constant']
    opt_sum_df.loc[:, 'c_elect_in_tou_mi'] = price_forecast['ToU_mi']
    opt_sum_df.loc[:, 'c_elect_in_const_mi'] = price_forecast['Con_mi']
    opt_sum_df.loc[:, 'c_elect_in_rtp'] = price_forecast['RTP']
    # Create a daytime identifier for weekday and time for heat map
    opt_sum_df['Daytime_ID'] = opt_sum_df.index.day_name().array + \
                                    ', ' + \
                               opt_sum_df.index.strftime('%H:%M').array
    flex_sum_df['Daytime_ID'] = opt_sum_df.index.day_name().array + \
                                    ', ' + \
                                opt_sum_df.index.strftime('%H:%M').array
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    # Go through all power levels
    for power in power_levels:
        # Create folder for aggregated data
        Path(output_path + str(power) + '/Aggregated Data').mkdir(parents=True, exist_ok=True)
        # Go through all files
        for result_name in file_names:
            my_ems_tou_mi = opentumflex.init_ems_js(path=output_path + str(power) + '/ToU_mi/' + result_name)
            my_ems_tou = opentumflex.init_ems_js(path=output_path + str(power) + '/ToU/' + result_name)
            my_ems_const_mi = opentumflex.init_ems_js(path=output_path + str(power) + '/Con_mi/' + result_name)
            my_ems_const = opentumflex.init_ems_js(path=output_path + str(power) + '/Constant/' + result_name)
            my_ems_rtp = opentumflex.init_ems_js(path=output_path + str(power) + '/RTP/' + result_name)

            opt_result_df = pd.DataFrame({'P_ev_opt_tou_mi': my_ems_tou_mi['optplan']['EV_power'],
                                          'P_ev_opt_tou': my_ems_tou['optplan']['EV_power'],
                                          'P_ev_opt_const_mi': my_ems_const_mi['optplan']['EV_power'],
                                          'P_ev_opt_const': my_ems_const['optplan']['EV_power'],
                                          'P_ev_opt_rtp': my_ems_rtp['optplan']['EV_power']},
                                         index=pd.date_range(start=my_ems_tou_mi['time_data']['time_slots'][0],
                                                             end=my_ems_tou_mi['time_data']['time_slots'][-1],
                                                             freq='15Min'))
            flex_result_df = pd.DataFrame({'P_pos_tou': my_ems_tou['flexopts']['ev']['Pos_P'],
                                           'P_pos_tou_mi': my_ems_tou_mi['flexopts']['ev']['Pos_P'],
                                           'P_pos_const': my_ems_const['flexopts']['ev']['Pos_P'],
                                           'P_pos_const_mi': my_ems_const_mi['flexopts']['ev']['Pos_P'],
                                           'P_pos_rtp': my_ems_rtp['flexopts']['ev']['Pos_P'],
                                           'P_neg_tou': my_ems_tou['flexopts']['ev']['Neg_P'],
                                           'P_neg_tou_mi': my_ems_tou_mi['flexopts']['ev']['Neg_P'],
                                           'P_neg_const': my_ems_const['flexopts']['ev']['Neg_P'],
                                           'P_neg_const_mi': my_ems_const_mi['flexopts']['ev']['Neg_P'],
                                           'P_neg_rtp': my_ems_rtp['flexopts']['ev']['Neg_P'],
                                           'E_pos_tou': my_ems_tou['flexopts']['ev']['Pos_E'],
                                           'E_pos_tou_mi': my_ems_tou_mi['flexopts']['ev']['Pos_E'],
                                           'E_pos_const': my_ems_const['flexopts']['ev']['Pos_E'],
                                           'E_pos_const_mi': my_ems_const_mi['flexopts']['ev']['Pos_E'],
                                           'E_pos_rtp': my_ems_rtp['flexopts']['ev']['Pos_E'],
                                           'E_neg_tou': my_ems_tou['flexopts']['ev']['Neg_E'],
                                           'E_neg_tou_mi': my_ems_tou_mi['flexopts']['ev']['Neg_E'],
                                           'E_neg_const': my_ems_const['flexopts']['ev']['Neg_E'],
                                           'E_neg_const_mi': my_ems_const_mi['flexopts']['ev']['Neg_E'],
                                           'E_neg_rtp': my_ems_rtp['flexopts']['ev']['Neg_E']
                                           },
                                          index=pd.date_range(start=my_ems_tou_mi['time_data']['time_slots'][0],
                                                              end=my_ems_tou_mi['time_data']['time_slots'][-1],
                                                              freq='15Min'))
            # Optimal charging power addition
            opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_tou_mi'] \
                += opt_result_df['P_ev_opt_tou_mi']
            opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_tou'] \
                += opt_result_df['P_ev_opt_tou']
            opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_const_mi'] \
                += opt_result_df['P_ev_opt_const_mi']
            opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_const'] \
                += opt_result_df['P_ev_opt_const']
            opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_rtp'] \
                += opt_result_df['P_ev_opt_rtp']
            opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'n_veh_avail'] += 1
            # Flexible power addition
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_tou'] \
                += flex_result_df['P_pos_tou']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_tou_mi'] \
                += flex_result_df['P_pos_tou_mi']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_const'] \
                += flex_result_df['P_pos_const']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_const_mi'] \
                += flex_result_df['P_pos_const_mi']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_rtp'] \
                += flex_result_df['P_pos_rtp']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_tou'] \
                += flex_result_df['P_neg_tou']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_tou_mi'] \
                += flex_result_df['P_neg_tou_mi']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_const'] \
                += flex_result_df['P_neg_const']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_const_mi'] \
                += flex_result_df['P_neg_const_mi']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_rtp'] \
                += flex_result_df['P_neg_rtp']
            # Flexible energy addition
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_tou'] \
                += flex_result_df['E_pos_tou']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_tou_mi'] \
                += flex_result_df['E_pos_tou_mi']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_const'] \
                += flex_result_df['E_pos_const']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_const_mi'] \
                += flex_result_df['E_pos_const_mi']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_rtp'] \
                += flex_result_df['E_pos_rtp']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_tou'] \
                += flex_result_df['E_neg_tou']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_tou_mi'] \
                += flex_result_df['E_neg_tou_mi']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_const'] \
                += flex_result_df['E_neg_const']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_const_mi'] \
                += flex_result_df['E_neg_const_mi']
            flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_rtp'] \
                += flex_result_df['E_neg_rtp']

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

        """
        ####################################################################
        # Group optimal and flexible power schedules by daytime ID #########
        ####################################################################
        """
        # Prepare heat map for optimal charging power
        opt_per_daytime = pd.DataFrame()
        opt_per_daytime_temp = opt_sum_df.groupby(by='Daytime_ID').mean()
        opt_per_daytime = opt_per_daytime.append(opt_per_daytime_temp.iloc[96:192, :])
        opt_per_daytime = opt_per_daytime.append(opt_per_daytime_temp.iloc[480:, :])
        opt_per_daytime = opt_per_daytime.append(opt_per_daytime_temp.iloc[384:480, :])
        opt_per_daytime = opt_per_daytime.append(opt_per_daytime_temp.iloc[0:96, :])
        opt_per_daytime = opt_per_daytime.append(opt_per_daytime_temp.iloc[192:384, :])
        opt_per_daytime = opt_per_daytime.reset_index()

        # Calculate weekday and weekend optimal schedule averages per daytime
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
        flex_per_daytime_temp = flex_sum_df.groupby(by='Daytime_ID').mean()
        flex_per_daytime = flex_per_daytime.append(flex_per_daytime_temp.iloc[96:192, :])
        flex_per_daytime = flex_per_daytime.append(flex_per_daytime_temp.iloc[480:, :])
        flex_per_daytime = flex_per_daytime.append(flex_per_daytime_temp.iloc[384:480, :])
        flex_per_daytime = flex_per_daytime.append(flex_per_daytime_temp.iloc[0:96, :])
        flex_per_daytime = flex_per_daytime.append(flex_per_daytime_temp.iloc[192:384, :])
        flex_per_daytime = flex_per_daytime.reset_index()

        # Calculate weekday and weekend flexibility averages per daytime
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

        # Save data to hdf files for further analysis
        opt_per_daytime.to_hdf(output_path + str(power) + '/Aggregated Data/opt_per_daytime_data.h5', mode='w', key='df')
        opt_per_daytime_qt.to_hdf(output_path + str(power) + '/Aggregated Data/opt_per_daytime_qt_data.h5', mode='w', key='df')
        flex_per_daytime.to_hdf(output_path + str(power) + '/Aggregated Data/flex_per_daytime_data.h5', mode='w', key='df')
        weekday_opt_per_daytime.to_hdf(output_path + str(power) + '/Aggregated Data/weekday_opt_per_daytime_data.h5', mode='w', key='df')
        weekend_opt_per_daytime.to_hdf(output_path + str(power) + '/Aggregated Data/weekend_opt_per_daytime_data.h5', mode='w', key='df')
        weekday_flex_per_daytime.to_hdf(output_path + str(power) + '/Aggregated Data/weekday_flex_per_daytime_data.h5', mode='w', key='df')
        weekend_flex_per_daytime.to_hdf(output_path + str(power) + '/Aggregated Data/weekend_flex_per_daytime_data.h5', mode='w', key='df')

        # prepare df for week heat map
        P_pos_tou_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                    columns=days)
        P_pos_const_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                      columns=days)
        P_pos_tou_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                       columns=days)
        P_pos_const_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                         columns=days)
        P_pos_rtp_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                    columns=days)
        P_neg_tou_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                    columns=days)
        P_neg_const_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                      columns=days)
        P_neg_tou_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                       columns=days)
        P_neg_const_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                         columns=days)
        P_neg_rtp_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                    columns=days)
        n_avail_veh_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                      columns=days)

        # Copy power to single day columns
        for i in range(7):
            P_pos_tou_hm[days[i]].iloc[:] = flex_per_daytime['P_pos_sum_tou'].iloc[i * 96:i * 96 + 96].values
            P_pos_const_hm[days[i]].iloc[:] = flex_per_daytime['P_pos_sum_const'].iloc[i * 96:i * 96 + 96].values
            P_pos_tou_mi_hm[days[i]].iloc[:] = flex_per_daytime['P_pos_sum_tou_mi'].iloc[i * 96:i * 96 + 96].values
            P_pos_const_mi_hm[days[i]].iloc[:] = flex_per_daytime['P_pos_sum_const_mi'].iloc[i * 96:i * 96 + 96].values
            P_pos_rtp_hm[days[i]].iloc[:] = flex_per_daytime['P_pos_sum_rtp'].iloc[i * 96:i * 96 + 96].values
            P_neg_tou_hm[days[i]].iloc[:] = flex_per_daytime['P_neg_sum_tou'].iloc[i * 96:i * 96 + 96].values
            P_neg_const_hm[days[i]].iloc[:] = flex_per_daytime['P_neg_sum_const'].iloc[i * 96:i * 96 + 96].values
            P_neg_tou_mi_hm[days[i]].iloc[:] = flex_per_daytime['P_neg_sum_tou_mi'].iloc[i * 96:i * 96 + 96].values
            P_neg_const_mi_hm[days[i]].iloc[:] = flex_per_daytime['P_neg_sum_const_mi'].iloc[i * 96:i * 96 + 96].values
            P_neg_rtp_hm[days[i]].iloc[:] = flex_per_daytime['P_neg_sum_rtp'].iloc[i * 96:i * 96 + 96].values
            n_avail_veh_hm[days[i]].iloc[:] = opt_per_daytime['n_veh_avail'].iloc[i * 96:i * 96 + 96].values

        # Save heat map dataframes to files
        P_pos_tou_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_pos_tou_hm_data.h5', mode='w', key='df')
        P_pos_const_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_pos_const_hm_data.h5', mode='w', key='df')
        P_pos_tou_mi_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_pos_tou_mi_hm_data.h5', mode='w', key='df')
        P_pos_const_mi_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_pos_const_mi_hm_data.h5', mode='w', key='df')
        P_pos_rtp_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_pos_rtp_hm_data.h5', mode='w', key='df')
        P_neg_tou_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_neg_tou_hm_data.h5', mode='w', key='df')
        P_neg_const_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_neg_const_hm_data.h5', mode='w', key='df')
        P_neg_tou_mi_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_neg_tou_mi_hm_data.h5', mode='w', key='df')
        P_neg_const_mi_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_neg_const_mi_hm_data.h5', mode='w', key='df')
        P_neg_rtp_hm.to_hdf(output_path + str(power) + '/Aggregated Data/P_neg_rtp_hm_data.h5', mode='w', key='df')
        n_avail_veh_hm.to_hdf(output_path + str(power) + '/Aggregated Data/n_veh_avail_hm_data.h5', mode='w', key='df')


if __name__ == '__main__':
    # Read veh availabilities from file
    veh_avail = pd.read_csv('../input/chts_veh_availability.csv')
    # Extract a subsample for testing
    veh_avail = veh_avail[68:88]

    aggregate_ev_flex(veh_avail, output_path='../output/')

