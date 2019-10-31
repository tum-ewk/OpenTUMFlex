# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 14:06:33 2019

@author: ga47jes
"""

import pandas as pd
import matplotlib.pyplot as plt

def plot_flex(nsteps):    
    # For test purpose - to be restructrued with dataframe
    excelFile = r"H:\TUM-PC\Dokumente\Babu\System\Softwares\Python\Practice\Cumm_daten.xlsx"
    dat1 = pd.read_excel(excelFile, sheet_name='cumm', usecols='B:H', nrows=96)
#    dat2 = pd.DataFrame(index=pd.date_range(start="00:00", end="23:59", freq='15min').strftime('%H:%M'), columns = ['values'])

    # Plotting cummulative energy exchange
    theta = 0
    cum_data = [0]*nsteps
    for i in range(nsteps):
        cum_data[i] = theta + dat1.iloc[i,0]*0.25
        theta = cum_data[i]   
    plt.plot(cum_data, linewidth=2, color='k')
    plt.xlabel('Time slot')
    plt.ylabel('Cummulative energy (kWh)')
        
    for x in range(nsteps):
        # Negative flexibility plots
        if dat1.iloc[x,3] < 0:
            theta = cum_data[x]
            slots = int(round(4*dat1.iloc[x,3]/dat1.iloc[x,1]))  #nsteps
            slot_flex = dat1.iloc[x,3]/slots
            for y in range(1,slots):
                plt.plot([x+y-1,x+y],[theta, cum_data[x+y]+(slot_flex*y)], color='b')
                theta = cum_data[x+y]+(slot_flex*y)
       
        # Positive flexibility plots
        if dat1.iloc[x,4] > 0:
            theta = cum_data[x]
            slots = int(round(4*dat1.iloc[x,4]/dat1.iloc[x,2]))  #nsteps
            slot_flex = dat1.iloc[x,4]/slots
            for y in range(1,slots):
                plt.plot([x+y-1,x+y],[theta, cum_data[x+y]+(slot_flex*y)], color='r')
                theta = cum_data[x+y]+(slot_flex*y)
                
def save_results(dat1, nsteps, save_path):
      dat1.to_excel("output.xlsx",sheet_name='flex_results')      
