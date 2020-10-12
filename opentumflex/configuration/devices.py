"""
The "devices.py" module can initialize devices with default or customized parameters
"""

__author__ = "Zhengjie You"
__copyright__ = "2020 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "1.0"
__maintainer__ = "Zhengjie You"
__email__ = "zhengjie.you@tum.de"
__status__ = "Development"

import pandas as pd
import json as js
import numpy as np
import datetime
from scipy.interpolate import UnivariateSpline


def create_device(device_name, minpow=0, maxpow=0, stocap=0, eta=1, init_soc=20, end_soc=40, ev_aval=None,
                  supply_temp=45, timesetting=None, sto_volume=0, path=None):
    """ create_device will create one of five devices (hp, chp, ev, pv, bat) based on user input or json file

    :param device_name: name of the device, e.g. hp, chp, ev...
    :param minpow: minimum power
    :param maxpow: maximum power
    :param stocap: capacity of heat storage, battery or ev
    :param eta: efficiency
    :param init_soc: initial state of charge
    :param end_soc:  end state of charge
    :param ev_aval: availability of ev
    :param supply_temp: supply temperature of hp
    :param timesetting: time settings same as the ones of the ems object
    :param sto_volume: the heat capacity of heat storage calculated by the storage volume (if stocap is None)
    :param path: path of the json file which initialize the device by saved data instead of user input
    :return: dictionary filled with parameters of one device
    """

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
            # supply temperature series
            temp_supply = [288.15, 308.15, 318.15, 328.15, 333.15]

            # thermal power map according to supply and ambient temperature
            hp_q = pd.DataFrame({'266.15': [6, 5.2, 4.8, 4.2, 3.9],
                                 '275.15': [7.5, 6.5, 6.0, 5.3, 5.0],
                                 '280.15': [9.0, 8.0, 7.5, 6.8, 6.5],
                                 '288.15': [10.7, 9.7, 9.2, 8.4, 8.0],
                                 '293.15': [11.7, 10.5, 9.9, 9.2, 8.9],
                                 }, index=temp_supply
                                )
            # electric power map according to supply and ambient temperature
            hp_p = pd.DataFrame({'266.15': [1.5, 1.8, 1.9, 2.0, 2.1],
                                 '275.15': [1.6, 1.9, 2.1, 2.1, 2.1],
                                 '280.15': [1.6, 2.0, 2.3, 2.4, 2.4],
                                 '288.15': [1.7, 2.1, 2.5, 2.7, 2.8],
                                 '293.15': [1.8, 2.2, 2.6, 2.9, 3.0],
                                 }, index=temp_supply
                                )

            # calculate and add new thermal and electric power data for heat pump under the supply temperature by input
            def modify_hp_data(data_original, temperature):
                temp_data = data_original
                value = np.zeros(temp_data.shape[1])
                for _col_num in range(temp_data.shape[1]):
                    spline = UnivariateSpline(list(map(float, temp_data.index.values)),
                                              list(temp_data.iloc[:, _col_num]))
                    value[_col_num] = spline(temperature).item(0)
                temp_data.loc[temperature] = value
                return temp_data.sort_index()

            # modify the power map of HP by user input
            supply_temp = supply_temp + 273.15  # convert from grad celsius to kelvin
            hp_q = modify_hp_data(hp_q, supply_temp)
            hp_p = modify_hp_data(hp_p, supply_temp)
            hp_cop = hp_q.div(hp_p)  # calculate the COP
            fact_p = maxpow / hp_p.loc[supply_temp, '275.15']  # obtain the scaling factor

            # change the DataFrame to Dict
            unit.update({'powmap': hp_p.multiply(fact_p).to_dict('dict'),
                         'maxpow': maxpow,
                         'COP': hp_cop.to_dict('dict'),
                         'supply_temp': supply_temp,
                         'thermInertia': 50, 'minTemp': 20, 'maxTemp': 26, 'heatgain': 0.1})
            df_unit_hp = unit
            dict_unit_hp = {device_name: df_unit_hp}

        # load the device parameters directly from local data if it is available
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

            # modify the availability formats and prepare init_soc_check/end_soc_check time series
            idx = 0
            for i in range(_points):
                # obtain the start and end time step index
                timedelta_start = _ev_aval[idx] - start_time
                timedelta_end = _ev_aval[idx + 1] - start_time
                _aval_start = int((timedelta_start.seconds / 3600 + timedelta_start.days * 24) * ntsteps)
                _aval_end = int((timedelta_end.seconds / 3600 + timedelta_end.days * 24) * ntsteps - 1)
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
                timedelta_end = _ev_aval[idx + 1] - start_time
                timedelta_start = _ev_aval[idx + 2] - start_time
                _aval_end = int((timedelta_end.seconds / 3600 + timedelta_end.days * 24) * ntsteps)
                _aval_start = int((timedelta_start.seconds / 3600 + timedelta_start.days * 24) * ntsteps)
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

    # Update device: PV
    elif device_name == 'pv':
        df_unit_pv = {"maxpow": maxpow,
                      "minpow": minpow,
                      "eta": eta}
        dict_pv = {device_name: df_unit_pv}
        return dict_pv

    # Update device: Bat
    elif device_name == 'bat':
        df_unit_bat = unit
        dict_bat = {device_name: df_unit_bat}
        return dict_bat

    # for other situations: battery, chp, pv
    else:

        if path is None:

            dict_unit = {device_name: unit}

        else:
            with open(path) as f:
                dict_unit_import = js.load(f)

            dict_unit = {device_name: dict_unit_import}

        return dict_unit


def save_device(ems, device_name, path):
    """ save the device parameters data into json file

    :param ems: ems object
    :param device_name: name of the device, e.g. hp, chp, ev...
    :param path: path in which the json file is to be saved
    :return: None
    """

    # write parameters of other devices in js file
    device_unit = ems['devices'][device_name]

    # open the file and write in the data
    with open(path, 'w') as f:
        js.dump(device_unit, f)
