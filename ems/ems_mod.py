# -*- coding: utf-8 -*-
"""
ems(energy management system) is the module to document the ems_ID, user_preference, flexibility_product_type and time interval.
Besides, all the information from modules of devices parameters, optimal operational plan and flexibility shall also stored in the ems module for a better
overview and quick search of the needed data.
"""

import pandas as pd
import json as js
import datetime

def ems(emsid=000000, userpref=None, flexprodtype=None, timeintervall=15, days=1, dataintervall=15, start_time=None,
        end_time=None, initialize=False, path=None):
    # get the time index series
    date = pd.date_range(start='00:00:00', periods=5, freq=str(timeintervall) + ' ' + 'T')
    datestr = pd.Series(date.format())

    # initialize the ems by user input
    if not initialize:

        # DataFrame of forecasting for example
        df_fcst = pd.DataFrame({}, index=datestr)
        # DataFrame of optimal operational plan for example
        df_optplan = pd.DataFrame({}, index=datestr)
        # DataFrame of flexibility options for example
        df_flexopts = {}

        # convert the user input to time data
        time_data = {'nsteps': int(24 * 60 / timeintervall),
                     'ntsteps': int(60 / timeintervall),
                     't_inval': timeintervall,
                     'd_inval': dataintervall,
                     'start_time': start_time,
                     'end_time': end_time,
                     'days': days}

        # summary of all data in ems dict
        dic_ems = {'ID': emsid,
                   'userpref': userpref,
                   'flexprodtype': flexprodtype,
                   'time_data': time_data,
                   'timeintervall': timeintervall,
                   'fcst': df_fcst.to_dict('dict'),
                   'optplan': df_optplan.to_dict('dict'),
                   'flexopts': df_flexopts,
                   'devices': None
                   }

    # initialize the ems by csv import
    else:
        with open(path) as f:
            dic_ems = js.load(f)
            # convert flexopts from dict to dataframe
            for key in dic_ems['flexopts']:
                dic_ems['flexopts'][key] = pd.DataFrame.from_dict(dic_ems['flexopts'][key])

    return dic_ems


def ems_write(dict_ems, path):
    # change index to lists
    dict_ems['time_data']['time_slots'] = list(dict_ems['time_data']['time_slots'])
    with open(path, 'w') as f:
        # change dataframe format to dict
        for key in dict_ems['flexopts']:
            if not isinstance(dict_ems['flexopts'][key], dict):
                dict_ems['flexopts'][key] = dict_ems['flexopts'][key].to_dict('dict')
        js.dump(dict_ems, f)
    print('complete saving EMS_data!!! ')


def update_time_data(dict_ems):
    # update ems["time_data"], add new parameters: time_slots, nsteps, ntsteps
    dict_time = dict_ems['time_data']
    dict_time['time_slots'] = pd.date_range(start=dict_time['start_time'], end=dict_time['end_time'],
                                            freq=str(dict_time['t_inval']) + 'min').strftime('%Y-%m-%d %H:%M')

    dict_time['nsteps'] = len(dict_time['time_slots'])
    dict_time['ntsteps'] = int(60 / dict_ems['time_data']['t_inval'])
    dict_time_data = {'time_data': dict_time}
    return dict_time_data


if __name__ == '__main__':
    c = ems(initialize=True, path='../ems/ems_test_02_wopt.txt')
    c['time_data'] = {}
    c['time_data']['nsteps'] = 24
    c['time_data']['ntsteps'] = 1
    c['time_data']['t_inval'] = 60
    c['time_data']['d_inval'] = 15
    c['time_data']['days'] = 1
    ems_write(c, path='../ems/test_time.txt')
