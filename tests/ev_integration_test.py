
import pandas as pd
import numpy as np
import multiprocessing
import matplotlib.pyplot as plt
from joblib import Parallel, delayed

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

        #plot(my_ems, "ev")

    except Exception as e:
        print(e)
        print('--- EV capacity =', ev_cap, 'kWh')
        print('--- P_max =', p_max, 'kW')
        print('--- T_start, T_end =', ev_aval)
        print('--- SOC start =', init_soc)
        print('--- SOC end =', end_soc)
        if (end_soc-init_soc)*ev_cap/100 > p_max*((pd.to_datetime(ev_aval[1]) - pd.to_datetime(ev_aval[0])).seconds/3600):
            print('Desired charging of', str((end_soc-init_soc)*ev_cap/100),
                  'is not possible in given time. Max charging is',
                  str(p_max*((pd.to_datetime(ev_aval[1]) - pd.to_datetime(ev_aval[0])).seconds/3600)))
        pass

    return my_ems, success


def run_hems_samples(sample):
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
    my_ems['devices'].update(devices(device_name='hp', minpow=0, maxpow=2))
    my_ems['devices']['sto']['stocap'] = 0
    my_ems['devices']['boiler']['maxpow'] = 20
    my_ems['devices']['chp']['maxpow'] = 5
    my_ems['devices']['pv']['maxpow'] = 0
    my_ems['devices']['bat']['stocap'] = 0
    my_ems['devices']['bat']['maxpow'] = 0
    my_ems['devices'].update(devices(device_name='ev', stocap=sample[0], maxpow=sample[1], minpow=0,
                                     end_soc=sample[3], init_soc=sample[4], ev_aval=sample[5], eta=sample[6],
                                     timesetting=my_ems['time_data']))

    # Optimize device schedules
    my_ems['optplan'] = opt(my_ems, plot_fig=False, result_folder='data/')

    # Calculate ev flexibility
    my_ems['flexopts']['ev'] = calc_flex_ev(my_ems)

    success = True

    return my_ems, success


def plot_results(ems_results):
    # Plot flexibility results
    for i in range(len(ems_results)):
        plot(ems_results[i], 'ev')


def random_ev_sample_generator(n_samples=1):
    samples = list()

    ev_cap_range = np.arange(start=10, stop=100, step=10)         # ev capacity range
    p_ev_max_range = np.arange(start=5, stop=30, step=5)          # ev maximal charging power range
    p_ev_min_range = np.arange(start=1, stop=10, step=1)          # ev minimal charging power range
    soc_end_range = np.arange(start=50, stop=100, step=5)         # ev desired end soc range
    soc_start_range = np.arange(start=0, stop=50, step=5)         # ev initial soc range
    t_plugin_range = pd.date_range(start='2020-1-1 00:00', end='2020-1-1 9:00', freq='30Min')   # initial plug-in time range
    t_plugout_range = pd.date_range(start='2020-1-1 15:00', end='2020-1-1 23:59', freq='30Min')    # final plug-out time range
    eff_range = np.arange(start=95, stop=100, step=1) / 100

    while len(samples) < n_samples:
        ev_cap = np.random.choice(ev_cap_range)
        p_ev_max = np.random.choice(p_ev_max_range)
        p_ev_min = np.random.choice(p_ev_min_range)
        soc_end = np.random.choice(soc_end_range)
        soc_start = np.random.choice(soc_start_range)
        eff = np.random.choice(eff_range)
        ev_availability = [t_plugin_range[round(np.random.random()*len(t_plugin_range))-1].strftime('%Y-%m-%d %H:%M'),
                           t_plugout_range[round(np.random.random()*len(t_plugout_range))-1].strftime('%Y-%m-%d %H:%M')]

        # Check whether desired energy can be charged in given time period
        if (soc_end - soc_start) * ev_cap / 100 > p_ev_max * (
                (pd.to_datetime(ev_availability[1]) - pd.to_datetime(ev_availability[0])).seconds / 3600):
            # print('Charging not possible in given time. Reduce desired charging energy.')
            pass
        else:
            samples.append([ev_cap, p_ev_max, p_ev_min, [soc_end], [soc_start], ev_availability, eff])

    return samples


if __name__ == '__main__':
    results = list()

    # Create sample results
    ev_samples = random_ev_sample_generator(n_samples=50)

    # # Run hems with multiple ev_samples
    # for i in range(len(ev_samples)):
    #     print('###########################  HEMS iteration #', i, '  ###########################')
    #     my_ems, success = run_hems_samples(ev_samples[i])
    #     if success:
    #         print('Successful HEMS Operation')
    #         results.append(my_ems)

    # Run hems on multiple cores
    results_multi = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(run_hems_samples)(i) for i in ev_samples)
    # Extract multiprocessing results
    for i in range(len(results_multi)):
        results.append(results_multi[i][0])

    # # Run hems manually
    # my_ems, success = run_hems(ev_cap=50, p_max=5, p_min=0, ev_aval=["2020-1-1 4:00", "2020-1-1 18:00"], end_soc=[80], init_soc=[40])
    # #my_ems, success = run_hems()


    # # Plot results
    # plot_results(results)


