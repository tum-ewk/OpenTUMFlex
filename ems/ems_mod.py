# -*- coding: utf-8 -*-
"""
ems(energy management system) is the module to document the ems_ID, user_preference, flexibility_product_type and time interval.
Besides, all the information from modules of devices parameters, optimal operational plan and flexibility shall also stored in the ems module for a better
overview and quick search of the needed data.
"""

import pandas as pd
import json as js


# from ems.optim.opt_test import run_hp_opt as opt


def ems(emsid=000000, userpref=None, flexprodtype=None, timeintervall=15, initialize=False, path=None):
    # get the time index series
    date = pd.date_range(start='00:00:00', dtype='datetime64[ns]', periods=5, freq=str(timeintervall) + ' ' + 'T')
    datestr = pd.Series(date.format())

    # initialize the ems by user input
    if not initialize:

        # DataFrame of forecasting for example
        df_fcst = pd.DataFrame({'heatload': [2.11, 3.554, 4.55, 0.985, 2.88],
                                'elecload': [2.11, 3.554, 4.55, 0.985, 2.88],
                                'pvInt': [0.2, 0.3, 0.35, 0.44, 0.34],
                                'temp': [280, 285, 283, 284, 281]}, index=datestr
                               )
        # DataFrame of optimal operational plan for example
        df_optplan = pd.DataFrame({'hpstate': [1, 0, 0, 1, 1],
                                   'pvstate': [1, 0, 0, 1, 1],
                                   'batstate': [1, 0, 0, 1, 1],
                                   'evstate': [1, 0, 0, 1, 1]}, index=datestr
                                  )
        # DataFrame of flexibility options for example
        df_flexopts = pd.DataFrame({'optplan': [1, 0, 0, 1, 1],
                                    'pospower': [2.11, 3.554, 4.55, 0.985, 2.88],
                                    'negpower': [-2.11, -3.554, -4.55, 0.985, -2.88],
                                    'posergy': [0.11, 0.554, 0.55, 0.985, 0.88]}, index=datestr
                                   )
        dic_ems = {'ID': emsid,
                   'userpref': userpref,
                   'flexprodtype': flexprodtype,
                   'timeintervall': timeintervall,
                   'fcst': df_fcst.to_dict('dict'),
                   'optplan': df_optplan.to_dict('dict'),
                   'flexopts': df_flexopts.to_dict('dict'),
                   'devices': None
                   }

    # initialize the ems by csv import
    else:

        with open(path) as f:
            dic_ems = js.load(f)

        # change the dic(fcst,optplan,flexopts) into DataFrames
        # dic_ems['fcst'] = pd.DataFrame.from_dict(dic_ems['fcst'])
        # dic_ems['optplan'] = pd.DataFrame.from_dict(dic_ems['optplan'])
        # dic_ems['flexopts'] = pd.DataFrame.from_dict(dic_ems['flexopts'])

    return dic_ems


def ems_write(dict_ems, path):
    #dict_ems['fcst'] = dict_ems['fcst'].to_dict('dict')
    # dict_ems['optplan'] = dict_ems['optplan'].to_dict('dict')
    #dict_ems['flexopts'] = dict_ems['flexopts'].to_dict('dict')

    with open(path, 'w') as f:
        js.dump(dict_ems, f)


if __name__ == '__main__':
    c = ems(initialize=True, path='C:/Users/ge57vam/emsflex/ems/755552222_ems.txt')
    ems_write(c, path='C:/Users/ge57vam/emsflex/ems/7555522200_ems.txt')
