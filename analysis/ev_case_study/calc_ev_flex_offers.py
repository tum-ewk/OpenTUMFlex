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


def calc_ev_flex_offers_parallel(param_variation,
                                 param_fix):
    """
    This function calculates the flexibility of each vehicle availability for a specific power level & pricing strategy.

    :param param_variation: parameter variation as a list containing charging power (float), pricing strategy (string)
                            and vehicle availability (list)
    :param param_fix: fix parameters consisting of 'conversion_km_2_kwh', 'rtp_input_data_path',
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
    if t_departure_floored - t_arrival_ceiled < pd.Timedelta(minutes=2*my_ems['time_data']['t_inval']):
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

    # Save results to files
    opentumflex.save_ems(my_ems, path=param_fix['output_path'] + str(param_variation[0]) + '/' +
                                      param_variation[1] + '/ev_avail_' + str(param_variation[2][0]) + '.txt')


if __name__ == '__main__':
    # Read veh availabilities from file
    veh_avail = pd.read_csv('../input/chts_veh_availability.csv')
    # Extract a subsample for testing
    veh_avail = veh_avail[:]
    veh_avail = veh_avail.reset_index()

    # Make case study definitions
    power_levels = [3.7, 11, 22]
    pricing_strategies = ['ToU', 'Constant', 'Con_mi', 'ToU_mi', 'RTP']

    # Define case study details
    params = {'power': power_levels,
              'pricing': pricing_strategies,
              'veh_availability': veh_avail.values.tolist()}

    # Create all possible combinations of params
    keys = list(params)
    param_variations = list()
    param_con = {'conversion_km_2_kwh': 0.2,
                 'rtp_input_data_path': '../input/RTP/',
                 'output_path': '../output/',
                 'pricing_strategies': ['ToU', 'Constant', 'Con_mi', 'ToU_mi', 'RTP'],
                 'plotting': False,
                 'info': False}
    for values in itertools.product(*map(params.get, keys)):
        # Store in list
        param_variations.append(list(values))

    # Run flex calculation in parallel
    Parallel(n_jobs=int(multiprocessing.cpu_count()))(delayed(calc_ev_flex_offers_parallel)(i, param_con) for i in param_variations)
