# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 14:06:33 2019

@author: ga47jes
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec


def plot_flex(my_ems, device):
    nsteps = my_ems['time_data']['nsteps']
    ntsteps = my_ems['time_data']['ntsteps']
    dat1 = pd.DataFrame.from_dict(my_ems['flexopts'][device])
    neg_leg = 0
    pos_leg = 0
    fig = plt.figure(constrained_layout=True, figsize=(8, 5), dpi=80)
    spec = gridspec.GridSpec(ncols=1, nrows=4, figure=fig)
    plt_prc = fig.add_subplot(spec[3, 0])
    plt_pow = fig.add_subplot(spec[2, 0], sharex=plt_prc)
    plt_cum = fig.add_subplot(spec[0:2, 0], sharex=plt_prc)

    # Plotting cummulative energy exchange
    theta = 0
    cum_data = [0] * (nsteps + 1)
    for i in range(nsteps):
        cum_data[i + 1] = theta + dat1.iloc[i, 0] /ntsteps
        theta = cum_data[i + 1]
    p1 = plt_cum.plot(cum_data, linewidth=2, color='k')

    for x in range(nsteps):
        # Negative flexibility plots
        if dat1.iloc[x, 3] < 0:
            neg_leg = 1
            theta = cum_data[x]

            slots = int(round(ntsteps * dat1.iloc[x, 3] / dat1.iloc[x, 1]))

            slot_flex = dat1.iloc[x, 3] / slots
            for y in range(1, slots + 1):
                p2 = plt_cum.plot([x + y - 1, x + y], [theta, cum_data[x + y] + (slot_flex * y)], color='b')
                theta = cum_data[x + y] + (slot_flex * y)
            p4 = plt_pow.bar(x, dat1.iloc[x, 1], color='b', width=1.0, align='edge')
            p6 = plt_prc.bar(x, dat1.iloc[x, 5], color='b', width=1.0, align='edge')

        # Positive flexibility plots
        if dat1.iloc[x, 4] > 0:
            pos_leg = 1
            theta = cum_data[x]
            slots = int(round(ntsteps * dat1.iloc[x, 4] / dat1.iloc[x, 2]))
            slot_flex = dat1.iloc[x, 4] / slots
            for y in range(1, slots + 1):
                p3 = plt_cum.plot([x + y - 1, x + y], [theta, cum_data[x + y] + (slot_flex * y)], color='r')
                theta = cum_data[x + y] + (slot_flex * y)
            p5 = plt_pow.bar(x, dat1.iloc[x, 2], color='r', width=1.0, align='edge')
            p7 = plt_prc.bar(x, dat1.iloc[x, 6], color='r', width=1.0, align='edge')

    # Legend
    if neg_leg == 1 and pos_leg == 1:
        plt_cum.legend((p1[0], p2[0], p3[0]), ('Cummulative', 'Neg_flex', 'Pos_flex'),
                       prop={'size': 14}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_pow.legend((p4, p5), ('$P_{Neg\_flex}}$', '$P_{Pos\_flex}}$'),
                       prop={'size': 14}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_prc.legend((p6, p7), ('$C_{Neg\_flex}}$', '$C_{Pos\_flex}}$'),
                       prop={'size': 14}, bbox_to_anchor=(1.01, 0), loc="lower left")
    elif neg_leg == 1:
        plt_cum.legend((p1[0], p2[0]), ('Cummulative', 'Neg_flex'),
                       prop={'size': 14}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_pow.legend(p4, ['$P_{Neg\_flex}}$'],
                       prop={'size': 14}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_prc.legend(p6, ['$C_{Neg\_flex}}$'],
                       prop={'size': 14}, bbox_to_anchor=(1.01, 0), loc="lower left")
    elif pos_leg == 1:
        plt_cum.legend((p1[0], p3[0]), ('Cummulative', 'Pos_flex'),
                       prop={'size': 14}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_pow.legend((p5), ['$P_{Pos\_flex}}$'],
                       prop={'size': 14}, bbox_to_anchor=(1.01, 0), loc="lower left")
        plt_prc.legend((p7), ['$C_{Pos\_flex}}$'],
                       prop={'size': 14}, bbox_to_anchor=(1.01, 0), loc="lower left")
    else:
        plt_cum.legend((p1[0]), ('Cummulative'),
                       prop={'size': 14}, bbox_to_anchor=(1.01, 0), loc="lower left")

    # Labels
    plt_cum.set_title('Flexibility plots', fontsize=16)
    plt_cum.set(ylabel='CE(kWh)')
    plt_cum.grid(True)
    plt_pow.set(ylabel='Power(kWh)')
    plt_pow.grid(True)
    plt_prc.set(xlabel='Time slot', ylabel='Price(€/kWh)')
    plt_prc.grid(True)

    # limits
    lim_a = abs(1.1 * dat1.iloc[:, 1].min())
    lim_b = abs(1.1 * dat1.iloc[:, 2].max())
    lim_ends = max(lim_a, lim_b)
    if lim_ends != 0:
        plt_pow.set_ylim(-lim_ends, lim_ends)
    lim_a = abs(1.1 * dat1.iloc[:, 5].min())
    lim_b = abs(1.1 * dat1.iloc[:, 6].max())
    lim_ends = max(lim_a, lim_b)
    if lim_ends != 0:
        plt_prc.set_ylim(-lim_ends, lim_ends)
    plt.show()


def save_results(dat1, save_path, nsteps = 24):
    dat1.to_csv(save_path, index=False, sep=';')
