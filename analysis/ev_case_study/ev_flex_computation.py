"""
The ev_flex_computation module calculates the flexibility of a list of vehicle availabilities .
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
import opentumflex
import forecast
from pathlib import Path


def calc_ev_flex_offers(veh_availabilities,
                        output_path='output/',
                        power_levels=[3.7, 11, 22],
                        pricing_strategies={'ToU', 'Constant', 'Con_mi', 'ToU_mi', 'RTP'},
                        conversion_distance_2_km=1.61,
                        conversion_km_2_kwh = 0.2,
                        plotting=False):
    """
    This function iteratively calculates the flexibility of each vehicle availability for every power level and pricing strategy.

    :param veh_availabilities: vehicle availabilities consisting of arrival and departure times, distance travelled
    :param output_path: path where output shall be stored
    :param power_levels: charging power levels
    :param pricing_strategies: pricing strategies for simulations
    :param conversion_distance_2_km: conversion rate, e.g. 1 mile = 1.61 km
    :param conversion_km_2_kwh: conversion rate from km to kwh
    :param plotting: plotting parameter, default is False
    :return: None
    """

    # Create output folder
    Path(output_path).mkdir(parents=True, exist_ok=True)

    # Total number of home availabilities with trips conducted before and afterwards
    n_avail = len(veh_availabilities)
    n_veh = len(veh_availabilities['vehID'].unique())

    # initialize with basic time settings
    my_ems = opentumflex.initialize_time_setting(t_inval=15,
                                                 start_time='2012-01-01 00:00',
                                                 end_time='2012-01-01 23:00')

    # Initialize household devices
    opentumflex.initialize_ems(my_ems)
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
        price_fcst = forecast.simulate_elect_price_fcst(t_start=t_arrival_ceiled,
                                                        t_end=t_departure_floored,
                                                        pr_constant=0.19,
                                                        pricing=pricing_strategies)
        # Go through all price strategies
        for price in price_fcst.columns:
            # Go through all power levels
            for power in power_levels:
                print('Pricing: ' + price + ' and Power: ' + str(power))
                # Create subfolder for different power levels
                Path(output_path + str(power)).mkdir(parents=True, exist_ok=True)
                # Create subfolders for different pricing strategies
                Path(output_path + str(power) + '/' + price).mkdir(parents=True, exist_ok=True)
                # Update forecast data
                my_ems['fcst']['ele_price_in'] = price_fcst[price].to_list()

                # Update EV parameters
                my_ems['devices'].update(opentumflex.devices(device_name='ev', minpow=0, maxpow=power,
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
                m = opentumflex.solve_model(m, solver='glpk', time_limit=30)

                # extract the results from model and store them in opentumflex['optplan'] dictionary
                my_ems = opentumflex.extract_res(m, my_ems)

                # Calculate ev flexibility
                my_ems = opentumflex.calc_flex_ev(my_ems)

                # Plot flex result
                if plotting == True:
                    opentumflex.plot_flex(my_ems, 'ev')

                # Save results to files
                opentumflex.ems_write(my_ems, path=output_path + str(power) + '/' + price + '/ev_avail_' + str(i) + '.txt')


if __name__ == '__main__':

    # Read veh availabilities from file
    veh_availabilities = pd.read_csv('input/chts_veh_availability.csv')
    # Extract a subsample for testing
    veh_availabilities = veh_availabilities[0:20]

    calc_ev_flex_offers(veh_availabilities,
                        output_path='output/',
                        power_levels=[3.7, 11, 22],
                        pricing_strategies={'ToU', 'Constant', 'Con_mi', 'ToU_mi', 'RTP'},
                        conversion_distance_2_km=1.61,
                        conversion_km_2_kwh=0.2,
                        plotting=False)

