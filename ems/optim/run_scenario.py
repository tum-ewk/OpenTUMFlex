# new modules
from model import create_model
from model import solve_model
from model import extract_res
from plot import plot_results
from report import save_results
from ems_function import initialize_time_setting
from scenarios import scenario_hp01

# old modules
from ems.flex.flexhp import calc_flex_hp
from ems.init_ems import read_data
from ems.plot.flex_draw import plot_flex
# general modules
import os


def run_scenario(scenario, path_input, path_results, fcst_only=True, time_limit=30):
    """ run an OpenTUMFlex model for given scenario

    Args:
        - scenario: predefined scenario function which will modify the parameters in ems dictionary to create
          a certain scenario
        - path_input: path of input file which can be used to read devices parameters and forecasting data
        - path_results: path to be saved in for results of the optimization
        - fcst_only: if true, read_data() will only read forecasting data from input file, otherwise it will also read
          device parameters
        - time_limit: determine the maximum duration of optimization in seconds

    Returns:
        ems dictionary with optimization results and flexibility offers

    """

    # initialize with basic time settings
    my_ems = initialize_time_setting(t_inval=15, start_time='2019-12-18 00:00', end_time='2019-12-18 23:45')

    # read devices parameters and forecasting data from xlsx or csv file
    my_ems = read_data(my_ems, path_input, fcst_only=fcst_only, to_csv=True)

    # modify the ems regarding to predefined scenario
    my_ems = scenario(my_ems)

    # create Pyomo model from ems data
    m = create_model(my_ems)

    # solve the optimization problem
    m = solve_model(m, solver='glpk', time_limit=time_limit)

    # extract the results from model and store them in ems['optplan'] dictionary
    my_ems = extract_res(m, my_ems)

    # visualize the optimization results
    plot_results(my_ems)

    # save the data in .xlsx in given path
    save_results(my_ems, path_results)

    # calculate the flexibility of heat pump
    my_ems = calc_flex_hp(my_ems, reopt=False)

    # plot the results of flexibility calculation
    plot_flex(my_ems, "hp")

    return my_ems


if __name__ == '__main__':

    base_dir = os.path.abspath(os.getcwd())
    sub_dir = r'..\..\tests\data\input_data.csv'
    path_input_data = os.path.join(base_dir, sub_dir)
    path_results = os.path.join(base_dir, r'..\..\tests\data')

    ems = run_scenario(scenario_hp01, path_input_data, path_results, fcst_only=True, time_limit=10)
