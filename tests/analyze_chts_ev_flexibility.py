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
    print(result_name)
