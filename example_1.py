import opentumflex
import os


base_dir = os.path.abspath(os.getcwd())
input_file = r'\input\input_data.csv'
output_dir = r'\output'

path_input_data = base_dir + input_file
path_results = base_dir + output_dir

ems = opentumflex.run_scenario(opentumflex.scenario_apartment, path_input_data, path_results, fcst_only=True, time_limit=10,
                               show_flex_res=False, show_opt_res=True, save_opt_res=False, convert_input_tocsv=True,
                               troubleshooting=False)
