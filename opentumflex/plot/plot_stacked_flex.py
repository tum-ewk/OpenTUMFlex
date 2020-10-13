"""
The "plot_stacked_flex.py" can visualize the results of flexibility in one stacked plot
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
import matplotlib.pyplot as plt
from operator import add

def plot_stacked_flex(ems, reopt=0):
    """
    

    Parameters
    ----------
    ems : dict
        ems model.
    reopt : binary, optional
        Choose between optimization or reoptimization. The default is 0.

    Returns
    -------
    None.

    """    
    
    nsteps = ems['time_data']['nsteps']
    ts = ems['time_data']['time_slots'].tolist()
    chart = ['skyblue', 'steelblue', 'cornflowerblue', 'lightslategray', 'deepskyblue'] 
    plt.figure(figsize=(12, 8))
    font_size = 14
    
    # Cummulative list of devices for flex optimization
    if not reopt:
        # Get required defaults
        device = list(ems['flexopts'].keys())     
        bottom_pos = [0]*len(ts)     
        bottom_neg = [0]*len(ts)  
        
        # Loop through the device list and stack plot
        for i in range(len(device)):
            flex_pos = plt.bar(ts, ems['flexopts'][device[i]]['Pos_P'], color=chart[i], 
                               bottom=bottom_pos, align='edge', edgecolor='k', label=device[i])
            flex_neg = plt.bar(ts, ems['flexopts'][device[i]]['Neg_P'], color=chart[i], 
                               bottom=bottom_neg, align='edge', edgecolor='k')
            
            # Update bottom values
            bottom_pos = list(map(add, bottom_pos,ems['flexopts'][device[i]]['Pos_P'].tolist()))
            bottom_neg = list(map(add, bottom_neg,ems['flexopts'][device[i]]['Neg_P'].tolist()))
        
        # Change xtick intervals    
        req_ticks = 12   # ticks needed
        if nsteps > req_ticks:
            plt.xticks(ts[::int(round(nsteps/req_ticks))], rotation=-45, ha="left", fontsize=font_size)
        else:
            plt.xticks(ts, rotation=-45, ha="left", fontsize=font_size)       
            
        # Plot legend
        plt.legend(loc='lower left', bbox_to_anchor=(1.01, 0), fontsize=font_size)
        
        # Axis labels
        plt.ylabel("Flexibility power [kW]", fontsize=font_size)
        plt.xlabel("Time", fontsize=font_size)
        
        
def plot_stacked_flex_price(ems, reopt=0):
    """
    

    Parameters
    ----------
    ems : dict
        ems model.
    reopt : binary, optional
        Choose between optimization or reoptimization. The default is 0.

    Returns
    -------
    None.

    """  
    
    nsteps = ems['time_data']['nsteps']
    ts = ems['time_data']['time_slots'].tolist()
    plt.figure(figsize=(12, 8))
    font_size = 14
    
    if not reopt:
        # Get required defaults
        device = list(ems['flexopts'].keys())  
        pos_price_max = [0]*len(ts) 
        neg_price_min = [0]*len(ts) 
        
        # Loop through the device list and area plot
        for i in range(len(device)):
            pos_price_max = [max(value) for value in zip(pos_price_max, ems['flexopts'][device[i]]['Pos_Pr'])]
            neg_price_min = [min(value) for value in zip(neg_price_min, ems['flexopts'][device[i]]['Neg_Pr'])]
            
        pos_price_min = pos_price_max
        neg_price_max = neg_price_min
        
        for i in range(len(device)):
            pos_price_min = [min(value) for value in zip(pos_price_min, ems['flexopts'][device[i]]['Pos_Pr'])]
            neg_price_max = [max(value) for value in zip(neg_price_max, ems['flexopts'][device[i]]['Neg_Pr'])]
            
        # plt.fill_between(ts, pos_price_max, pos_price_min)
        # plt.fill_between(ts, neg_price_max, neg_price_min)
        
        plt.plot(ts, pos_price_max)
        plt.plot(ts, neg_price_min)
    
        # Change xtick intervals    
        req_ticks = 12   # ticks needed
        if nsteps > req_ticks:
            plt.xticks(ts[::int(round(nsteps/req_ticks))], rotation=-45, ha="left", fontsize=font_size)
        else:
            plt.xticks(ts, rotation=-45, ha="left", fontsize=font_size)     
            
        return pos_price_max, pos_price_min, neg_price_max, neg_price_min
    
    