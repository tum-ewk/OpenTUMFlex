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
    
    # Get required defaults
    timesteps = np.arange(ems['time_data']['isteps'], ems['time_data']['nsteps'])
    N = len(timesteps)
    isteps = ems['time_data']['isteps']
    nsteps = ems['time_data']['nsteps']
    ts = ems['time_data']['time_slots'].tolist()
    ts_raw = ems['time_data']['time_slots'][isteps:nsteps]
    ts_hr = pd.to_datetime(ts_raw).strftime('%H:%M').to_list()
    ts_date = pd.to_datetime(ts_raw).strftime('%d %b %Y')
    
    # Chart details
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
            plt.bar(ts, ems['flexopts'][device[i]]['Pos_P'], color=chart[i], 
                               bottom=bottom_pos, align='edge', edgecolor='k', label=device[i].upper())
            plt.bar(ts, ems['flexopts'][device[i]]['Neg_P'], color=chart[i], 
                               bottom=bottom_neg, align='edge', edgecolor='k')
            
            # Update bottom values
            bottom_pos = list(map(add, bottom_pos,ems['flexopts'][device[i]]['Pos_P'].tolist()))
            bottom_neg = list(map(add, bottom_neg,ems['flexopts'][device[i]]['Neg_P'].tolist()))
        
        # Change xtick intervals    
        req_ticks = 12   # ticks needed
        # plt.xticks(ts_hr)
        if nsteps > req_ticks:
            plt.xticks(ts[::int(round(nsteps/req_ticks))], ts_hr[::int(round(nsteps/req_ticks))], rotation=0, fontsize=font_size)
        else:
            plt.xticks(ts, ts_hr, rotation=0, fontsize=font_size)     
            
        # Plot legend
        plt.legend(loc='lower left', bbox_to_anchor=(1.01, 0), fontsize=font_size)
        
        # Get dates
        date_index, N_dates = find_date_index(ts_date, N)
        for i in np.arange(N_dates):
            plt.text(date_index[i], -14, ts_date[int(date_index[i])], size=font_size-2) 
                
        # Axis labels
        plt.ylabel("Flexibility power [kW]", fontsize=font_size)
        # plt.xlabel("Time", fontsize=font_size)
        plt.title('Aggregated flex power', fontsize=font_size, pad=20)
        plt.xlim([0, nsteps])
        plt.grid()
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
    timesteps = np.arange(ems['time_data']['isteps'], ems['time_data']['nsteps'])
    N = len(timesteps)
    isteps = ems['time_data']['isteps']
    nsteps = ems['time_data']['nsteps']
    ts = ems['time_data']['time_slots'].tolist()
    ts_raw = ems['time_data']['time_slots'][isteps:nsteps]
    ts_hr = pd.to_datetime(ts_raw).strftime('%H:%M').to_list()
    ts_date = pd.to_datetime(ts_raw).strftime('%d %b %Y')
    
    # Chart parameters
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
            # plt.xticks(ts_hr)
            if nsteps > req_ticks:
                plt.xticks(ts[::int(round(nsteps/req_ticks))], ts_hr[::int(round(nsteps/req_ticks))], rotation=0, fontsize=font_size)
            else:
                plt.xticks(ts, ts_hr, rotation=0, fontsize=font_size)
                
            # Plot legend
            plt.legend(loc='lower left', bbox_to_anchor=(1.01, 0), fontsize=font_size)
            
            # Get dates
            date_index, N_dates = find_date_index(ts_date, N)
            for i in np.arange(N_dates):
                plt.text(date_index[i], -0.4, ts_date[int(date_index[i])], size=font_size-2)
            
            # Axis labels
            plt.ylabel("Flexibility price [€/kWh]", fontsize=font_size)
            # plt.xlabel("Time", fontsize=font_size)
            plt.title('Aggregated flex price', fontsize=font_size, pad=20)
            plt.xlim([0, N])
            plt.grid()
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
                plt.xticks(ts[::int(round(nsteps/req_ticks))], ts_hr[::int(round(nsteps/req_ticks))], rotation=0, fontsize=font_size)
            else:
                plt.xticks(ts, ts_hr, rotation=0, fontsize=font_size)       
                
            # Plot legend
            plt.legend(loc='lower left', bbox_to_anchor=(1.01, 0), fontsize=font_size)
            
            # Get dates
            date_index, N_dates = find_date_index(ts_date, N)
            for i in np.arange(N_dates):
                plt.text(date_index[i], -0.38, ts_date[int(date_index[i])], size=font_size-2)            
            
            # Axis labels
            plt.ylabel("Flexibility price [€/kWh]", fontsize=font_size)
            plt.xlabel("Time", fontsize=font_size)
            plt.title('Aggregated flex price', fontsize=font_size, pad=20)
            plt.xlim([0, nsteps])
            plt.grid()
            plt.tight_layout()
            plt.show()
    return

# Get text from dates
def find_date_index(date_series, N):
    date_list = date_series.values.tolist()
    date_list_offset = iter(date_list[1:])
    date_change_index = [i for i, j in enumerate(date_list[:-1], 1) if j != next(date_list_offset)]
    date_change_index_total = [0] + date_change_index + [N-1]
    _N_index = len(date_change_index_total) - 1
    _date_index = np.zeros(_N_index)
    for _i in np.arange(_N_index):
        _date_index[_i] = (date_change_index_total[_i] + date_change_index_total[_i+1]) / 2
    return _date_index, _N_index