import opentumflex
import os


base_dir = os.path.abspath(os.getcwd())
input_file = r'\input\input_data.csv'
output_dir = r'\output'

path_input_data = base_dir + input_file
path_results = base_dir + output_dir

ems = opentumflex.run_scenario(opentumflex.scenario_fromfile,           # Select scenario from scenario.py 
                               path_input=path_input_data,              # Input path
                               path_results=path_results,               # Output path
                               solver='glpk',                           # Select solver
                               time_limit=50,                           # Time limit to solve the optimization
                               save_opt_res=False,                      # Save optimization results
                               show_opt_balance=True,                   # Plot energy balance
                               show_opt_soc=True,                       # Plot optimized SOC plan
                               show_flex_res=True,                      # Show flexibility plots
                               show_aggregated_flex=True,               # Plot aggregated flex
                               show_aggregated_flex_price='bar',        # Plot aggregated price as bar/scatter
                               save_flex_offers=False,                  # Save flexibility offers in comax/alf format
                               convert_input_tocsv=True,                # Save .xlsx file to .csv format
                               troubleshooting=False)                   # Troubleshooting on/off

