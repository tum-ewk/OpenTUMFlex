# -*- coding: utf-8 -*-
"""
Created on Mon May 11 13:06:57 2020
@author: aditya
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec

def plot_reopt(my_ems):    
    print('Reoptimization Plot')   

    device=my_ems['reoptim']['device']
    nsteps = my_ems['time_data']['nsteps']
    ntsteps = my_ems['time_data']['ntsteps']
    t_intval = my_ems['time_data']['t_inval']
    dat1 = pd.DataFrame.from_dict(my_ems['flexopts'][device])
    dat2 =  pd.DataFrame.from_dict(my_ems['reoptim']['flexopts'][device])
    time_step = my_ems['reoptim']['timestep']
      
    # Initialize    
    neg_leg = 0
    pos_leg = 0
    font_size = 20
    fig = plt.figure(constrained_layout=True, figsize=(16, 12), dpi=80)
    spec = gridspec.GridSpec(ncols=1, nrows=4, figure=fig)
    plt_prc = fig.add_subplot(spec[3, 0])
    plt_pow = fig.add_subplot(spec[2, 0], sharex=plt_prc)
    plt_cum = fig.add_subplot(spec[0:2, 0], sharex=plt_prc)
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
            slot_flex = dat1['Neg_E'][x] / slots
            for y in range(1, slots + 1):
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
            slot_flex = dat1['Pos_E'][x] / slots
            for y in range(1, slots + 1):
                p3 = plt_cum.plot([ts[x + y - 1], ts[x + y]], [theta, cum_data.iloc[x + y, 0] + (slot_flex * y)],
                                  color='darkred')
                theta = cum_data.iloc[x + y, 0] + (slot_flex * y)
            p5 = plt_pow.bar(ts[x], dat1['Pos_P'][x], color='darkred', width=1.0, align='edge', edgecolor='k', zorder=3)
            p7 = plt_prc.bar(ts[x], dat1['Pos_Pr'][x], color='darkred', width=1.0, align='edge', edgecolor='k', zorder=3)

    
    #________________________________________________________________
    #STARTED EDITING FROM HERE @Aditya_SAWANT
    # tsr= #Time of timestep
    # tsr= #Time of reoptimization
    theta = 0
    # cum_data_reopt = pd.DataFrame(index=my_ems['time_data']['time_slots'], columns={'cumm'})
    # cum_data_reopt.iloc[0, 0] = 0
    cum_data_reopt=cum_data
    #print(cum_data_reopt.iloc[50:63,0])
    timestep = my_ems['reoptim']['timestep']
    
    #Check Flexibility offer is Negative or Poitive
    if my_ems['reoptim']['flextype'] == 'Neg' and (device == 'pv' or device == 'bat'):
        Energy = 'Neg_E'
        Power = 'Neg_P'
    elif my_ems['reoptim']['flextype'] == 'Pos' and device == 'bat':
        Energy = 'Pos_E'
        Power = 'Pos_P'
        
    for i in range(nsteps - 1):
        if i==my_ems['reoptim']['timestep'] and dat1['Neg_E'][i] <= 0 and dat1['Pos_E'][i] >= 0:
                neg_leg = 1
                theta = cum_data.iloc[i, 0]
                slots = int(round(ntsteps * dat1[Energy][i] / dat1[Power][i]))
                slot_flex = dat1[Energy][i] / slots
                for y in range(1, slots + 1):
                    p13 = plt_cum.plot([ts[i + y - 1], ts[i + y]], [theta, cum_data.iloc[i + y, 0] + (slot_flex * y)],
                                      linewidth=3,color='r') 
                    cum_data_reopt.iloc[i+y-1, 0]=cum_data.iloc[i + y, 0] + (slot_flex * y)             # created new data set for cumulative flexibility
                    theta = cum_data.iloc[i + y, 0] + (slot_flex * y)
        elif i>my_ems['reoptim']['timestep']+slots-1 and dat1['Neg_E'][i] <= 0 and dat1['Pos_E'][i] >= 0:
            cum_data_reopt.iloc[i, 0] = cum_data.iloc[i, 0]+my_ems['flexopts'][device][Energy][timestep]
    p8 = plt_cum.plot(cum_data_reopt.iloc[my_ems['reoptim']['timestep']+slots:(nsteps-1), 0], linewidth=3, color='y')
    
    
    
    index_re=my_ems['time_data']['isteps']
    for a in range(nsteps):
        if a>=index_re:                         #a is to get time stamp for Reoptimization data
            x=a-index_re                        #x is to get 0 to 77 value(Reoptimization dict)
            # Negative flexibility plots
            if dat2['Neg_E'][x] < 0:
                neg_leg = 1
                theta = cum_data.iloc[a, 0]
                slots = int(round(ntsteps * dat2['Neg_E'][x] / dat2['Neg_P'][x]))
                slot_flex = dat2['Neg_E'][x] / slots
                # for y in range(1, slots + 1):
                #     p2 = plt_cum.plot([ts[a + y - 1], ts[a + y]], [theta, cum_data_reopt.iloc[a + y, 0] + (slot_flex * y)],
                #                       color='y')                    
                #     theta = cum_data.iloc[a + y, 0] + (slot_flex * y)
            p9 = plt_pow.bar(ts[a], dat2['Neg_P'][x], color='m', width=1.0, align='edge', edgecolor='k', zorder=3)
            p11 = plt_prc.bar(ts[a], dat2['Neg_Pr'][x], color='m', width=1.0, align='edge', edgecolor='k', zorder=3)
            
            
            # Positive flexibility plots
            if dat2['Pos_E'][x] > 0:
                pos_leg = 1
                theta = cum_data.iloc[a, 0]
                slots = int(round(ntsteps * dat2['Pos_E'][x] / dat2['Pos_P'][x]))
                slot_flex = dat2['Pos_E'][x] / slots
                # for y in range(1, slots + 1):
                #     p3 = plt_cum.plot([ts[a + y - 1], ts[a + y]], [theta, cum_data.iloc[a + y, 0] + (slot_flex * y)],
                #                       color='y')
                #     theta = cum_data.iloc[a + y, 0] + (slot_flex * y)
                p10 = plt_pow.bar(ts[a], dat2['Pos_P'][x], color='y', width=1.0, align='edge', edgecolor='k', zorder=3)
                p12 = plt_prc.bar(ts[a], dat2['Pos_Pr'][x], color='y', width=1.0, align='edge', edgecolor='k', zorder=3)
    

    # Legend
    if neg_leg == 1 and pos_leg == 1:
        plt_cum.legend((p1[0], p2[0], p3[0],p8[0],p13[0]), ('Cummulative', 'Neg_flex', 'Pos_flex','New Optimal Exchange Energy','Called Flexibility Offer'),
                       prop={'size': font_size}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_pow.legend((p4, p5,p9,p10), ('$P_{Neg\_flex}}$', '$P_{Pos\_flex}}$','$P_{Neg\_flex}}$ for Reoptimization', '$P_{Pos\_flex}}$ for Reoptimization'),
                       prop={'size': font_size+2}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_prc.legend((p6, p7), ('$C_{Neg\_flex}}$', '$C_{Pos\_flex}}$'),
                       prop={'size': font_size+2}, bbox_to_anchor=(1.01, 0), loc="lower left")
    elif neg_leg == 1:
        plt_cum.legend((p1[0], p2[0],p8[0],p13[0]), ('Cummulative', 'Neg_flex','New Optimal Exchange Energy','Called Flexibility Offer'),
                       prop={'size': font_size}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_pow.legend(p4, ['$P_{Neg\_flex}}$'],
                       prop={'size': font_size+2}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_prc.legend(p6, ['$C_{Neg\_flex}}$'],
                       prop={'size': font_size+2}, bbox_to_anchor=(1.01, 0), loc="lower left")
    elif pos_leg == 1:
        plt_cum.legend((p1[0], p3[0],p8[0],p13[0]), ('Cummulative', 'Pos_flex','New Optimal Exchange Energy','Called Flexibility Offer'),
                       prop={'size': font_size}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_pow.legend((p5), ['$P_{Pos\_flex}}$'],
                       prop={'size': font_size+2}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_prc.legend((p7), ['$C_{Pos\_flex}}$'],
                       prop={'size': font_size+2}, bbox_to_anchor=(1.01, 0), loc="lower left")
    else:
        plt_cum.legend((p1[0],p8[0]), ('Cummulative','New Optimal Exchange Energy'),
                       prop={'size': font_size}, bbox_to_anchor=(1.01, 0), loc="lower left")      
    
    
    # Labels            
    # plt_cum.set_title('Flexibility plots', fontsize=font_size, pad=20)
    plt_cum.set_ylabel('$CE\ [kWh]$', fontsize=font_size+2)
    plt_cum.tick_params(axis="x", labelsize=font_size, labelbottom=False)
    plt_cum.tick_params(axis="y", labelsize=font_size)
    plt_cum.grid(color='lightgrey', linewidth=0.75)
    plt_pow.set_ylabel('$Power\ [kWh]$)', fontsize=font_size+2)
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