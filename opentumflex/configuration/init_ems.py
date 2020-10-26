# -*- coding: utf-8 -*-
"""
init_ems.py is the module to initialize and save ems object. It also includes the functions reading forecasting data and
device parameters.
Besides, all the information from modules of devices parameters, optimal operational plan and flexibility shall also
stored in the ems object for a better overview and quick search of the needed data.
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
import os


def save_ems(ems, path):
    """ save all the data in ems object into one json file

    :param ems: ems object
    :param path: path where the json file will be saved
    :return: none
    """

    # change index to lists
    ems['time_data']['time_slots'] = list(ems['time_data']['time_slots'])
    with open(path, 'w') as f:
        # change dataframe format to dict
        for key in ems['flexopts']:
            if not isinstance(ems['flexopts'][key], dict):
                ems['flexopts'][key] = ems['flexopts'][key].to_dict('dict')
        js.dump(ems, f)


def init_ems_js(path=None):
    """ initialize the ems object by json file

    :param path: path of the json file
    :return: ems object
    """
    # initialize the opentumflex by user input
    with open(path) as f:
        ems = js.load(f)
        # convert flexopts from dict to dataframe
        for key in ems['flexopts']:
            ems['flexopts'][key] = pd.DataFrame.from_dict(ems['flexopts'][key])

    return ems


def update_time_data(ems):
    """ calculate the remaining time settings based on the user input

    :param ems: ems object
    :return:
    """
    # update opentumflex["time_data"], add new parameters: time_slots, nsteps, ntsteps
    dict_time = ems['time_data']
    # form the time slots
    dict_time['time_slots'] = pd.date_range(start=dict_time['start_time'], end=dict_time['end_time'],
                                            freq=str(dict_time['t_inval']) + 'min').strftime('%Y-%m-%d %H:%M')

    dict_time['isteps'] = 0
    # calculate the total time steps
    dict_time['nsteps'] = len(dict_time['time_slots'])
    # calculate the time steps in each hour
    dict_time['ntsteps'] = int(60 / ems['time_data']['t_inval'])

    dict_time_data = {'time_data': dict_time}

    return dict_time_data


def read_data(ems, path=None, to_csv=False, fcst_only=True):
    """ read device parameters or forecasting data from input file

    :param ems: ems object
    :param path: path of the input data
    :param to_csv: determine if csv data will be created
    :param fcst_only: if False,  forecasting data and device parameters will be read, otherwise only forecasting data
    :return: ems object updated by the input data
    """

    # Check for the file type 
    if path.endswith('.xlsx'):
        print('Reading your excel file, please wait!')
        # obtain the spreadsheet data
        xls = pd.ExcelFile(path)
        if not fcst_only:            
            # read device parameters
            prop = pd.read_excel(xls, sheet_name='properties', index_col=0, usecols=range(0, 3))
            read_properties(ems, prop)
        # read forecasting data and write it into ems object
        ts = pd.read_excel(xls, sheet_name='time_series', usecols='B:I', nrows=ems['time_data']['nsteps'])
        ems['fcst'] = read_forecast(ts)
        # Save excel file as CSV
        if to_csv:
            basename = os.path.basename(path)
            filename = os.path.splitext(basename)[0] + '.csv'
            if not os.path.exists('input'):
                os.mkdir('input')
            directory = os.path.join(r'input', filename)
            with open(directory, 'w') as f:
                if not fcst_only:
                    pd.concat([prop, ts], sort=False).to_csv(f, sep=';')
                else:
                    ts.to_csv(f, sep=';')

    elif path.endswith('.csv'):
        csv_data = pd.read_csv(path, sep=';', index_col=0)
        prop = csv_data.iloc[:, 0:2].dropna(how='all')
        ts = csv_data.iloc[:, 2:].dropna(how='all')
        # read device parameters
        if not fcst_only:
            read_properties(ems, prop)
        # read forecasting data and write it into ems object
        ems['fcst'] = read_forecast(ts)

    else:
        print('Input file format is not accepted, Exit call')

    return ems


def read_forecast(excel_data):
    """ read the forecasting data from spreadsheet

    :param excel_data: excel_data sheet 'time_series'
    :return: dictionary of forecasting data
    """
    dict_fcst = excel_data.to_dict('dict')
    for key in dict_fcst:
        dict_fcst[key] = list(dict_fcst[key].values())

    return dict_fcst


def read_properties(ems, prop):
    """ read the device parameters from spreadsheet

    :param ems: ems object
    :param prop:  device parameters from input file
    :return: None
    """
    data_index = prop.index.unique()
    device_set = ems['devices']
    # iterate through all the device parameters and write it into dictionary device_set
    for i in range(0, len(data_index)):
        dat = prop[prop.index == data_index[i]].set_index('parameter')
        dat_T = dat.T
        dat_T.reset_index(inplace=True, drop=True)
        device_set[data_index[i]].update(dat_T.to_dict('records')[0])
    ems['devices'] = device_set

    # Changing EV input to list
    ems['devices']['ev']['initSOC'] = [ems['devices']['ev']['initSOC']]
    ems['devices']['ev']['endSOC'] = [ems['devices']['ev']['endSOC']]

