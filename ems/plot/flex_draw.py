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
    neg_leg = 0
    pos_leg = 0    
    fig = plt.figure(constrained_layout=True, figsize=(16, 12), dpi=80)
    spec = gridspec.GridSpec(ncols=1, nrows=4, figure=fig)
    plt_prc = fig.add_subplot(spec[3, 0])
    plt_pow = fig.add_subplot(spec[2, 0], sharex=plt_prc)   
    plt_cum = fig.add_subplot(spec[0:2, 0], sharex=plt_prc) 
    ts = pd.date_range(start="00:00", end="23:59", freq=str(t_intval)+'min').strftime('%H:%M').tolist()

    # Plotting cummulative energy exchange
    theta = 0
    cum_data = pd.DataFrame(index=pd.date_range(start="00:00", end="23:59", freq=str(t_intval)+'min').strftime('%H:%M'), columns={'cumm'})
    cum_data.iloc[0,0] = 0
    for i in range(nsteps-1):
        cum_data.iloc[i+1,0] = theta + dat1.iloc[i,0]/ntsteps
        theta = cum_data.iloc[i+1,0]   
    p1 = plt_cum.plot(cum_data.iloc[:,0], linewidth=3, color='k')   
        
    for x in range(nsteps):
        # Negative flexibility plots
        if dat1.iloc[x,3] < 0:
            neg_leg = 1
            theta = cum_data.iloc[x,0]
            slots = int(round(ntsteps*dat1.iloc[x,3]/dat1.iloc[x,1]))  
            slot_flex = dat1.iloc[x,3]/slots
            for y in range(1,slots+1):
                p2 = plt_cum.plot([ts[x+y-1],ts[x+y]],[theta, cum_data.iloc[x+y,0]+(slot_flex*y)], color='tab:blue')
                theta = cum_data.iloc[x+y,0]+(slot_flex*y)
        p4 = plt_pow.bar(ts[x],dat1.iloc[x,1], color='tab:blue', width=1.0, align='edge', edgecolor='k', zorder=3)
        p6 = plt_prc.bar(ts[x],dat1.iloc[x,5], color='tab:blue', width=1.0, align='edge', edgecolor='k', zorder=3)
       
        # Positive flexibility plots
        if dat1.iloc[x,4] > 0:
            pos_leg = 1
            theta = cum_data.iloc[x,0]
            slots = int(round(ntsteps*dat1.iloc[x,4]/dat1.iloc[x,2]))  
            slot_flex = dat1.iloc[x,4]/slots
            for y in range(1,slots+1):
                p3 = plt_cum.plot([ts[x+y-1],ts[x+y]],[theta, cum_data.iloc[x+y,0]+(slot_flex*y)], color='darkred')
                theta = cum_data.iloc[x+y,0]+(slot_flex*y)
            p5 = plt_pow.bar(ts[x],dat1.iloc[x,2], color='darkred', width=1.0, align='edge', edgecolor='k', zorder=3)
            p7 = plt_prc.bar(ts[x],dat1.iloc[x,6], color='darkred', width=1.0, align='edge', edgecolor='k', zorder=3)
            
    # Legend
    if neg_leg==1 and pos_leg==1:
        plt_cum.legend((p1[0], p2[0], p3[0]),('Cummulative', 'Neg_flex', 'Pos_flex'),
                prop={'size': 20}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_pow.legend((p4, p5), ('$P_{Neg\_flex}}$', '$P_{Pos\_flex}}$'),
                prop={'size': 22}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_prc.legend((p6, p7), ('$C_{Neg\_flex}}$', '$C_{Pos\_flex}}$'),
                prop={'size': 22}, bbox_to_anchor=(1.01, 0), loc="lower left") 
    elif neg_leg==1:
        plt_cum.legend((p1[0], p2[0]),('Cummulative', 'Neg_flex'),
                prop={'size': 20}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_pow.legend(p4, ['$P_{Neg\_flex}}$'], 
                prop={'size': 22}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_prc.legend(p6, ['$C_{Neg\_flex}}$'],
                prop={'size': 18}, bbox_to_anchor=(1.01, 0), loc="lower left")
    elif pos_leg==1:
        plt_cum.legend((p1[0], p3[0]),('Cummulative', 'Pos_flex'),
                prop={'size': 20}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_pow.legend((p5), ['$P_{Pos\_flex}}$'],
                prop={'size': 22}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_prc.legend((p7), ['$C_{Pos\_flex}}$'],
                prop={'size': 22}, bbox_to_anchor=(1.01, 0), loc="lower left")
    else:
        plt_cum.legend((p1[0]),('Cummulative'),
                prop={'size': 20}, bbox_to_anchor=(1.01, 0), loc="lower left")
          
    # Labels            
    plt_cum.set_title('Flexibility plots', fontsize=24, pad=20)
    plt_cum.set_ylabel('$CE\ [kWh]$', fontsize=20)
    plt_cum.tick_params(axis="x", labelsize=16, labelbottom=False)
    plt_cum.tick_params(axis="y", labelsize=16)
    plt_cum.grid(color='lightgrey', linewidth=0.75)
    plt_pow.set_ylabel('$Power\ [kWh]$)', fontsize=20)
    plt_pow.tick_params(axis="x", labelsize=16, labelbottom=False)
    plt_pow.tick_params(axis="y", labelsize=16)
    plt_pow.grid(color='lightgrey', linewidth=0.75, zorder=0)
    plt_prc.set_xlabel('Time', fontsize=20, labelpad=3)
    plt_prc.set_ylabel('$Price\ [€/kWh]$', fontsize=20)
    plt_prc.tick_params(axis="x", labelsize=16, pad=5)
    plt_prc.tick_params(axis="y", labelsize=16)
    plt_prc.grid(color='lightgrey', linewidth=0.75, zorder=0)
    fig.align_labels() 
          
    #limits    
    lim_a = abs(1.5*dat1.iloc[:,1].min())
    lim_b = abs(1.5*dat1.iloc[:,2].max())
    lim_ends = max(lim_a, lim_b)
    if lim_ends != 0:
        plt_pow.set_ylim(-lim_ends,lim_ends)
    lim_a = abs(1.5*dat1.iloc[:,5].min())
    lim_b = abs(1.5*dat1.iloc[:,6].max())  
    lim_ends = max(lim_a, lim_b)
    if lim_ends != 0:
        plt_prc.set_ylim(-lim_ends,lim_ends)
#    plt_prc.set_xlim(0, nsteps+1)
   
    # Horizontal line - bar plot
    plt_pow.axhline(y=0, linewidth=2, color='k')
    plt_prc.axhline(y=0, linewidth=2, color='k')
    
    # Change xtick intervals    
    plt_prc.set_xticks(plt_prc.get_xticks()[::4])
    
    # Settings
    plt.rc('font', family='serif')
    plt.margins(x=0)
    plt.show()

def save_results(dat1, nsteps, save_path):
    dat1.to_excel("output.xlsx",sheet_name='flex_results')      

#from ems.plot.flex_draw1 import plot_flex as plot
#if __name__ == "__main__":
#    plot(my_ems, 'bat')
