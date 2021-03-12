"""
The ev_flex_computation module calculates the flexibility of a list of vehicle availabilities.
"""

__author__ = "Michel Zadé"
__copyright__ = "2020 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "1.0"
__maintainer__ = "Michel Zadé"
__email__ = "michel.zade@tum.de"
__status__ = "Development"

from joblib import Parallel, delayed
import multiprocessing
import pandas as pd
import opentumflex
import forecast
import itertools


def calc_ev_flex_offers(veh_availabilities,
                        rtp_input_data_path='../analysis/input/RTP/',
                        output_path='output/',
                        power_levels=[3.7, 11, 22],
                        pricing_strategies={'ToU', 'Constant', 'Con_mi', 'ToU_mi', 'RTP'},
                        conversion_distance_2_km=1.61,
                        conversion_km_2_kwh=0.2,
                        plotting=False):
    """
    This function iteratively calculates the flexibility of each vehicle availability for every power level
    and pricing strategy.

    :param veh_availabilities: vehicle availabilities consisting of arrival and departure times, distance travelled
    :param output_path: path where output shall be stored
    :param rtp_input_data_path: real time prices input file in h5 format
    :param power_levels: charging power levels
    :param pricing_strategies: pricing strategies for simulations
    :param conversion_distance_2_km: conversion rate, e.g. 1 mile = 1.61 km
    :param conversion_km_2_kwh: conversion rate from km to kwh
    :param plotting: plotting parameter, default is False
    :return: None
    """

    # initialize with basic time settings
    my_ems = opentumflex.initialize_time_setting(t_inval=15,
                                                 start_time='2012-01-01 00:00',
                                                 end_time='2012-01-01 23:00')

    # Reset forecasts
    my_ems['fcst'] = {}

    # Counter for keeping track of insufficient time differences
    t_insufficient_count = 0

    # Go through all vehicle availabilities
    for i in range(len(veh_availabilities)):
        print('################# Vehicle availability #' + str(i) + ' #################')
        # Ceil arrival time to next quarter hour
        t_arrival_ceiled = pd.Timestamp(veh_availabilities['t_arrival'][i]).ceil(freq='15Min')
        # Floor departure time to previous quarter hour
        t_departure_floored = pd.Timestamp(veh_availabilities['t_departure'][i]).floor(freq='15Min')
        # Check whether time between ceiled arrival and floored departure time are at least two time steps
        if t_arrival_ceiled >= t_departure_floored:
            print('### Time is not sufficient for timestep:', i, '###')
            t_insufficient_count += 1
            continue

        # change the time interval
        my_ems['time_data']['start_time'] = t_arrival_ceiled.strftime('%Y-%m-%d %H:%M')
        my_ems['time_data']['end_time'] = t_departure_floored.strftime('%Y-%m-%d %H:%M')
        my_ems.update(opentumflex.update_time_data(my_ems))
        my_ems['fcst']['temp'] = [0] * my_ems['time_data']['nsteps']
        my_ems['fcst']['solar'] = [0] * my_ems['time_data']['nsteps']
        my_ems['fcst']['last_heat'] = [0] * my_ems['time_data']['nsteps']
        my_ems['fcst']['last_elec'] = [0] * my_ems['time_data']['nsteps']
        my_ems['fcst']['gas'] = [0] * my_ems['time_data']['nsteps']
        my_ems['fcst']['ele_price_out'] = [0] * my_ems['time_data']['nsteps']

        # Get simulated price forecast for given time period
        price_fcst = forecast.simulate_elect_price_fcst(rtp_input_data_path=rtp_input_data_path,
                                                        t_start=t_arrival_ceiled,
                                                        t_end=t_departure_floored,
                                                        pr_constant=0.19,
                                                        pricing=pricing_strategies)
        # Go through all price strategies
        for price in price_fcst.columns:
            # Go through all power levels
            for power in power_levels:
                print('#' + str(i) + ': Power=' + str(power) + ' Pricing=' + price)
                # Update forecast data
                my_ems['fcst']['ele_price_in'] = price_fcst[price].to_list()

                # Update EV parameters
                my_ems['devices'].update(opentumflex.create_device(device_name='ev', minpow=0, maxpow=power,
                                                                   stocap=round(veh_availabilities['d_travelled'][i] *
                                                                                conversion_distance_2_km *
                                                                                conversion_km_2_kwh),
                                                                   init_soc=[0], end_soc=[100], eta=0.98,
                                                                   ev_aval=[my_ems['time_data']['start_time'],
                                                                            my_ems['time_data']['end_time']],
                                                                   timesetting=my_ems['time_data']))

                # create Pyomo model from opentumflex data
                m = opentumflex.create_model(my_ems)

                # solve the optimization problem
                m = opentumflex.solve_model(m, solver='glpk', time_limit=30, troubleshooting=False)

                # extract the results from model and store them in opentumflex['optplan'] dictionary
                my_ems = opentumflex.extract_res(m, my_ems)

                # Calculate ev flexibility
                my_ems = opentumflex.calc_flex_ev(my_ems)

                # Plot flex result
                if plotting:
                    opentumflex.plot_flex(my_ems, 'ev')

                # Save results to files
                opentumflex.save_ems(my_ems, path=output_path + str(power) + '/' + price + '/ev_avail_' + str(i) + '.txt')


