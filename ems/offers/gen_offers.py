# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 12:47:59 2020

@author: ga47jes
"""

import pandas as pd
from datetime import datetime 
import os

def alf_markt(my_ems,device):
    df = pd.DataFrame(columns=['Uhrzeit','Leistung_Plan','Leistung-','Leistung+','Energie-',
                               'Energie+','Preis-','Preis+', 'Teilabruf', 
                               'max_Anzahl_Abrufe_pro_Tag', 'max_Dauer_pro_Tag_in_h',
                               'Dauer_zwischen_zwei_Abrufen_in_h', 'max_Dauer_eines_Abrufs',
                               'min_Dauer_eines_Abrufs'], index=range(1,96))
    
    # Add UTC string to Uhrzeit
    UTC = " +0100"
    
    for i in range(0,95):
        for j in range(0,8):
            if j != 0:
                df.iloc[i][j] = round(my_ems['flexopts'][device].iloc[i][j], 5)
            else:
                temp = my_ems['flexopts'][device].iloc[i][j]
                if isinstance(temp, str):
                    datetime_object = datetime.strptime(temp, "%Y-%m-%d %H:%M")
                    df.iloc[i][j] = datetime_object.strftime("%d.%m.%Y %H:%M") + UTC
                else:
                    print("check whether flex offer time column is available?")
     
    # Additional parameters           
    df.iloc[0,8] = "Ja"  #Teilberuf
    df.iloc[0,9] = 2     #max_Anzahl_Abrufe_pro_Tag
    df.iloc[0,10] = 2.25     #max_Dauer_pro_Tag_in_h
    df.iloc[0,11] = 1.5     #Dauer_zwischen_zwei_Abrufen_in_h
    df.iloc[0,12] = 1.5     #max_Dauer_eines_Abrufs
    df.iloc[0,13] = 0.25     #min_Dauer_eines_Abrufs
    
    df['Leistung_Plan'] = df['Leistung_Plan'].astype(float)
    df['Leistung-'] = df['Leistung-'].astype(float)
    df['Leistung+'] = df['Leistung+'].astype(float)
    df['Energie-'] = df['Energie-'].astype(float)
    df['Energie+'] = df['Energie+'].astype(float)
    df['Preis-'] = df['Preis-'].astype(float)
    df['Preis+'] = df['Preis+'].astype(float)
    # df['Teilabruf'] = df['Teilabruf'].astype(str)
    df['max_Anzahl_Abrufe_pro_Tag'] = df['max_Anzahl_Abrufe_pro_Tag'].astype(float)
    df['max_Dauer_pro_Tag_in_h'] = df['max_Dauer_pro_Tag_in_h'].astype(float)
    df['Dauer_zwischen_zwei_Abrufen_in_h'] = df['Dauer_zwischen_zwei_Abrufen_in_h'].astype(float)
    df['max_Dauer_eines_Abrufs'] = df['max_Dauer_eines_Abrufs'].astype(float)
    df['min_Dauer_eines_Abrufs'] = df['min_Dauer_eines_Abrufs'].astype(float)
    
    # Save as CSV file
    cwd = os.getcwd()
    # back_cwd = os.path.dirname(cwd)
    mdir = "flexoffers" 
    path = os.path.join(cwd,mdir)
    if not os.path.exists(path):
        os.mkdir(path)
    file_name = datetime_object.strftime("%Y-%m-%d")+ '_' + \
        device+'_Flex-Angebot.csv'
    new_cwd = os.path.join(path,file_name)
    df.to_csv(new_cwd, sep=';', decimal=',', index=False)
    print("CSV file generated! Available on " + new_cwd)
    