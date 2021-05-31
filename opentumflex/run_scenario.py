"""
The "run_scenarios.py" execute all the functional modules within opentumflex folder including initialization,
optimization, flexibility calculation...
"""

__author__ = "Zhengjie You"
__copyright__ = "2020 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "1.0"
__maintainer__ = "Zhengjie You"
__email__ = "zhengjie.you@tum.de"
__status__ = "Development"

# new modules
import opentumflex

# general modules
import os


def run_scenario(scenario, path_input, path_results, solver='glpk', time_limit=30, troubleshooting=True,
                 show_opt_balance=True, show_opt_soc=True, show_flex_res=True,
                 save_opt_res=True, show_aggregated_flex=True, save_flex_offers=False,
                 convert_input_tocsv=True, show_aggregated_flex_price='bar'):
    """ run an OpenTUMFlex model for given scenario

    Args:
        - scenario: predefined scenario function which will modify the parameters in opentumflex dictionary to create
          a certain scenario
        - path_input: path of input file which can be used to read devices parameters and forecasting data
        - path_results: path to be saved in for results of the optimization
        - fcst_only: if true, read_data() will only read forecasting data from input file, otherwise it will also read
          device parameters
        - time_limit: determine the maximum duration of optimization in seconds

    Returns:
        opentumflex dictionary with optimization results and flexibility offers

    """

    # initialize with basic time settings
    my_ems = opentumflex.initialize_time_setting(t_inval=15, start_time='2019-12-18 00:00', end_time='2019-12-18 23:45')

    if scenario == opentumflex.scenario_fromfile:
        # read devices parameters and forecasting data from xlsx or csv file
        my_ems = opentumflex.read_data(my_ems, path_input, fcst_only=False, to_csv=convert_input_tocsv)
    else:
        # read only the input time series from the excel table
        my_ems = opentumflex.read_data(my_ems, path_input, fcst_only=True, to_csv=convert_input_tocsv)
        # modify the opentumflex regarding to predefined scenario
        my_ems = scenario(my_ems)

    # create Pyomo model from opentumflex data
    m = opentumflex.create_model(my_ems)

    # solve the optimization problem
    m = opentumflex.solve_model(m, solver=solver, time_limit=time_limit, troubleshooting=troubleshooting)

    # extract the results from model and store them in opentumflex['optplan'] dictionary
    my_ems = opentumflex.extract_res(m, my_ems)

    # visualize the optimization results
    opentumflex.plot_optimal_results(my_ems, show_balance=show_opt_balance, show_soc=show_opt_soc)

    # save the data in .xlsx in given path
    if save_opt_res:
        opentumflex.save_results(my_ems, path_results)

    # calculate the flexibility
    # create a group of all flex calculators
    calc_flex = {opentumflex.calc_flex_hp: 'hp',
                 opentumflex.calc_flex_ev: 'ev',
                 opentumflex.calc_flex_chp: 'chp',
                 opentumflex.calc_flex_bat: 'bat',
                 opentumflex.calc_flex_pv: 'pv'}

    # iterate through all the flexibility functions
    for function, device_name in calc_flex.items():
        if my_ems['devices'][device_name]['maxpow'] != 0:
            function(my_ems, reopt=False)

    # plot the results of flexibility calculation
    if show_flex_res:
        for device_name in calc_flex.values():
            if my_ems['devices'][device_name]['maxpow'] != 0:
                opentumflex.plot_flex(my_ems, device_name)
                
    # plot stacked flexibility of all devices
    if show_aggregated_flex:
        opentumflex.plot_aggregated_flex_power(my_ems)
        opentumflex.plot_aggregated_flex_price(my_ems, plot_flexpr=show_aggregated_flex_price)    

    # save flex offers
    if save_flex_offers:
        opentumflex.save_offers(my_ems, market='comax')
    
    return my_ems


if __name__ == '__main__':
    base_dir = os.path.abspath(os.getcwd())
    input_file = r'\..\input\input_data.csv'
    output_dir = r'\..\results'
    path_input_data = base_dir + input_file
    path_results = base_dir + output_dir

    ems = run_scenario(opentumflex.scenario_apartment,
                       path_input=path_input_data, path_results=path_results,
                       fcst_only=True, time_limit=10,
                       show_flex_res=True, show_opt_res=True, save_opt_res=False,
                       convert_input_tocsv=True, show_aggregated_flex=True, 
                       show_aggregated_flex_price='bar', troubleshooting=False)
