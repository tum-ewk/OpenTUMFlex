"""
The "fcst.py" read the input data (xlsx) regarding predefined time settings
"""

__author__ = "Babu Kumaran Nalini"
__copyright__ = "2020 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "1.0"
__maintainer__ = "Babu Kumaran Nalini"
__email__ = "babu.kumaran-nalini@tum.de"
__status__ = "Development"


import pandas as pd


# from tkinter import filedialog

def load_data(my_ems, path=r"../forecast/Testdata/Eingangsdaten_hp.xlsx"):
    # path = filedialog.askopenfilename()
    if my_ems['time_data']['t_inval'] == my_ems['time_data']['d_inval']:
        df = pd.read_excel(path, sheet_name='time_series', usecols='B:I', nrows=my_ems['time_data']['nsteps'])
        dict_fcst = df.to_dict('dict')
        for key in dict_fcst:
            dict_fcst[key] = list(dict_fcst[key].values())
        return dict_fcst
    elif my_ems['time_data']['t_inval'] > my_ems['time_data']['d_inval']:
        ratio = int(my_ems['time_data']['t_inval'] / my_ems['time_data']['d_inval'])
        df = pd.read_excel(path, sheet_name='time_series', usecols='B:I', nrows=my_ems['time_data']['nsteps'] * ratio)
        df_mean = df.groupby(df.index // ratio).mean()
        dict_fcst = df_mean.to_dict('dict')
        for key in dict_fcst:
            dict_fcst[key] = list(dict_fcst[key].values())
        return dict_fcst


if __name__ == '__main__':
    timeintervall = 60
    days = 1
    time_data = {'nsteps': int(24 * 60 / timeintervall),
                 'ntsteps': int(60 / timeintervall),
                 't_inval': timeintervall,
                 'd_inval': 15,
                 'days': days}
    my_ems = {'time_data': time_data}
    e = load_data(my_ems)
    time_series = pd.DataFrame.from_dict(e)
