import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from ems.ems_mod import ems as ems_loc

# Prepare memory variables for analysis
results = list()
result_names = list()

# List all files in a directory using os.listdir
basepath = 'C:/Users/ga47num/PycharmProjects/OpenTUMFlexPy/tests/results/CHTS/ToU/'
for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)):
        result_names.append(entry)
        # print(entry)

# read all results and save them in memory
for result_name in result_names:
    my_ems = ems_loc(initialize=True, path='results/CHTS/ToU/' + result_name)
    results.append(my_ems)
    # print(result_name)

"""
Create a date range of min to maximal time
"""
# find minimal and maximal time
t_min = pd.Timestamp(results[0]['time_data']['time_slots'][0])
t_max = pd.Timestamp(results[0]['time_data']['time_slots'][-1])

# Go through all results and update minimal and maximal time
for i in range(len(results)):
    if pd.Timestamp(results[i]['time_data']['time_slots'][0]) < t_min:
        t_min = pd.Timestamp(results[i]['time_data']['time_slots'][0])
    if pd.Timestamp(results[i]['time_data']['time_slots'][-1]) > t_max:
        t_max = pd.Timestamp(results[i]['time_data']['time_slots'][-1])

# print(t_min)
# print(t_max)

# Date range from minimal to maximal time
t_range = pd.date_range(start=t_min, end=t_max, freq='15Min')
# Create df for sum of optimal charging plans
p_opt_chts_sum = pd.DataFrame(0, index=t_range, columns={'P_ev_opt_sum'})


"""
Analysis of optimal charging plan
"""
for i in range(len(results)):
    opt_result_df = pd.DataFrame(results[i]['optplan']['EV_power'],
                                 columns={'P_ev_opt'},
                                 index=pd.date_range(start=results[i]['time_data']['time_slots'][0],
                                                     end=results[i]['time_data']['time_slots'][-1], freq='15Min'))

    p_opt_chts_sum.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum'] += opt_result_df['P_ev_opt']


# Plot optimal charging power over time
p_opt_chts_sum.plot()

"""
Analysis of ev flexibility
"""