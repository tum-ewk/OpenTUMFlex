"""
The ev_flex_computation_single module calculates the flexibility of a single ev availability.
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
import random

p_charge_max = 3.7                   # Maximal charging power, 11 kW
convert_mile_2_km = 1.60934         # conversion rate of 1.6 km/mile
convert_dist_2_energy = 0.2         # conversion rate of 0.2 kWh/km (20 kWh/100km)

# Define input and output paths
input_path = 'input/'
output_path = 'output/'
# Read vehicle availabilities from file
veh_avail = pd.read_csv(input_path + 'chts_veh_availability.csv')
# Choose random vehicle availability
random_veh_avail = random.choice(list(veh_avail.index))
# random_veh_avail = 3763
# Ceil arrival time to next quarter hour
t_arrival_ceiled = pd.Timestamp(veh_avail['t_arrival'][random_veh_avail]).ceil(freq='15Min')
# Floor departure time to previous quarter hour
t_departure_floored = pd.Timestamp(veh_avail['t_departure'][random_veh_avail]).floor(freq='15Min')
if t_arrival_ceiled >= t_departure_floored:
    print('### Time is not sufficient ###')
else:
    # Get simulated price forecast for given time period
    price_fcst = forecast.simulate_elect_price_fcst(t_start=t_arrival_ceiled, t_end=t_departure_floored, pr_constant=0.19)

    # initialize with basic time settings
    my_ems = opentumflex.initialize_time_setting(t_inval=15,
                                                 start_time=t_arrival_ceiled.strftime('%Y-%m-%d %H:%M'),
                                                 end_time=t_departure_floored.strftime('%Y-%m-%d %H:%M'))
    # Initialize household devices
    opentumflex.initialize_ems(my_ems)
    # Reset all fcst to zero, except electricity prices
    my_ems['fcst'] = {}
    my_ems['fcst']['temp'] = [0] * my_ems['time_data']['nsteps']
    my_ems['fcst']['solar'] = [0] * my_ems['time_data']['nsteps']
    my_ems['fcst']['last_heat'] = [0] * my_ems['time_data']['nsteps']
    my_ems['fcst']['last_elec'] = [0] * my_ems['time_data']['nsteps']
    my_ems['fcst']['ele_price_in'] = price_fcst['RTP'].to_list()
    my_ems['fcst']['gas'] = [0] * my_ems['time_data']['nsteps']
    my_ems['fcst']['ele_price_out'] = [0] * my_ems['time_data']['nsteps']

    # Update EV parameters
    my_ems['devices'].update(opentumflex.devices(device_name='ev', minpow=0, maxpow=p_charge_max,
                                                 stocap=veh_avail['d_travelled'][random_veh_avail] * convert_mile_2_km * convert_dist_2_energy,
                                                 eta=0.98, timesetting=my_ems['time_data'],
                                                 ev_aval=[my_ems['time_data']['start_time'], my_ems['time_data']['end_time']],
                                                 init_soc=[0], end_soc=[100]))

    # create Pyomo model from opentumflex data
    m = opentumflex.create_model(my_ems)

    # solve the optimization problem
    m = opentumflex.solve_model(m, solver='glpk', time_limit=30)

    # extract the results from model and store them in opentumflex['optplan'] dictionary
    my_ems = opentumflex.extract_res(m, my_ems)

    # Calculate ev flexibility
    my_ems = opentumflex.calc_flex_ev(my_ems)

    # Plot flex result
    opentumflex.plot_flex(my_ems, 'ev')
