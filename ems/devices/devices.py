"""
devices module will  document the device parameters (general and specific for each device). All the data will
be sorted in an adequate serving other modules like optplan and flexopts.
"""

import pandas as pd
import json as js
import numpy as np
import datetime


def devices(device_name, minpow=0, maxpow=0, stocap=None, eta=None, init_soc=None, end_soc=None, ev_aval=None,
            timesetting=96, sto_volume=0, path=None):
    # define general unit parameters
    unit = {'minpow': minpow,
            'maxpow': maxpow,
            'stocap': stocap,
            'initSOC': init_soc,
            'eta': eta
            }

    # use case for heat pump
    if device_name == 'hp':

        # if no predefined device data is available:
        if path is None:
            # typical heat pump power map
            temp_supply = [288.15, 318.15, 333.15]
            hp_q = pd.DataFrame({'266.15': [4.8, 4.8, 4.8],
                                 '275.15': [6.0, 6.0, 6.0],
                                 '280.15': [7.5, 7.5, 7.5],
                                 '288.15': [9.2, 9.2, 9.2],
                                 '293.15': [9.9, 9.9, 9.9],
                                 }, index=temp_supply
                                )

            hp_p = pd.DataFrame({'266.15': [1.9, 1.9, 1.9],
                                 '275.15': [2.1, 2.1, 2.1],
                                 '280.15': [2.3, 2.3, 2.3],
                                 '288.15': [2.5, 2.5, 2.5],
                                 '293.15': [2.6, 2.6, 2.6],
                                 }, index=temp_supply
                                )

            hp_cop = hp_q.div(hp_p)
            fact_p = maxpow / hp_p.mean(axis=0)[1]

            # change the DataFrame to Dict
            unit.update({'maxpow': hp_p.multiply(fact_p).to_dict('dict'), 'COP': hp_cop.to_dict('dict')})
            df_unit_hp = unit
            dict_unit_hp = {device_name: df_unit_hp}

        # load the device parameters directly from local data
        else:
            with open(path) as f:
                dict_hp = js.load(f)
            dict_unit_hp = {device_name: dict_hp}
        return dict_unit_hp

    # use case for electric vehicle
    elif device_name == 'ev':

        if path is None:

            # convert the data formats
            _ev_aval_date = ev_aval
            aval_time_init = ev_aval[::2]
            aval_time_end = ev_aval[1::2]
            # convert time string to datetime
            _ev_aval = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M') for x in _ev_aval_date]
            # calculate how many pairs of charging start and end time
            _points = int(len(_ev_aval) / 2)
            _timesteps = timesetting['nsteps']
            # how many time steps it has in one hour
            ntsteps = timesetting['ntsteps']

            # create aval with the same length of time steps
            # if aval[i] == 1 means availability is True

            aval = np.zeros(_timesteps)

            # arrays for inital and end soc check
            # for each time steps the real soc should be lower than init_soc_check and bigger than end_soc_check
            init_soc_check = np.zeros(_timesteps) + 100
            end_soc_check = np.zeros(_timesteps)

            # consum array for eventually energy consumption of EV
            consum = np.zeros(_timesteps)
            # node is the time steps indx between one availability end and the next availability start
            node = np.zeros((_points - 1) * 2)
            # start_time is the first time step for the optimization
            start_time = datetime.datetime.strptime(timesetting['start_time'], '%Y-%m-%d %H:%M')

            idx = 0
            for i in range(_points):

                # obtain the start and end time step index
                _aval_start = int((_ev_aval[idx] - start_time).seconds / 3600 * ntsteps)
                _aval_end = int((_ev_aval[idx + 1] - start_time).seconds / 3600 * ntsteps - 1)
                # change them to 1
                aval[_aval_start:_aval_end + 1] = 1
                # for the first time step the init_soc_check isn't needed, otherwise it should be same as init_soc[i]
                if _aval_start == 0:
                    pass
                else:
                    init_soc_check[_aval_start - 1] = init_soc[i]

                # end_soc_check should be kept for possible time steps
                end_soc_check[_aval_end] = end_soc[i]
                # after last end_soc index the constrain should keep until last time step
                if i == _points - 1:
                    end_soc_check[_aval_end:] = end_soc[i]
                # loop for every two points in availability array
                idx = idx + 2

            idx = 0

            # some procedure to obatin the nodes for the periods when the EV is not available
            for j in range(_points - 1):
                _aval_end = int((_ev_aval[idx + 1] - start_time).seconds / 3600 * ntsteps)
                _aval_start = int((_ev_aval[idx + 2] - start_time).seconds / 3600 * ntsteps)
                node[idx] = _aval_end
                node[idx + 1] = _aval_start - 1
                consum[_aval_end:_aval_start] = (end_soc[j] - init_soc[j + 1]) / 100 * stocap / \
                                                (_aval_start - _aval_end)
                idx = idx + 2

            # add new elements in the general dict for EV
            unit.update({'endSOC': end_soc,
                         'aval': list(aval),
                         'aval_init': list(aval_time_init),
                         'aval_end': list(aval_time_end),
                         'init_soc_check': list(init_soc_check),
                         'end_soc_check': list(end_soc_check),
                         'node': list(node)})

            df_unit_ev = unit
            dict_unit_ev = {device_name: df_unit_ev}

        # initialize EV from local file
        else:
            with open(path) as f:
                dict_ev = js.load(f)
            dict_unit_ev = {device_name: dict_ev}

        return dict_unit_ev

    # use case for heat storage
    elif device_name == 'sto':

        if path is None:
            # min/max temperature
            temp_min = 18
            temp_max = 50
            # if stocap not given, it can be calculated based on the temperature constrains
            if stocap is None:
                stocap = sto_volume * 0.997 * 4.186 * (temp_max - temp_min) / 3600

            unit.update({'stocap': stocap, 'mintemp': temp_min, 'maxtemp': temp_max, 'self_discharge': 0.005})
            df_unit_sto = unit
            dict_unit_sto = {device_name: df_unit_sto}

        else:
            with open(path) as f:
                dict_sto = js.load(f)

            dict_unit_sto = {device_name: dict_sto}

        return dict_unit_sto

    # for other situations: battery, chp, pv
    else:

        if path is None:

            dict_unit = {device_name: unit}

        else:
            with open(path) as f:
                dict_unit_import = js.load(f)

            dict_unit = {device_name: dict_unit_import}

        return dict_unit


