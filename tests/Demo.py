
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# import ems and devices modules
from ems.ems_mod import ems as ems_loc
from ems.ems_mod import ems_write
from ems.ems_mod import update_time_data
from ems.devices.devices import devices
from ems.devices.devices import device_write

# import forecast model for weather and price data
from forecast.fcst import load_data

# import optimization module
from ems.optim.opt_test import run_hp_opt as opt

# import flex devices modules
from ems.flex.flexhp import calc_flex_hp
from ems.flex.flexchp import calc_flex_chp
from ems.flex.flex_ev import calc_flex_ev
from ems.flex.Bat import Batflex
from ems.flex.PV import PVflex
from ems.flex.flex_ev import calc_flex_ev

# import plot module
from ems.plot.flex_draw import plot_flex as plot
from ems.plot.flex_draw import save_results

Demo_Nr = 3
# Demo 1: EV 8 kW 40 kWwh
# Demo 2: HP 5 kW  heat storage 40 kWh
# Demo 3: CHP 4 kW  heat storage 150 kWh
# Demo 4: PV  2.4 kWp
# Demo 5: Bat 10kWh


if Demo_Nr == 1:
    # load the predefined ems data, initialization by user input is also possible:
    my_ems = ems_loc(initialize=True, path='data/test_Nr_01.txt')

    # change the time interval
    my_ems['time_data']['t_inval'] = 30
    my_ems['time_data']['d_inval'] = 15
    my_ems['time_data']['start_time'] = '2019-12-18 00:00'
    my_ems['time_data']['end_time'] = '2019-12-18 23:59'
    my_ems['time_data']['days'] = 1
    my_ems.update(update_time_data(my_ems))

    # load the weather and price data
    my_ems['fcst'] = load_data(my_ems, path=r"../forecast/Testdata/Eingangsdaten_hp.xlsx")

    # add or change the utility/devices
    my_ems['devices'].update(devices(device_name='hp', minpow=0, maxpow=0))
    my_ems['devices']['sto']['stocap'] = 0
    my_ems['devices']['boiler']['maxpow'] = 20
    my_ems['devices']['chp']['maxpow'] = 0
    my_ems['devices']['pv']['maxpow'] = 0
    my_ems['devices']['bat']['stocap'] = 0
    my_ems['devices']['bat']['maxpow'] = 0
    my_ems['devices'].update(devices(device_name='ev', minpow=0, maxpow=8, stocap=40, init_soc=[5, 15],
                                     end_soc=[60, 70], eta=0.98,
                                     ev_aval=["2019-12-18 0:00", "2019-12-18 9:00",
                                              "2019-12-18 19:00", "2019-12-18 23:59"],
                                     # ev_aval=["2019-12-18 4:00", "2019-12-18 9:00"],
                                     timesetting=my_ems['time_data']))

    # calculate the timetable for all the devices
    my_ems['optplan'] = opt(my_ems, plot_fig=True, result_folder='data/')

    # calculate the flexibility of one device

    my_ems['flexopts']['ev'] = calc_flex_ev(my_ems)

    # plot the results#

    plot(my_ems, "ev")
    # ems_write(my_ems, path='data/test_Nr_02.txt')
    # store the data of the whole ems for reuse

