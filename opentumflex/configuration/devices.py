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


def devices(device_name, minpow=0, maxpow=0, stocap=0, eta=1, init_soc=20, end_soc=40, ev_aval=None,
            supply_temp=45, timesetting=96, sto_volume=0, path=None):
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
            temp_supply = [288.15, 308.15, 318.15, 328.15, 333.15]
            # 45 C supply temperature
            # hp_q = pd.DataFrame({'266.15': [4.8, 4.8, 4.8],
            #                      '275.15': [6.0, 6.0, 6.0],
            #                      '280.15': [7.5, 7.5, 7.5],
            #                      '288.15': [9.2, 9.2, 9.2],
            #                      '293.15': [9.9, 9.9, 9.9],
            #                      }, index=temp_supply
            #                     )
            # 20 C supply temperature
            hp_q = pd.DataFrame({'266.15': [6, 5.2, 4.8, 4.2, 3.9],
                                 '275.15': [7.5, 6.5, 6.0, 5.3, 5.0],
                                 '280.15': [9.0, 8.0, 7.5, 6.8, 6.5],
                                 '288.15': [10.7, 9.7, 9.2, 8.4, 8.0],
                                 '293.15': [11.7, 10.5, 9.9, 9.2, 8.9],
                                 }, index=temp_supply
                                )
            hp_p = pd.DataFrame({'266.15': [1.5, 1.8, 1.9, 2.0, 2.1],
                                 '275.15': [1.6, 1.9, 2.1, 2.1, 2.1],
                                 '280.15': [1.6, 2.0, 2.3, 2.4, 2.4],
                                 '288.15': [1.7, 2.1, 2.5, 2.7, 2.8],
                                 '293.15': [1.8, 2.2, 2.6, 2.9, 3.0],
                                 }, index=temp_supply
                                )

            def modify_hp_data(data_original, temperature):
                temp_data = data_original
                value = np.zeros(temp_data.shape[1])
                for _col_num in range(temp_data.shape[1]):
                    spline = UnivariateSpline(list(map(float, temp_data.index.values)),
                                              list(temp_data.iloc[:, _col_num]))
                    value[_col_num] = spline(temperature).item(0)
                temp_data.loc[temperature] = value
                return temp_data.sort_index()

            supply_temp = supply_temp + 273.15  # convert from grad celsius to kelvin
            hp_q = modify_hp_data(hp_q, supply_temp)
            hp_p = modify_hp_data(hp_p, supply_temp)
            hp_cop = hp_q.div(hp_p)
            fact_p = maxpow / hp_p.loc[supply_temp, '275.15']

            # change the DataFrame to Dict
            unit.update({'maxpow': hp_p.multiply(fact_p).to_dict('dict'), 'COP': hp_cop.to_dict('dict'),
                         'supply_temp': supply_temp,
                         'thermInertia': 50, 'minTemp': 20, 'maxTemp': 26, 'heatgain': 0.1})
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
            elif ev_column[i]==1 and i==nsteps-1:
                change_toZero = change_toZero +1
                node.append(i)

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
        if len(aval_time_init) > len(aval_time_end):
            end_soc_check[nsteps-1]= end_soc[k]
            aval_time_end.append(ev_aval['timeStamp'][nsteps-1])
            
        node.sort()
       
        unit.update({'initSOC': init_soc,'endSOC': end_soc, 'aval': aval, 'aval_init': list(aval_time_init),
                     'aval_end': list(aval_time_end),
                     'init_soc_check': list(init_soc_check),
                     'end_soc_check': list(end_soc_check), 'node': list(node)})
        df_unit_ev = unit
        dict_unit_ev = {device_name: df_unit_ev}
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
                    "eta": eta }                   
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


def device_write(dict_ems, device_name, path):
    # write parameters of other devices in js file
    device_unit = dict_ems['devices'][device_name]

    # open the file and write in the data
    with open(path, 'w') as f:
        js.dump(device_unit, f)


if __name__ == '__main__':
    ev_aval_date = ["2019-11-30 11:15", "2019-12-02 8:45"]
    ev_aval = [datetime.datetime.strptime(x, '%Y-%m-%d %H:%M') for x in ev_aval_date]
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

# device_write(my_ems1, 'bat', path='C:/Users/ge57vam/emsflex/opentumflex/bat01_ems.txt')
