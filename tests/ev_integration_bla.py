
import pandas as pd
import numpy as np
import multiprocessing
import matplotlib.pyplot as plt

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

# import plot module
from ems.plot.flex_draw import plot_flex as plot
from ems.plot.flex_draw import save_results


def run_hems(ev_cap=60, p_max=20, p_min=0, init_soc=[10], end_soc=[80], eta=0.98, ev_aval=["2020-1-1 4:00", "2020-1-1 18:00"]):
    # load the predefined ems data, initialization by user input is also possible:
    my_ems = ems_loc(initialize=True, path='data/test_Nr_01.txt')

    # change the time interval
    my_ems['time_data']['t_inval'] = 15
    my_ems['time_data']['d_inval'] = 15
    my_ems['time_data']['start_time'] = '2020-1-1 00:00'
    my_ems['time_data']['end_time'] = '2020-1-1 23:59'
    my_ems['time_data']['days'] = 1
    my_ems.update(update_time_data(my_ems))

    # load the weather and price data
    my_ems['fcst'] = load_data(my_ems)
    my_ems['devices'].update(devices(device_name='hp', minpow=0, maxpow=0))
    my_ems['devices']['sto']['stocap'] = 0
    my_ems['devices']['boiler']['maxpow'] = 20
    my_ems['devices']['chp']['maxpow'] = 5
    my_ems['devices']['pv']['maxpow'] = 0
    my_ems['devices']['bat']['stocap'] = 0
    my_ems['devices']['bat']['maxpow'] = 0
    my_ems['devices'].update(devices(device_name='ev', minpow=p_min, maxpow=p_max, stocap=ev_cap, init_soc=init_soc,
                                     end_soc=end_soc, eta=eta, ev_aval=ev_aval, timesetting=my_ems['time_data']))

    success = False

    try:
        # calculate the timetable for all the devices
        my_ems['optplan'] = opt(my_ems, plot_fig=False, result_folder='data/')

        # calculate the flexibility of one device
        my_ems['flexopts']['ev'] = calc_flex_ev(my_ems)

        success = True

        plot(my_ems, "ev")

    except Exception as e:
        print(e)
        print('--- EV capacity =', c, 'kWh')
        print('--- P_max =', p, 'kW')
        print('--- T_start, T_end =', ev_availability)
        print('--- SOC start =', soc_s)
        print('--- SOC end =', soc_e)
        if (soc_e-soc_s)*c/100 > p*((pd.to_datetime(ev_availability[1]) - pd.to_datetime(ev_availability[0])).seconds/3600):
            print('Desired charging of', str((soc_e-soc_s)*c/100), 'is not possible in given time. Max charging is', str(p*((pd.to_datetime(ev_availability[1]) - pd.to_datetime(ev_availability[0])).seconds/3600)))
        pass

    return my_ems, success


if __name__ == '__main__':

    cap_ev = np.arange(start=10, stop=100, step=10)
    p_max = np.arange(start=1, stop=10, step=1)
    soc_end = np.arange(start=50, stop=100, step=5)
    soc_start = np.arange(start=0, stop=50, step=5)
    date_start = pd.date_range(start='2020-1-1 00:00', end='2020-1-1 9:00', freq='30Min')
    date_end = pd.date_range(start='2020-1-1 15:00', end='2020-1-1 23:59', freq='30Min')

    results = list()

    for i in range(25):
        n_ev_avail = 1
        t_end = date_end
        t_start = np.random.choice(date_start)
        c = np.random.choice(cap_ev)
        p = np.random.choice(p_max)
        soc_e = np.random.choice(soc_end)
        soc_s = np.random.choice(soc_start)
        ev_availability = [date_start[round(np.random.random()*len(date_start))-1].strftime('%Y-%m-%d %H:%M'),
                           date_end[round(np.random.random()*len(date_end))-1].strftime('%Y-%m-%d %H:%M')]

        my_ems, success = run_hems(ev_cap=c, p_max=p, ev_aval=ev_availability, end_soc=[soc_e], init_soc=[soc_s])
        # my_ems, success = run_hems()
        if success:
            results.append(my_ems)


