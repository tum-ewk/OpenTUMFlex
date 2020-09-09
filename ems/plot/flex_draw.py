# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 14:06:33 2019
@author: Babu Kumaran Nalini
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec

def plot_flex(my_ems, device):  
    nsteps = my_ems['time_data']['nsteps']
    ntsteps = my_ems['time_data']['ntsteps']
    t_intval = my_ems['time_data']['t_inval']
    dat1 = pd.DataFrame.from_dict(my_ems['flexopts'][device])
      
    # Initialize    
    neg_leg = 0
    pos_leg = 0
    font_size = 20
    fig = plt.figure(constrained_layout=True, figsize=(16, 12), dpi=80)
    spec = gridspec.GridSpec(ncols=1, nrows=4, figure=fig)
    plt_prc = fig.add_subplot(spec[3, 0])
    plt_pow = fig.add_subplot(spec[2, 0], sharex=plt_prc)
    plt_cum = fig.add_subplot(spec[0:2, 0], sharex=plt_prc)
    #ts = my_ems['time_data']['time_slots'].tolist()
    ts = my_ems['time_data']['time_slots']

    # Plotting cummulative energy exchange
    theta = 0
    # cum_data = pd.DataFrame(
    #     index=pd.date_range(start="00:00", end="23:59",
    #     freq=str(t_intval) + 'min').strftime('%H:%M'), columns={'cumm'})
    cum_data = pd.DataFrame(
             index=my_ems['time_data']['time_slots'], columns={'cumm'})
    cum_data.iloc[0, 0] = 0
    for i in range(nsteps - 1):
        cum_data.iloc[i + 1, 0] = theta + dat1['Sch_P'][i]/ntsteps
        theta = cum_data.iloc[i + 1, 0]
    p1 = plt_cum.plot(cum_data.iloc[:, 0], linewidth=3, color='k')
    
    for x in range(nsteps):
        # Negative flexibility plots
        if dat1['Neg_E'][x] < 0:
            neg_leg = 1
            theta = cum_data.iloc[x, 0]
            slots = int(round(ntsteps * dat1['Neg_E'][x] / dat1['Neg_P'][x]))
            slots_lim = slots
            if x + slots >= nsteps:
                slots_lim = nsteps-x-1
            slot_flex = dat1['Neg_E'][x] / slots
            for y in range(1, slots_lim + 1):
                p2 = plt_cum.plot([ts[x + y - 1], ts[x + y]], [theta, cum_data.iloc[x + y, 0] + (slot_flex * y)],
                                  color='tab:blue')
                theta = cum_data.iloc[x + y, 0] + (slot_flex * y)
        p4 = plt_pow.bar(ts[x], dat1['Neg_P'][x], color='tab:blue', width=1.0, align='edge', edgecolor='k', zorder=3)
        p6 = plt_prc.bar(ts[x], dat1['Neg_Pr'][x], color='tab:blue', width=1.0, align='edge', edgecolor='k', zorder=3)
        
        # Positive flexibility plots
        if dat1['Pos_E'][x] > 0:
            pos_leg = 1
            theta = cum_data.iloc[x, 0]
            slots = int(round(ntsteps * dat1['Pos_E'][x] / dat1['Pos_P'][x]))
            slots_lim = slots
            if x + slots >= nsteps:
                slots_lim = nsteps-x-1
            slot_flex = dat1['Pos_E'][x] / slots
            for y in range(1, slots_lim + 1):
                p3 = plt_cum.plot([ts[x + y - 1], ts[x + y]], [theta, cum_data.iloc[x + y, 0] + (slot_flex * y)],
                                  color='darkred')
                theta = cum_data.iloc[x + y, 0] + (slot_flex * y)
            p5 = plt_pow.bar(ts[x], dat1['Pos_P'][x], color='darkred', width=1.0, align='edge', edgecolor='k', zorder=3)
            p7 = plt_prc.bar(ts[x], dat1['Pos_Pr'][x], color='darkred', width=1.0, align='edge', edgecolor='k', zorder=3)

    # Legend
    if neg_leg == 1 and pos_leg == 1:
        plt_cum.legend((p1[0], p2[0], p3[0]), ('Cummulative', 'Neg_flex', 'Pos_flex'),
                       prop={'size': font_size}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_pow.legend((p4, p5), ('$P_{Neg\_flex}}$', '$P_{Pos\_flex}}$'),
                       prop={'size': font_size+2}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_prc.legend((p6, p7), ('$C_{Neg\_flex}}$', '$C_{Pos\_flex}}$'),
                       prop={'size': font_size+2}, bbox_to_anchor=(1.01, 0), loc="lower left")
    elif neg_leg == 1:
        plt_cum.legend((p1[0], p2[0]), ('Cummulative', 'Neg_flex'),
                       prop={'size': font_size}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_pow.legend(p4, ['$P_{Neg\_flex}}$'],
                       prop={'size': font_size+2}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_prc.legend(p6, ['$C_{Neg\_flex}}$'],
                       prop={'size': font_size+2}, bbox_to_anchor=(1.01, 0), loc="lower left")
    elif pos_leg == 1:
        plt_cum.legend((p1[0], p3[0]), ('Cummulative', 'Pos_flex'),
                       prop={'size': font_size}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_pow.legend((p5), ['$P_{Pos\_flex}}$'],
                       prop={'size': font_size+2}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_prc.legend((p7), ['$C_{Pos\_flex}}$'],
                       prop={'size': font_size+2}, bbox_to_anchor=(1.01, 0), loc="lower left")
    else:
        plt_cum.legend(['Cummulative'], prop={'size': font_size+2})

    # Labels            
    # plt_cum.set_title('Flexibility plots', fontsize=font_size, pad=20)
    plt_cum.set_ylabel('$CE\ [kWh]$', fontsize=font_size+2)
    plt_cum.tick_params(axis="x", labelsize=font_size, labelbottom=False)
    plt_cum.tick_params(axis="y", labelsize=font_size)
    plt_cum.grid(color='lightgrey', linewidth=0.75)
    plt_pow.set_ylabel('$Power\ [kW]$', fontsize=font_size+2)
    plt_pow.tick_params(axis="x", labelsize=font_size, labelbottom=False)
    plt_pow.tick_params(axis="y", labelsize=font_size)
    plt_pow.grid(color='lightgrey', linewidth=0.75, zorder=0)
    plt_prc.set_xlabel('Time', fontsize=font_size, labelpad=3)
    plt_prc.set_ylabel('$Price\ [€/kWh]$', fontsize=font_size+2)
    plt_prc.tick_params(axis="x", labelsize=font_size, pad=5)
    plt_prc.tick_params(axis="y", labelsize=font_size)
    plt_prc.grid(color='lightgrey', linewidth=0.75, zorder=0)
    fig.align_labels()

    # limits
    lim_a = abs(1.5 * dat1['Neg_P'].min())
    lim_b = abs(1.5 * dat1['Pos_P'].max())
    lim_ends = max(lim_a, lim_b)
    if lim_ends != 0:
        plt_pow.set_ylim(-lim_ends, lim_ends)
    lim_a = abs(1.5 * dat1['Neg_Pr'].min())
    lim_b = abs(1.5 * dat1['Pos_Pr'].max())
    lim_ends = max(lim_a, lim_b)
    if lim_ends != 0:
        plt_prc.set_ylim(-lim_ends, lim_ends)
    #    plt_prc.set_xlim(0, nsteps+1)

    # Horizontal line - bar plot
    plt_pow.axhline(y=0, linewidth=2, color='k')
    plt_prc.axhline(y=0, linewidth=2, color='k')

    # Change xtick intervals    
    req_ticks = 12   # ticks needed
    if nsteps > req_ticks:
        plt_prc.set_xticks(plt_prc.get_xticks()[::int(round(nsteps/req_ticks))])
        plt_prc.set_xticklabels(ts[::int(round(nsteps/req_ticks))], rotation=-45, ha="left")
    else:
        plt_prc.set_xticks(plt_prc.get_xticks())
        plt_prc.set_xticklabels(ts, rotation=-45, ha="left")        

    # Settings
    plt.rc('font', family='serif')
    plt.margins(x=0)
    plt.show()   
    return 

def save_results(dat1, nsteps, save_path):
    dat1.to_excel("output.xlsx", sheet_name='flex_results')


# from ems.plot.flex_draw1 import plot_flex as plot
# if __name__ == "__main__":
#    plot(my_ems, 'bat')
