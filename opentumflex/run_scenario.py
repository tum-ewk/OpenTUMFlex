# new modules
import opentumflex

# general modules
import os


def run_scenario(scenario, path_input, path_results, fcst_only=True, time_limit=30, troubleshooting=True,
                 show_opt_res=True, show_flex_res=True, save_opt_res=True, convert_input_tocsv=True):
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

    # read devices parameters and forecasting data from xlsx or csv file
    my_ems = opentumflex.read_data(my_ems, path_input, fcst_only=fcst_only, to_csv=convert_input_tocsv)

    # modify the opentumflex regarding to predefined scenario
    my_ems = scenario(my_ems)

    # create Pyomo model from opentumflex data
    m = opentumflex.create_model(my_ems)

    # solve the optimization problem
    m = opentumflex.solve_model(m, solver='glpk', time_limit=time_limit, troubleshooting=troubleshooting)

    # extract the results from model and store them in opentumflex['optplan'] dictionary
    my_ems = opentumflex.extract_res(m, my_ems)

    # visualize the optimization results
    if show_opt_res:
        opentumflex.plot_optimal_results(my_ems)
    
    # save the data in .xlsx in given path
    if save_opt_res:    
        opentumflex.save_results(my_ems, path_results)

    # calculate the flexibility
    my_ems = opentumflex.calc_flex_hp(my_ems, reopt=False)
    my_ems = opentumflex.calc_flex_ev(my_ems, reopt=False)
    my_ems = opentumflex.calc_flex_chp(my_ems)
    my_ems = opentumflex.calc_flex_bat(my_ems, reopt=False)
    my_ems = opentumflex.calc_flex_pv(my_ems, reopt=False)

    # plot the results of flexibility calculation
    if show_flex_res:
        opentumflex.plot_flex(my_ems, "hp")
        opentumflex.plot_flex(my_ems, "ev")
        opentumflex.plot_flex(my_ems, "pv")
        opentumflex.plot_flex(my_ems, "bat")
        opentumflex.plot_flex(my_ems, "chp")

    return my_ems


if __name__ == '__main__':

    base_dir = os.path.abspath(os.getcwd())
    input_file = r'\..\input\input_data.csv'
    output_dir = r'\..\results'
    path_input_data = base_dir + input_file
    path_results = base_dir + output_dir

    ems = run_scenario(opentumflex.scenario_hp01, path_input_data, path_results, fcst_only=True, time_limit=10, troubleshooting=True)
