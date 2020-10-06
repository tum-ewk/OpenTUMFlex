"""
opentumflex:

A linear optimisation and flexibility calculation model for residential premises.
opentumflex optimizes the operation of a certain device configuration
based on cost and weather forecasts, mobility, heat and electricity demand in the form of time series.
Furthermore, the model calculates and prices the flexibility potential of different household devices
(e.g. heat pumps, electric vehicles, photovoltaic systems etc.).
"""

from opentumflex.configuration.devices import save_device, create_device
from opentumflex.configuration.set_time import initialize_time_setting
from opentumflex.configuration.init_ems import save_ems, init_ems_js, read_data, read_forecast, \
    read_properties, update_time_data
from opentumflex.flexibility.flex_hp import calc_flex_hp
from opentumflex.flexibility.flex_pv import calc_flex_pv
from opentumflex.flexibility.flex_chp import calc_flex_chp
from opentumflex.flexibility.flex_bat import calc_flex_bat
from opentumflex.flexibility.flex_ev import calc_flex_ev
from opentumflex.market_communication.generate_market_offers import save_offers_alf, save_offers_comax
from opentumflex.optimization.report import save_results
from opentumflex.optimization.model import create_model, solve_model, extract_res
# from opentumflex.market_communication.handle_market_call import calc_flex_response_bat, calc_flex_response_ev, calc_flex_response_pv, \
#     calc_flex_response_hp
from opentumflex.plot.plot_optimal_results import plot_optimal_results
from opentumflex.plot.plot_flex_reoptimized import plot_cumm_energy_reoptimized, plot_flex_reoptimized, \
    plot_compare_optim_reoptim
from opentumflex.plot.plot_flex import plot_flex
from opentumflex.scenarios.scenarios import *
from .run_scenario import run_scenario

