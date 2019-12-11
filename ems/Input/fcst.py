# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 13:12:54 2019
@author: ga47jes
"""

import pandas as pd
# from tkinter import filedialog

def load_data(my_ems, path=r"H:\TUM-PC\Dokumente\Babu\System\Softwares\Python\Practice\Eingangsdaten_hp.xlsx"):
    # path = filedialog.askopenfilename()
    if my_ems['time_data']['t_inval'] == my_ems['time_data']['d_inval']:
        df = pd.read_excel(path, sheet_name='time_series', usecols='B:H', nrows=my_ems['time_data']['nsteps'])
        dict_fcst = df.to_dict('dict')
        return dict_fcst
    elif my_ems['time_data']['t_inval'] > my_ems['time_data']['d_inval']:
        ratio = int(my_ems['time_data']['t_inval']/my_ems['time_data']['d_inval'])
        df = pd.read_excel(path, sheet_name='time_series', usecols='B:H', nrows=my_ems['time_data']['nsteps']*ratio)        
        df_mean = df.groupby(df.index // 4).mean()
        dict_fcst = df_mean.to_dict('dict')
        return dict_fcst
    
if __name__ == '__main__':
    timeintervall = 60
    days = 1
    time_data = {'nsteps': int(24*60/timeintervall),
             'ntsteps': int(60/timeintervall),
             't_inval': timeintervall,
             'd_inval': 15,
             'days': days}
    my_ems = {'time_data':time_data}
    e = load_data(my_ems)
    time_series = pd.DataFrame.from_dict(e)
    