if Demo_Nr == 2:
    # load the predefined ems data, initialization by user input is also possible:
    my_ems = ems_loc(initialize=True, path='data/test_Nr_01.txt')

    # change the time interval
    my_ems['time_data']['t_inval'] = 15
    my_ems['time_data']['d_inval'] = 15
    my_ems['time_data']['start_time'] = '2019-12-18 00:00'
    my_ems['time_data']['end_time'] = '2019-12-18 23:59'
    my_ems['time_data']['days'] = 1
    my_ems.update(update_time_data(my_ems))

    # load the weather and price data
    my_ems['fcst'] = load_data(my_ems, path=r"../forecast/Testdata/Eingangsdaten_hp.xlsx")

    # add or change the utility/devices
    # if deleting one specific device please use del my_ems['devices']['hp']
    # my_ems['devices'].update(dev(device_name='hp', minpow=3, maxpow=6))
    my_ems['devices'].update(devices(device_name='hp', minpow=0, maxpow=5))
    my_ems['devices']['sto']['stocap'] = 40
    my_ems['devices']['boiler']['maxpow'] = 0
    my_ems['devices']['chp']['maxpow'] = 0
    my_ems['devices']['pv']['maxpow'] = 0
    my_ems['devices']['bat']['stocap'] = 0
    my_ems['devices']['bat']['maxpow'] = 0
    my_ems['devices'].update(devices(device_name='ev', minpow=0, maxpow=0, stocap=0, init_soc=[5, 15],
                                     end_soc=[60, 70], eta=0.98,
                                     ev_aval=["2019-12-18 0:00", "2019-12-18 9:00",
                                              "2019-12-18 19:00", "2019-12-18 23:59"],
                                     # ev_aval=["2019-12-18 4:00", "2019-12-18 9:00"],
                                     timesetting=my_ems['time_data']))


    # calculate the timetable for all the devices
    my_ems['optplan'] = opt(my_ems, plot_fig=True, result_folder='data/')

    # calculate the flexibility of one device
    my_ems['flexopts']['hp'] = calc_flex_hp(my_ems)

    # plot the results#

    plot(my_ems, "hp")
    # ems_write(my_ems, path='data/test_Nr_02.txt')
    # store the data of the whole ems for reuse


if Demo_Nr == 3:
    # load the predefined ems data, initialization by user input is also possible:
    my_ems = ems_loc(initialize=True, path='data/test_Nr_01.txt')

    # change the time interval
    my_ems['time_data']['t_inval'] = 15
    my_ems['time_data']['d_inval'] = 15
    my_ems['time_data']['start_time'] = '2019-12-18 00:00'
    my_ems['time_data']['end_time'] = '2019-12-18 23:59'
    my_ems['time_data']['days'] = 1
    my_ems.update(update_time_data(my_ems))

    # load the weather and price data
    my_ems['fcst'] = load_data(my_ems, path=r"../forecast/Testdata/Eingangsdaten_hp.xlsx")

    # add or change the utility/devices
    # if deleting one specific device please use del my_ems['devices']['hp']
    # my_ems['devices'].update(dev(device_name='hp', minpow=3, maxpow=6))
    my_ems['devices'].update(devices(device_name='hp', minpow=0, maxpow=0))
    my_ems['devices']['sto']['stocap'] = 150
    my_ems['devices']['boiler']['maxpow'] = 10
    my_ems['devices']['chp']['maxpow'] = 4
    my_ems['devices']['pv']['maxpow'] = 0
    my_ems['devices']['bat']['stocap'] = 0
    my_ems['devices']['bat']['maxpow'] = 0
    my_ems['devices'].update(devices(device_name='ev', minpow=0, maxpow=0, stocap=0, init_soc=[5, 15],
                                     end_soc=[60, 70], eta=0.98,
                                     ev_aval=["2019-12-18 0:00", "2019-12-18 9:00",
                                              "2019-12-18 19:00", "2019-12-18 23:59"],
                                     # ev_aval=["2019-12-18 4:00", "2019-12-18 9:00"],
                                     timesetting=my_ems['time_data']))


    # calculate the timetable for all the devices
    my_ems['optplan'] = opt(my_ems, plot_fig=True, result_folder='data/')

    # calculate the flexibility of one device
    my_ems['flexopts']['chp'] = calc_flex_chp(my_ems)

    # plot the results#

    plot(my_ems, "chp")
    # ems_write(my_ems, path='data/test_Nr_02.txt')
    # store the data of the whole ems for reuse


