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
import multiprocessing
import pandas as pd
import itertools
import analysis.ev_case_study as ev_case_study

# Define input and output paths
output_path = 'output/'
input_path = 'input/'
figure_path = 'figures/'
rtp_input_path = '../analysis/input/RTP/'
# Read veh availabilities from file
veh_availabilities = pd.read_csv('input/chts_veh_availability.csv')
# Extract a subsample for testing
veh_availabilities = veh_availabilities[:20]
veh_availabilities = veh_availabilities.reset_index()

# Define case study details
params = {'power': [3.7, 11, 22],
          'pricing': ['ToU', 'Constant', 'Con_mi', 'ToU_mi', 'RTP'],
          'veh_availability': veh_availabilities.values.tolist()}

# Create output folder
ev_case_study.create_output_folder(output_path=output_path,
                                   power_levels=params['power'],
                                   pricing_strategies=params['pricing'])

# Create all possible combinations of params
keys = list(params)
param_variations = list()
param_con = {'conversion_distance_2_km': 1.61,
             'conversion_km_2_kwh': 0.2,
             'rtp_input_data_path': rtp_input_path,
             'output_path': output_path,
             'pricing_strategies': ['ToU', 'Constant', 'Con_mi', 'ToU_mi', 'RTP'],
             'plotting': False}
for values in itertools.product(*map(params.get, keys)):
    # Store in list
    param_variations.append(list(values))

# Run flex calculation in parallel
Parallel(n_jobs=int(multiprocessing.cpu_count()))(
    delayed(ev_case_study.calc_ev_flex_offers_parallel)(i, param_con) for i in param_variations)

# Aggregate single offers
ev_case_study.aggregate_ev_flex(veh_availabilities,
                                output_path=output_path,
                                rtp_input_data_path=rtp_input_path)

# Plot number of available vehicles at home over a week (only for one power level, since it won't change)
ev_case_study.plot_n_avail_veh(output_path=output_path + str(params['power'][0]) + '/',
                               figure_path=figure_path)

# Plot aggregated flexibility offers over time
for power in params['power']:
    ev_case_study.plot_opt_flex_timeseries(output_path=output_path + str(power) + '/', figure_path=figure_path)

# Plot aggregated flexibility offers in a heat map
ev_case_study.plot_flex_heatmap(output_path=output_path)

# Calculate overall costs of optimal charging
overall_cost = ev_case_study.calc_overall_cost(output_path=output_path)

# Plot overall cost
ev_case_study.plot_overall_cost(overall_cost, figure_path=figure_path)
