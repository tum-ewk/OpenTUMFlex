"""
opentumflex:

A linear optimisation and flexibility calculation model for residential premises.
opentumflex optimizes the operation of a certain device configuration
based on cost and weather forecasts, mobility, heat and electricity demand in the form of time series.
Furthermore, the model calculates and prices the flexibility potential of different household devices
(e.g. heat pumps, electric vehicles, photovoltaic systems etc.).
"""

from .devices.devices import device_write, devices
from .flex.flex_ev import calc_flex_ev
from .flex.flex_bat import calc_flex_bat
from .flex.flex_pv import calc_flex_pv
from .flex.flex_hp import calc_flex_hp
from .flex.flex_chp import calc_flex_chp
from .optim.opt import run_opt
from .optim.reoptim import reflex_hp, reflex_ev, reflex_bat, reoptimize, reflex_pv
from .plot.flex_draw import plot_flex
from .plot.reopt_draw import plot_reopt, plot_reopt_compare, plot_reopt_price
