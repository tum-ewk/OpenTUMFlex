import opentumflex
import os


base_dir = os.path.abspath(os.getcwd())
input_file = r'\input\input_data.xlsx'
output_dir = r'\output'

path_input_data = base_dir + input_file
path_results = base_dir + output_dir

ems = opentumflex.run_scenario(opentumflex.scenario_customized,
                               path_input=path_input_data, path_results=path_results,
                               solver='glpk', time_limit=50,
                               show_flex_res=False, save_opt_res=False,
                               convert_input_tocsv=True, show_aggregated_flex=False,
                               show_aggregated_flex_price='bar', troubleshooting=False)