import matplotlib.pyplot as plt
import numpy as np


def plot_results(ems, prnt_pgr=False):
    # plot electricity balance
    # ts = ems_local['time_data']['time_slots'].tolist()
    isteps = ems['time_data']['isteps']
    nsteps = ems['time_data']['nsteps']
    timesteps = np.arange(ems['time_data']['isteps'], ems['time_data']['nsteps'])
    N = len(timesteps)
    ind = np.arange(N)  # the x locations for the groups
    ts = ems['time_data']['time_slots'][isteps:nsteps]
    ts = np.asarray(ts)
    # ind = ems_local['time_data']['time_slots'].tolist()
    width = 1  # the width of the bars: can also be len(x) sequence

    # obtain the optimization results from ems
    opt_res = ems['optplan']
    for param in opt_res:
        opt_res[param] = np.array(opt_res[param])

    if prnt_pgr:
        print('Optimized electricity net cost (€):', sum(opt_res['opt_ele_price']))
        print('Results Loaded.' + '\n')

    # figure properties
    fig = plt.figure(figsize=(10, 6))
    plt.rc('font', family='serif')
    font_size = 16
    # plots
    p1 = plt.bar(ind, opt_res['CHP_elec_pow'], width, bottom=opt_res['bat_output_power'],
                 color='skyblue', align='edge')
    p2 = plt.bar(ind, opt_res['PV_power'], width, bottom=opt_res['bat_output_power'] + opt_res['CHP_elec_pow'],
                 color='goldenrod', align='edge')
    p3 = plt.bar(ind, opt_res['bat_output_power'], width, color='indianred', align='edge')
    p4 = plt.bar(ind, -opt_res['bat_input_power'], width, color='indianred', align='edge')
    p5 = plt.bar(ind, opt_res['grid_import'], width,
                 bottom=opt_res['bat_output_power'] + opt_res['CHP_elec_pow'] + opt_res['PV_power'],
                 color='grey', align='edge')
    p6 = plt.bar(ind, -opt_res['grid_export'], width, bottom=-opt_res['bat_input_power'],
                 color='darkseagreen', align='edge')
    p7 = plt.step(ind, opt_res['Last_elec'], linewidth=2, where='post', color='k')
    p8 = plt.bar(ind, -opt_res['EV_power'], width, bottom=-opt_res['bat_input_power']-opt_res['grid_export'],
                 color='plum', align='edge')
    p9 = plt.bar(ind, -opt_res['HP_elec_power'], width,
                 bottom=-opt_res['bat_input_power'] - opt_res['grid_export'] - np.array(opt_res['EV_power']),
                 color='wheat', align='edge')
    # xticks
    ax = plt.gca()
    ax.axhline(linewidth=2, color="black")
    idx_plt = np.arange(0, N, int(N / 5))
    plt.xticks(ind[idx_plt], ts[idx_plt], rotation=20)
    plt.tick_params(axis="x", labelsize=font_size - 2)
    plt.tick_params(axis="y", labelsize=font_size - 2)
    # labels
    plt.xlabel('Time [h]', fontsize=font_size)
    plt.ylabel('Electrical demand [kW]', fontsize=font_size)
    plt.title('Electricity Balance', fontsize=20)
    plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0], p6[0], p7[0], p8[0], p9[0]),
               ('CHP', 'PV', 'Bat_Discharge', 'Bat_Charge', 'Import', 'Export', 'E_Demand', 'EV_charge', 'HP'),
               prop={'size': font_size - 2}, bbox_to_anchor=(1.01, 0), loc="lower left")
    # plot properties
    plt.grid(color='lightgrey', linewidth=0.75)
    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.margins(x=0)
    plt.show()

    fig1 = plt.figure()
    ax2 = plt.subplot()
    # p8 = plt.plot(ind, bat_cont/bat_max_cont*100,linewidth=1,color='red')

    p8 = plt.step(ind, opt_res['SOC_elec'], linewidth=1, color='red', where='mid')
    plt.xlabel('time [h]', fontsize=font_size)
    plt.ylabel('SOC [%]', fontsize=font_size)
    plt.title('SOC of Battery', fontsize=font_size)
    plt.xticks(ind[idx_plt], ts[idx_plt], rotation=20)
    ax2.set_xlim(0, N - 1)
    plt.show()

    # plot EV soc
    fig1 = plt.figure()
    ax3 = plt.subplot()
    # p8 = plt.plot(ind, bat_cont/bat_max_cont*100,linewidth=1,color='red')

    p8 = plt.step(ind, opt_res['EV_SOC'], linewidth=1, color='red', where='mid')
    plt.xlabel('time [h]', fontsize=font_size)
    plt.ylabel('SOC [%]', fontsize=font_size)
    plt.title('SOC of EV', fontsize=font_size)
    plt.xticks(ind[idx_plt], ts[idx_plt], rotation=20)
    ax2.set_xlim(0, N - 1)
    plt.show()

    #  plot heat balance
    # plots
    fig = plt.figure(figsize=(10, 6))
    plt.rc('font', family='serif')
    font_size = 16
    p1 = plt.bar(ind, opt_res['boiler_heat_power'], width, bottom=opt_res['sto_heat_power_pos'], color='grey')
    p2 = plt.bar(ind, opt_res['CHP_heat_pow'], width,
                 bottom=opt_res['boiler_heat_power'] + opt_res['sto_heat_power_pos'], color='skyblue')
    p3 = plt.bar(ind, opt_res['HP_heat_power'], width,
                 bottom=opt_res['boiler_heat_power'] + opt_res['CHP_heat_pow'] + opt_res['sto_heat_power_pos'],
                 color='wheat')
    p4 = plt.bar(ind, opt_res['sto_heat_power_pos'], width, color='indianred')
    p5 = plt.bar(ind, opt_res['sto_heat_power_neg'], width, color='indianred')
    p6 = plt.step(ind, opt_res['Last_heat'], linewidth=2, where='mid', color='k')

    # xticks
    ax = plt.gca()
    ax.axhline(linewidth=2, color="black")
    idx_plt = np.arange(0, N, int(N / 5))
    plt.xticks([0, 24, 2, 2], fontsize=font_size)
    plt.tick_params(axis="x", labelsize=font_size - 2)
    plt.tick_params(axis="y", labelsize=font_size - 2)
    plt.xlabel('time [1/4 h]', fontsize=font_size)
    plt.ylabel('Heat Load [kW]', fontsize=font_size)
    plt.title('Heat Balance', fontsize=font_size)
    plt.legend((p1[0], p2[0], p3[0], p4[0], p6[0]), ('boiler', 'CHP', 'HP', 'heat storage', 'heat demand'),
               prop={'size': font_size}, bbox_to_anchor=(1.01, 0), loc='lower left')

    # plot properties
    plt.grid(color='lightgrey', linewidth=0.75)
    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.margins(x=0)
    plt.show()

    fig1 = plt.figure()
    ax2 = plt.subplot()
    p7 = plt.step(ind, opt_res['SOC_heat'], linewidth=1, where='mid', color='red')
    plt.xlabel('time [h]', fontsize=font_size)
    plt.ylabel('SOC [%]', fontsize=font_size)
    plt.xticks(ind[idx_plt], ts[idx_plt], rotation=20)
    ax2.set_xlim(0, N - 1)
    plt.title('SOC of Heat Storage', fontsize=20)
    plt.show()
