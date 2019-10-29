# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 13:12:54 2019

@author: ga47jes
"""

import pandas as pd
#from tkinter import filedialog

def load_data(nsteps):
    #excelFile = filedialog.askopenfilename()
    excelFile = r"H:\TUM-PC\Dokumente\Babu\Project\Csells\Ficus_update\Eingangsdaten_hp.xlsx"
    df = pd.read_excel(excelFile, sheet_name='time_series', usecols='B:H', nrows=nsteps)
    return df