def calc_ev_flex_offers_parallel(param_variation,
                                 param_fix):
    """
    This function calculates the flexibility of each vehicle availability for a specific power level & pricing strategy.

    :param param_variation: parameter variation as a list containing charging power (float), pricing strategy (string)
                            and vehicle availability (list)
    :param param_fix: fix parameters consisting of 'conversion_distance_2_km', 'conversion_km_2_kwh', 'rtp_input_data_path',
                      'output_path', 'pricing_strategies', 'plotting'
    :return: None
    """

    # initialize with basic time settings
    my_ems = opentumflex.initialize_time_setting(t_inval=15,
                                                 start_time='2012-01-01 00:00',
                                                 end_time='2012-01-01 23:00')

    # Reset forecasts
    my_ems['fcst'] = {}

    # Ceil arrival time to next quarter hour
    t_arrival_ceiled = pd.Timestamp(param_variation[2][4]).ceil(freq='15Min')
    # Floor departure time to previous quarter hour
    t_departure_floored = pd.Timestamp(param_variation[2][5]).floor(freq='15Min')
    # Check whether time between ceiled arrival and floored departure time are at least two time steps
    if t_arrival_ceiled >= t_departure_floored:
        if param_fix['info']:
            print('#' + str(param_variation[2][0]) + ': Time not sufficient.')
        return
    else:
        if param_fix['info']:
            print('#' + str(param_variation[2][0]) + ': Power=' + str(param_variation[0]) + ' Pricing=' + param_variation[1])

    # change the time interval
    my_ems['time_data']['start_time'] = t_arrival_ceiled.strftime('%Y-%m-%d %H:%M')
    my_ems['time_data']['end_time'] = t_departure_floored.strftime('%Y-%m-%d %H:%M')
    my_ems.update(opentumflex.update_time_data(my_ems))
    my_ems['fcst']['temperature'] = [0] * my_ems['time_data']['nsteps']
    my_ems['fcst']['solar_power'] = [0] * my_ems['time_data']['nsteps']
    my_ems['fcst']['load_heat'] = [0] * my_ems['time_data']['nsteps']
    my_ems['fcst']['load_elec'] = [0] * my_ems['time_data']['nsteps']
    my_ems['fcst']['gas_price'] = [0] * my_ems['time_data']['nsteps']
    my_ems['fcst']['ele_price_out'] = [0] * my_ems['time_data']['nsteps']

    # Get simulated price forecast for given time period
    price_fcst = forecast.simulate_elect_price_fcst(rtp_input_data_path=param_fix['rtp_input_data_path'],
                                                    t_start=t_arrival_ceiled,
                                                    t_end=t_departure_floored,
                                                    pr_constant=0.19,
                                                    pricing=param_fix['pricing_strategies'])

    # Update forecast data
    my_ems['fcst']['ele_price_in'] = price_fcst[param_variation[1]].to_list()

    # Update EV parameters
    my_ems['devices'].update(opentumflex.create_device(device_name='ev', minpow=0, maxpow=param_variation[0],
                                                       stocap=round(param_variation[2][2] *
                                                                    param_fix['conversion_distance_2_km'] *
                                                                    param_fix['conversion_km_2_kwh']),
                                                       init_soc=[0], end_soc=[100], eta=0.98,
                                                       ev_aval=[my_ems['time_data']['start_time'],
                                                                my_ems['time_data']['end_time']],
                                                       timesetting=my_ems['time_data']))

    # create Pyomo model from opentumflex data
    m = opentumflex.create_model(my_ems)

    # solve the optimization problem
    m = opentumflex.solve_model(m, solver='glpk', time_limit=30, troubleshooting=False)

    # extract the results from model and store them in opentumflex['optplan'] dictionary
    my_ems = opentumflex.extract_res(m, my_ems)

    # Calculate ev flexibility
    my_ems = opentumflex.calc_flex_ev(my_ems)

    # Plot flex result
    if param_fix['plotting']:
        opentumflex.plot_flex(my_ems, 'ev')


    if param_fix['save_ems_object_as_json']:
        # Save results to files
        opentumflex.save_ems(my_ems, path=param_fix['output_path'] + str(param_variation[0]) + '/' +
                                          param_variation[1] + '/ev_avail_' + str(param_variation[2][0]) + '.txt')
    '''
    if param_fix['save_ev_flex_as_feather']:
        my_ems['flexopts']['ev'].reset_index().to_feather(path=param_fix['output_path'] + str(param_variation[0]) + '/' +
                                                 param_variation[1] + '/ev_avail_' + str(param_variation[2][0]) + '.ft')
                                                 
        https://towardsdatascience.com/the-best-format-to-save-pandas-data-414dca023e0d
    '''

