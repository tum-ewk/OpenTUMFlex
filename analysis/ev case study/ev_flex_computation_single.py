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
from ems.ems_mod import update_time_data
from ems.devices.devices import devices
from forecast.price_fcst import get_elect_price_fcst
from ems.optim.opt_test import run_hp_opt as opt
from ems.ems_mod import initialize_devices
from ems.flex.flex_ev import calc_flex_ev
from ems.plot.flex_draw_bar_plot import plot_flex as plot
import os

p_charge_max = 11                   # Maximal charging power

# Define input and output paths
input_path = 'C:/Users/ga47num/PycharmProjects/GER MP - OpenTUMFlex - EV/Input/'
test_input = 'data/input_data.xlsx'

rtp_files = os.listdir(input_path + 'RTP/')
rtp_price_forecast = pd.read_hdf(input_path + 'RTP/' + rtp_files[rtp_files == 'rtp_15min'], key='df')

# Counter for keeping track of insufficient time differences
t_insufficient_count = 0

# Create a list of result ems
results = list()

# Ceil arrival time to next quarter hour
t_arrival_ceiled = pd.Timestamp('2017-12-18 09:30')
# Floor departure time to previous quarter hour
t_departure_floored = pd.Timestamp('2017-12-18 17:00')

# Get price forecast for given time period
price_fcst = get_elect_price_fcst(t_start=t_arrival_ceiled, t_end=t_departure_floored, pr_constant=0.19)
price_fcst.insert(value=rtp_price_forecast['price'].loc[t_arrival_ceiled:t_departure_floored], loc=0, column='RTP')
price_fcst = price_fcst.drop(columns={'Random', 'EPEX'})

# Initial time settings
my_ems = {'time_data': {}}
my_ems['time_data']['t_inval'] = 15
my_ems['time_data']['d_inval'] = 15
my_ems['time_data']['start_time'] = '2017-12-18 09:30'
my_ems['time_data']['end_time'] = '2017-12-18 17:00'
my_ems['time_data']['days'] = 1
my_ems.update(update_time_data(my_ems))
# Initialize household devices
initialize_devices(my_ems)
my_ems['fcst'] = {}
my_ems['fcst']['temp'] = [0] * my_ems['time_data']['nsteps']
my_ems['fcst']['solar'] = [0] * my_ems['time_data']['nsteps']
my_ems['fcst']['last_heat'] = [0] * my_ems['time_data']['nsteps']
my_ems['fcst']['last_elec'] = [0] * my_ems['time_data']['nsteps']
my_ems['fcst']['ele_price_in'] = price_fcst['RTP'].to_list()
my_ems['fcst']['gas'] = [0] * my_ems['time_data']['nsteps']
my_ems['fcst']['ele_price_out'] = [0] * my_ems['time_data']['nsteps']


# Update EV parameters
my_ems['devices'].update(devices(device_name='ev', minpow=0, maxpow=p_charge_max,
                                 stocap=60, eta=0.98, timesetting=my_ems['time_data'],
                                 ev_aval=[my_ems['time_data']['start_time'], my_ems['time_data']['end_time']],
                                 init_soc=[0], end_soc=[100]))

# calculate the timetable for all the devices
my_ems['optplan'] = opt(my_ems, plot_fig=False, result_folder='data/')

# Calculate ev flexibility
my_ems['flexopts']['ev'] = calc_flex_ev(my_ems)

# Plot flex result
plot(my_ems, 'ev')
