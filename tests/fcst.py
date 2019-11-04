# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 13:12:54 2019
@author: ga47jes
"""

import pandas as pd


# from tkinter import filedialog

def load_data(nsteps=96, path=r"C:\Optimierung\Eingangsdaten_hp.xlsx"):
    # excelFile = filedialog.askopenfilename()
    # excelFile = r"C:\Optimierung\Eingangsdaten_hp.xlsx"
    df = pd.read_excel(path, sheet_name='time_series', usecols='B:H', nrows=nsteps)
    dict_fcst = df.to_dict('dict')
    return dict_fcst


if __name__ == '__main__':
    e = load_data(96)
    time_series = pd.DataFrame.from_dict(e)