if Demo_Nr == 4:
    # load the predefined ems data, initialization by user input is also possible:
    my_ems = ems_loc(initialize=True, path='data/test_Nr_01.txt')

    # change the time interval
    my_ems['time_data']['t_inval'] = 15
    my_ems['time_data']['d_inval'] = 15
    my_ems['time_data']['start_time'] = '2019-12-18 00:00'
    my_ems['time_data']['end_time'] = '2019-12-18 23:59'
    my_ems['time_data']['days'] = 1
    my_ems.update(update_time_data(my_ems))

    # load the weather and price data
    my_ems['fcst'] = load_data(my_ems, path=r"../forecast/Testdata/Eingangsdaten_hp.xlsx")

    # add or change the utility/devices
    # if deleting one specific device please use del my_ems['devices']['hp']
    # my_ems['devices'].update(dev(device_name='hp', minpow=3, maxpow=6))
    my_ems['devices'].update(devices(device_name='hp', minpow=0, maxpow=0))
    my_ems['devices']['sto']['stocap'] = 25
    my_ems['devices']['boiler']['maxpow'] = 20
    my_ems['devices']['chp']['maxpow'] = 0
    my_ems['devices']['pv']['maxpow'] = 8
    my_ems['devices']['bat']['stocap'] = 0
    my_ems['devices']['bat']['maxpow'] = 0
    my_ems['devices'].update(devices(device_name='ev', minpow=0, maxpow=0, stocap=0, init_soc=[5, 15],
                                     end_soc=[60, 70], eta=0.98,
                                     ev_aval=["2019-12-18 0:00", "2019-12-18 9:00",
                                              "2019-12-18 19:00", "2019-12-18 23:59"],
                                     # ev_aval=["2019-12-18 4:00", "2019-12-18 9:00"],
                                     timesetting=my_ems['time_data']))


    # calculate the timetable for all the devices
    my_ems['optplan'] = opt(my_ems, plot_fig=True, result_folder='data/')

    # calculate the flexibility of one device
    my_ems['flexopts']['pv'] = PVflex(my_ems)

    # plot the results#

    plot(my_ems, "pv")
    # ems_write(my_ems, path='data/test_Nr_02.txt')
    # store the data of the whole ems for reuse



if Demo_Nr == 5:
    # load the predefined ems data, initialization by user input is also possible:
    my_ems = ems_loc(initialize=True, path='data/test_Nr_01.txt')

    # change the time interval
    my_ems['time_data']['t_inval'] = 15
    my_ems['time_data']['d_inval'] = 15
    my_ems['time_data']['start_time'] = '2019-12-18 00:00'
    my_ems['time_data']['end_time'] = '2019-12-18 23:59'
    my_ems['time_data']['days'] = 1
    my_ems.update(update_time_data(my_ems))

    # load the weather and price data
    my_ems['fcst'] = load_data(my_ems, path=r"../forecast/Testdata/Eingangsdaten_hp.xlsx")

    # add or change the utility/devices
    # if deleting one specific device please use del my_ems['devices']['hp']
    # my_ems['devices'].update(dev(device_name='hp', minpow=3, maxpow=6))
    my_ems['devices'].update(devices(device_name='hp', minpow=0, maxpow=0))
    my_ems['devices']['sto']['stocap'] = 25
    my_ems['devices']['boiler']['maxpow'] = 20
    my_ems['devices']['chp']['maxpow'] = 0
    my_ems['devices']['pv']['maxpow'] = 0
    my_ems['devices']['bat']['stocap'] = 10
    my_ems['devices']['bat']['maxpow'] = 10
    my_ems['devices'].update(devices(device_name='ev', minpow=0, maxpow=0, stocap=0, init_soc=[5, 15],
                                     end_soc=[60, 70], eta=0.98,
                                     ev_aval=["2019-12-18 0:00", "2019-12-18 9:00",
                                              "2019-12-18 19:00", "2019-12-18 23:59"],
                                     # ev_aval=["2019-12-18 4:00", "2019-12-18 9:00"],
                                     timesetting=my_ems['time_data']))


    # calculate the timetable for all the devices
    my_ems['optplan'] = opt(my_ems, plot_fig=True, result_folder='data/')

    # calculate the flexibility of one device
    my_ems['flexopts']['bat'] = Batflex(my_ems)

    # plot the results#

    plot(my_ems, "bat")
    # ems_write(my_ems, path='data/test_Nr_02.txt')
    # store the data of the whole ems for reuse