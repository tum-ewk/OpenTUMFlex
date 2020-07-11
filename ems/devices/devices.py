"""
devices module will  document the device parameters (general and specific for each device). All the data will
be sorted in an adequate serving other modules like optplan and flexopts.
"""

import pandas as pd
import json as js
import numpy as np
import datetime
from scipy.interpolate import UnivariateSpline

from ems.ems_mod import ems as ems_loc
from ems.ems_mod import ems_write as emswrite


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

        if path is None:
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

        else:

            with open(path) as f:
                dict_hp = js.load(f)

            dict_unit_hp = {device_name: dict_hp}

        return dict_unit_hp

    # for test
    # test
    # use case for electric vehicle
    elif device_name == 'ev':

        if path is None:

            # ev_aval = ["10:00", "14:00", "17:45", "19:15"]
            _ev_aval_date = ev_aval
            aval_time_init = ev_aval[::2]
            aval_time_end = ev_aval[1::2]
            _ev_aval = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M') for x in _ev_aval_date]
            _points = int(len(_ev_aval) / 2)
            _timesteps = timesetting['nsteps']
            ntsteps = timesetting['ntsteps']
            nsteps = timesetting['nsteps']
            aval = np.zeros(_timesteps)
            init_soc_check = np.zeros(_timesteps) + 100
            end_soc_check = np.zeros(_timesteps)
            consum = np.zeros(_timesteps)
            node = np.zeros((_points - 1) * 2)
            start_time = datetime.datetime.strptime(timesetting['start_time'], '%Y-%m-%d %H:%M')
            day_start = start_time.day
            hour_start = start_time.hour
            min_start = start_time.minute

            idx = 0
            for i in range(_points):
                _aval_start = int(((_ev_aval[idx].day - day_start) * 24 +
                                   (_ev_aval[idx].hour - hour_start) +
                                   (_ev_aval[idx].minute - min_start) / 60) * ntsteps)
                # _aval_end = int(_ev_aval[idx + 1].hour * 4 + _ev_aval[idx + 1].minute / 15 - 1)
                _aval_end = int(((_ev_aval[idx + 1].day - day_start) * 24 +
                                 (_ev_aval[idx + 1].hour - hour_start) +
                                 (_ev_aval[idx + 1].minute - min_start) / 60) * ntsteps - 1)
                aval[_aval_start:_aval_end + 1] = 1
                if _aval_start == 0:
                    pass
                else:
                    init_soc_check[_aval_start-1] = init_soc[i]
                end_soc_check[_aval_end] = end_soc[i]
                if i == _points - 1:
                    end_soc_check[_aval_end:] = end_soc[i]
                idx = idx + 2

            idx = 0
            for j in range(_points - 1):
                # _aval_end = int(_ev_aval[idx + 1].hour * 4 + _ev_aval[idx + 1].minute / 15)
                _aval_end = int(((_ev_aval[idx + 1].day - day_start) * 24 +
                                 (_ev_aval[idx + 1].hour - hour_start) +
                                 (_ev_aval[idx + 1].minute - min_start) / 60) * ntsteps)
                # _aval_start = int(_ev_aval[idx + 2].hour * 4 + _ev_aval[idx + 2].minute / 15)
                _aval_start = int(((_ev_aval[idx + 2].day - day_start) * 24 +
                                   (_ev_aval[idx + 2].hour - hour_start) +
                                   (_ev_aval[idx + 2].minute - min_start) / 60) * ntsteps)
                node[idx] = _aval_end
                node[idx + 1] = _aval_start - 1
                consum[_aval_end:_aval_start] = (end_soc[j] - init_soc[j + 1]) / 100 * stocap / \
                                                (_aval_start - _aval_end)
                idx = idx + 2

            unit.update({'endSOC': end_soc, 'aval': list(aval), 'aval_init': list(aval_time_init),
                         'aval_end': list(aval_time_end),
                         'init_soc_check': list(init_soc_check),
                         'end_soc_check': list(end_soc_check), 'node': list(node)})
            df_unit_ev = unit
            dict_unit_ev = {device_name: df_unit_ev}

        else:
            with open(path) as f:
                dict_ev = js.load(f)

            dict_unit_ev = {device_name: dict_ev}

        return dict_unit_ev
    
    # use case for electric vehicle
    #use ev_new when importing data from excel
    elif device_name == 'ev_new':        
        device_name = 'ev'   
        nsteps = timesetting['nsteps']
        ev_aval_list = {'timeStamp':timesetting['time_slots'].to_list(),'ev_aval':ev_aval}
        ev_aval = pd.DataFrame(ev_aval_list)               
        aval = ev_aval['ev_aval'].values.tolist()
        init_soc_check = np.zeros(nsteps) + 100
        end_soc_check = np.zeros(nsteps)
        node= []
        
        #checking no. of changes in the column: ev_aval from 0 to 1
        change_toOne = 0
        ev_column = ev_aval['ev_aval']
        length = len(ev_column.index)
        for i in range(length):
            if i<nsteps-1:
                if ev_column[i] == 1 and i==0:
                    change_toOne = change_toOne +1
                    node.append(i)
                elif ev_column[i] < ev_column[i+1]:
                    change_toOne = change_toOne +1
                    node.append(i)

        # print(change_toOne)
        init_soc= []
        for p in range(change_toOne):
            init_soc.append(40)
        if change_toOne == 0:
            init_soc.append(0)            
            
        #for change from 0 to 1: updating init_soc_check
        j=0
        aval_time_init =[]
        for i in range(length):
            if i<nsteps-1:
                if ev_column[i] == 1 and i==0:
                    init_soc_check[i]= init_soc[j]
                    aval_time_init.append(ev_aval['timeStamp'][i])
                    j+=1
                elif ev_column[i] < ev_column[i+1]:
                    init_soc_check[i]= init_soc[j]                      
                    aval_time_init.append(ev_aval['timeStamp'][i+1])
                    j+=1
        if len(aval_time_init) == 0:
            aval_time_init.append(ev_aval['timeStamp'][0]) ##edit

        #checking no. of changes in the column: ev_aval from 1 to 0   
        change_toZero = 0
        for i in range(length):
            if i<nsteps-1:
                if ev_column[i] > ev_column[i+1]:
                    change_toZero = change_toZero +1
                    node.append(i+1)

        # print(change_toZero)
        end_soc= []
        for q in range(change_toZero):
            end_soc.append(60)
        if change_toZero == 0:
            end_soc.append(0)
      
        #for change from 1 to 0: updating end_soc_check
        k=0
        aval_time_end =[]
        for i in range(length):
            if i<nsteps-1:
                if ev_column[i] > ev_column[i+1]:
                    end_soc_check[i]= end_soc[k]
                    aval_time_end.append(ev_aval['timeStamp'][i+1])
                    if k == change_toZero - 1:
                        end_soc_check[i:] = end_soc[k]
                    k+=1 
        if len(aval_time_end) == 0:
            aval_time_end.append(ev_aval['timeStamp'][0])
        node.sort()
       
        unit.update({'initSOC': init_soc,'endSOC': end_soc, 'aval': aval, 'aval_init': list(aval_time_init),
                     'aval_end': list(aval_time_end),
                     'init_soc_check': list(init_soc_check),
                     'end_soc_check': list(end_soc_check), 'node': list(node)})
        df_unit_ev = unit
        dict_unit_ev = {device_name: df_unit_ev}
        return dict_unit_ev

    # use case for combine heat and power
    elif device_name == 'sto':

        if path is None:

            temp_min = 18
            temp_max = 50
            if stocap is None:
                stocap = sto_volume * 0.997 * 4.186 * (temp_max - temp_min) / 3600
            unit.update({'stocap': stocap, 'mintemp': temp_min, 'maxtemp': temp_max,
                         'self_discharge': 0.005}
                        )
            df_unit_sto = unit
            dict_unit_sto = {device_name: df_unit_sto}

        else:
            with open(path) as f:
                dict_sto = js.load(f)

            dict_unit_sto = {device_name: dict_sto}

        return dict_unit_sto

    # for other situations
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


"""
test
"""

if __name__ == '__main__':

    ev_aval_date = ["10:00", "14:00", "17:45", "19:15", "21:30", "23:15"]
    ev_aval = [datetime.datetime.strptime(x, "%H:%M") for x in ev_aval_date]
    points = int(len(ev_aval) / 2)
    timesteps = 96
    aval = np.zeros(timesteps)

    idx = 0
    for i in range(points):
        aval_start = int(ev_aval[idx].hour * 4 + ev_aval[idx].minute / 15)
        aval_end = int(ev_aval[idx + 1].hour * 4 + ev_aval[idx + 1].minute / 15 - 1)
        aval[aval_start:aval_end + 1] = 1
        idx = idx + 2

    # count = raw_input('Number of variables:')
# for i in my_ems1['devices'].keys():
#     exec('var_' + str(i) + ' = ' + str(my_ems1['devices'][i]))

# device_write(my_ems1, 'bat', path='C:/Users/ge57vam/emsflex/ems/bat01_ems.txt')
