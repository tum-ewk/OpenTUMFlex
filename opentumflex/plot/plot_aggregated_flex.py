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
import numpy as np

def plot_aggregated_flex_power(ems, reopt=0):
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
        plt.title('Aggregated flex power', fontsize=font_size, pad=20)
        plt.tight_layout()
        plt.show()
    return


def plot_aggregated_flex_price(ems, reopt=0, plot_flexpr='bar'):
    """
    

    Parameters
    ----------
    ems : dict
        ems model.
    reopt : binary, optional
        Choose between optimization or reoptimization. The default is 0.
    plot_flexpr: string
        Choose between plot type bar or scatter

    Returns
    -------
    None.

    """  
    # Get required defaults
    nsteps = ems['time_data']['nsteps']
    ts = ems['time_data']['time_slots'].tolist()
    chart_pos = ['skyblue', 'steelblue', 'cornflowerblue', 'lightskyblue', 'deepskyblue']     
    chart_neg = ['sandybrown', 'indianred', 'coral', 'mistyrose', 'lightsalmon'] 
    device = list(ems['flexopts'].keys())    
    font_size = 14
    
    if not reopt:
        # Create an empty plot
        plt.figure(figsize=(12, 8))

        if plot_flexpr == 'bar':
            # Loop through the device list and stack plot
            for i in range(len(device)):
                plt.bar(ts, ems['flexopts'][device[i]]['Pos_Pr'], color=chart_pos[i], 
                                    alpha=0.8, align='edge', edgecolor='k', label=device[i]+'_pos')
                plt.bar(ts, ems['flexopts'][device[i]]['Neg_Pr'], color=chart_neg[i], 
                                    alpha=0.7, align='edge', edgecolor='k', label=device[i]+'_neg')
                       
            # Change xtick intervals    
            req_ticks = 12   # ticks needed
            if nsteps > req_ticks:
                plt.xticks(ts[::int(round(nsteps/req_ticks))], rotation=-45, ha="left", fontsize=font_size)
            else:
                plt.xticks(ts, rotation=-45, ha="left", fontsize=font_size)       
                
            # Plot legend
            plt.legend(loc='lower left', bbox_to_anchor=(1.01, 0), fontsize=font_size)
            
            # Axis labels
            plt.ylabel("Flexibility price [€/kWh]", fontsize=font_size)
            plt.xlabel("Time", fontsize=font_size)
            plt.title('Aggregated flex price', fontsize=font_size, pad=20)
            plt.tight_layout()
            plt.show()

        if plot_flexpr == 'scatter':
            # Loop through the device list and stack plot
            for i in range(len(device)):
                plt.scatter(ts, ems['flexopts'][device[i]]['Pos_Pr'], color=chart_pos[i], 
                                    label=device[i]+'_pos')
                plt.scatter(ts, ems['flexopts'][device[i]]['Neg_Pr'], color=chart_neg[i],
                                    label=device[i]+'_neg')
                       
            # Change xtick intervals    
            req_ticks = 12   # ticks needed
            if nsteps > req_ticks:
                plt.xticks(ts[::int(round(nsteps/req_ticks))], rotation=-45, ha="left", fontsize=font_size)
            else:
                plt.xticks(ts, rotation=-45, ha="left", fontsize=font_size)       
                
            # Plot legend
            plt.legend(loc='lower left', bbox_to_anchor=(1.01, 0), fontsize=font_size)
            
            # Axis labels
            plt.ylabel("Flexibility price [€/kWh]", fontsize=font_size)
            plt.xlabel("Time", fontsize=font_size)
            plt.title('Aggregated flex price', fontsize=font_size, pad=20)
            plt.tight_layout()
            plt.show()
    return