def device_write(dict_ems, device_name, path):
    # write parameters of other devices in js file
    device_unit = dict_ems['devices'][device_name]

    # open the file and write in the data
    with open(path, 'w') as f:
        js.dump(device_unit, f)


if __name__ == '__main__':
    ev_aval_date = ["10:00", "14:00", "17:45", "19:15", "21:30", "23:15"]
    ev_aval = [datetime.datetime.strptime(x, "%H:%M") for x in ev_aval_date]
    points = int(len(ev_aval) / 2)
    xx = ev_aval[1] - ev_aval[0]
    a = xx.seconds / 3600

    # timesteps = 96
    # aval = np.zeros(timesteps)
    #
    # idx = 0
    # for i in range(points):
    #     aval_start = int(ev_aval[idx].hour * 4 + ev_aval[idx].minute / 15)
    #     aval_end = int(ev_aval[idx + 1].hour * 4 + ev_aval[idx + 1].minute / 15 - 1)
    #     aval[aval_start:aval_end + 1] = 1
    #     idx = idx + 2

    # count = raw_input('Number of variables:')
# for i in my_ems1['devices'].keys():
#     exec('var_' + str(i) + ' = ' + str(my_ems1['devices'][i]))

# device_write(my_ems1, 'bat', path='C:/Users/ge57vam/emsflex/ems/bat01_ems.txt')
