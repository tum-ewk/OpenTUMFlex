"""
This script computes all results and plots concerning the flexibility potential of EV that were published in the paper
"Quantifying the Flexibility of Electric Vehicles in Germany and California – A Case Study".
"""

__author__ = "Michel Zadé"
__copyright__ = "2020 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "1.0"
__maintainer__ = "Michel Zadé"
__email__ = "michel.zade@tum.de"
__status__ = "Complete"

from joblib import Parallel, delayed
from tqdm import tqdm
import multiprocessing
import pandas as pd
import itertools
import analysis.ev_case_study as ev_case_study
import os
import json

# Define input and output paths
output_path = 'yourfolder/output/'
input_path = 'yourfolder/input/'
figure_path = 'yourfolder/figures/'
rtp_input_path = 'yourfolder/input/RTP/'
# Read veh availabilities from file - check for delimiter type before and specify if semicolon (, sep=';')
veh_availabilities = pd.read_csv('yourfolder/input/some_availability.csv')

print('1. Prepare input data.')

# Extract a subsample for testing
veh_availabilities = veh_availabilities[:]
veh_availabilities = veh_availabilities.reset_index()

# Define case study details
params = {'power_levels': [3.7, 11, 22],
          'pricing': ['ToU', 'Constant', 'Con_mi', 'ToU_mi', 'RTP'],
          'veh_availability': veh_availabilities.values.tolist()}

# Create output folder
ev_case_study.create_output_folder(output_path=output_path,
                                   power_levels=params['power_levels'],
                                   pricing_strategies=params['pricing'])
# Create empty figures folder
ev_case_study.create_figures_folder(figure_folder_path=figure_path)

# Create all possible combinations of params
keys = list(params)
param_variations = list()
param_con = {'conversion_km_2_kwh': 0.2,
             'rtp_input_data_path': rtp_input_path,
             'output_path': output_path,
             'pricing_strategies': ['ToU', 'Constant', 'Con_mi', 'ToU_mi', 'RTP'],
             'plotting': False,
             'info': False}
for values in itertools.product(*map(params.get, keys)):
    # Store in list
    param_variations.append(list(values))

print('2. Calculate flexibility offers.')

# Run flex calculation in parallel
Parallel(n_jobs=int(multiprocessing.cpu_count()))(
    delayed(ev_case_study.calc_ev_flex_offers_parallel)(i, param_con) for i in tqdm(param_variations))

print('3. Aggregate optimal charging schedules, costs, and flexibility offers.')

# Aggregate single offers
ylim_dict = ev_case_study.aggregate_ev_flex(veh_availabilities,
                                            output_path=output_path,
                                            rtp_input_data_path=rtp_input_path)
# save y-limits dictionary to file
with open(figure_path + 'y_limits.txt', 'w') as ylims:
    json.dump(ylim_dict, ylims)

#%%
print('4. Plot results.')

# optional: read ylim-dict from file if wanting to execute step '4.' alone
# with open(figure_path + 'y_limits.txt') as ylims:
#     data = ylims.read()
#     ylim_dict = json.loads(data)

# Plot number of available vehicles at home over a week (only for one power level, since it won't change)
ev_case_study.plot_n_avail_veh(output_path=output_path + str(params['power_levels'][0]) + '/',
                               figure_path=figure_path)

# Plot aggregated flexibility offers in a heat map
ev_case_study.plot_flex_heatmap(output_path=output_path, figure_path=figure_path)

# List all power levels - sorted from low to high
power_levels = sorted(os.listdir(output_path), key=float)
# df for overall costs
overall_costs = pd.DataFrame(columns=power_levels, index=params['pricing'])
for power in power_levels:
    # Read and sum up overall costs from aggregated files
    overall_costs[power]['ToU'] = pd.read_hdf(output_path + str(power) + '/Aggregated Data/opt_sum_data.h5')['c_tou_energy'].sum()
    overall_costs[power]['ToU_mi'] = pd.read_hdf(output_path + str(power) + '/Aggregated Data/opt_sum_data.h5')['c_tou_mi_energy'].sum()
    overall_costs[power]['Constant'] = pd.read_hdf(output_path + str(power) + '/Aggregated Data/opt_sum_data.h5')['c_con_energy'].sum()
    overall_costs[power]['Con_mi'] = pd.read_hdf(output_path + str(power) + '/Aggregated Data/opt_sum_data.h5')['c_con_mi_energy'].sum()
    overall_costs[power]['RTP'] = pd.read_hdf(output_path + str(power) + '/Aggregated Data/opt_sum_data.h5')['c_rtp_energy'].sum()
    # Plot aggregated flexibility offers over time
    ev_case_study.plot_opt_flex_timeseries(power, output_path=output_path + str(power) + '/', figure_path=figure_path)
    # Plot flex prices over time
    ev_case_study.plot_flex_prices(power, output_path=output_path + str(power) + '/', figure_path=figure_path, ylims=ylim_dict, results='case_study')

# Plot overall cost
ev_case_study.plot_overall_cost(overall_costs=overall_costs, figure_path=figure_path)
