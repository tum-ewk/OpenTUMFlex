import opentumflex
import os


base_dir = os.path.abspath(os.getcwd())
input_file = r'\input\input_data.csv'
output_dir = r'\output'

path_input_data = base_dir + input_file
path_results = base_dir + output_dir

ems = opentumflex.run_scenario(opentumflex.scenario_residential_house,
                               path_input=path_input_data, path_results=path_results,
                               fcst_only=True, time_limit=10,
                               show_flex_res=False, show_opt_res=False, save_opt_res=False,
                               convert_input_tocsv=True, show_stacked_flex=False,
                               troubleshooting=False)