if __name__ == '__main__':
    # Read veh availabilities from file
    veh_avail = pd.read_csv('../input/chts_veh_availability.csv')
    # Extract a subsample for testing
    veh_avail = veh_avail[68:88]
    veh_avail = veh_avail.reset_index()

    # Make case study definitions
    power_levels = [3.7, 11, 22]
    pricing_strategies = ['ToU', 'Constant', 'Con_mi', 'ToU_mi', 'RTP']

    calc_ev_flex_offers(veh_avail,
                        rtp_input_data_path='../input/RTP/',
                        output_path='../output/',
                        power_levels=power_levels,
                        pricing_strategies=pricing_strategies,
                        conversion_distance_2_km=1.61,
                        conversion_km_2_kwh=0.2,
                        plotting=False)


    # Define case study details
    params = {'power': power_levels,
              'pricing': pricing_strategies,
              'veh_availability': veh_avail.values.tolist()}

    # Create all possible combinations of params
    keys = list(params)
    param_variations = list()
    param_con = {'conversion_distance_2_km': 1.61,
                 'conversion_km_2_kwh': 0.2,
                 'rtp_input_data_path': 'C:/Users/ga47num/PycharmProjects/OpenTUMFlexPy/analysis/input/RTP/',
                 'output_path': 'C:/Users/ga47num/PycharmProjects/OpenTUMFlexPy/analysis/output/',
                 'pricing_strategies': ['ToU', 'Constant', 'Con_mi', 'ToU_mi', 'RTP'],
                 'plotting': False,
                 'save_ev_flex_as_feather': True,
                 'save_ems_object_as_json': False}
    for values in itertools.product(*map(params.get, keys)):
        # Store in list
        param_variations.append(list(values))

    # Run flex calculation in parallel
    Parallel(n_jobs=int(multiprocessing.cpu_count()))(delayed(calc_ev_flex_offers_parallel)(i, param_con) for i in param_variations)
