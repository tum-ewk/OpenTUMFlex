import matplotlib.pyplot as plt
import numpy as np
import datetime
import pandas as pd
import math


def plot_optimal_results(ems, prnt_pgr=False, show_balance=True, show_soc=True):
    """ visualize the optimization results based on ems dict
    Args:
        - ems: ems dict with optimization results
        - prnt_pgr: (to be finished by Babu)

    """
    # plot electricity balance
    # ts = ems_local['time_data']['time_slots'].tolist()
    isteps = ems['time_data']['isteps']
    nsteps = ems['time_data']['nsteps']
    timesteps = np.arange(ems['time_data']['isteps'], ems['time_data']['nsteps'])
    N = len(timesteps)
    ind = np.arange(N)  # the x locations for the groups
    indplus1 = np.arange(N+1)  # extra index series for step plot
    ts_raw = ems['time_data']['time_slots'][isteps:nsteps]
    ts = pd.to_datetime(ts_raw).strftime('%H:%M')
    ts_date = pd.to_datetime(ts_raw).strftime('%d %b %Y')

    # ind = ems_local['time_data']['time_slots'].tolist()
    width = 1  # the width of the bars: can also be len(x) sequence

    # obtain the optimization results from ems dict
    opt_res = ems['optplan']
    for param in opt_res:
        opt_res[param] = np.array(opt_res[param])

    if prnt_pgr:
        print('Optimized electricity net cost (€):', sum(opt_res['opt_ele_price']))
        print('Results Loaded.' + '\n')

    if show_balance:
        # figure properties
        fig, axs = plt.subplots(2, 1, figsize=(10, 7))
        # fig = plt.figure(figsize=(10, 6))
        plt.rc('font', family='serif')
        font_size = 16
        # plots
        ax1 = axs[0]
        p1 = ax1.bar(ind, opt_res['CHP_elec_pow'], width, bottom=opt_res['bat_output_power'],
                color='skyblue', align='edge')
        p2 = ax1.bar(ind, opt_res['PV_power'], width, bottom=opt_res['bat_output_power'] + opt_res['CHP_elec_pow'],
                color='goldenrod', align='edge')
        p3 = ax1.bar(ind, opt_res['bat_output_power'], width, color='indianred', align='edge')
        p4 = ax1.bar(ind, -opt_res['bat_input_power'], width, color='indianred', align='edge')
        p5 = ax1.bar(ind, opt_res['grid_import'], width,
                bottom=opt_res['bat_output_power'] + opt_res['CHP_elec_pow'] + opt_res['PV_power'],
                color='grey', align='edge')
        p6 = ax1.bar(ind, -opt_res['grid_export'], width, bottom=-opt_res['bat_input_power'],
                color='darkseagreen', align='edge')
        p7 = ax1.bar(ind, -opt_res['EV_power'], width, bottom=-opt_res['bat_input_power'] - opt_res['grid_export'],
                color='plum', align='edge')
        p8 = ax1.bar(ind, -opt_res['HP_elec_power'], width,
                bottom=-opt_res['bat_input_power'] - opt_res['grid_export'] - np.array(opt_res['EV_power']),
                color='wheat', align='edge')
        p9 = ax1.step(indplus1, np.append(opt_res['Last_elec'], 0), linewidth=2, where='post', color='k')

        # xticks
        # ax1 = plt.gca()
        ax1.axhline(linewidth=2, color="black")
        idx_plt = (np.linspace(0, N - 1, 5, endpoint=True)).astype(int)

        # labels and ticks
        # ax1.set_xlabel('Time [h]', fontsize=font_size)
        ax1.tick_params(axis="x", labelsize=font_size - 2)
        ax1.tick_params(axis="y", labelsize=font_size - 2)
        ax1.set_ylabel('Electrical demand [kW]', fontsize=font_size)
        ax1.set_title('Electricity balance', fontsize=font_size)
        ax1.set_xticks(ind[idx_plt])
        ax1.set_xticklabels(ts[idx_plt])
        plt.setp(ax1.get_xticklabels(), visible=False)
        # select which legends are to be shown
        selector = {np.count_nonzero(opt_res['CHP_elec_pow']): [p1[0], 'CHP'],
                    np.count_nonzero(opt_res['PV_power']): [p2[0], 'PV'],
                    np.count_nonzero(opt_res['bat_output_power'] + opt_res['bat_input_power']): [p3[0], 'Battery'],
                    np.count_nonzero(opt_res['grid_import']): [p5[0], 'Grid_import'],
                    np.count_nonzero(opt_res['grid_export']): [p6[0], 'Grid_export'],
                    np.count_nonzero(opt_res['EV_power']): [p7[0], 'EV'],
                    np.count_nonzero(opt_res['HP_elec_power']): [p8[0], 'HP'],
                    }
        legend_entries = [p9[0]]
        labels_entries = ['Electrical load']
        for count_nonzero, legend_entry in selector.items():
            if count_nonzero > 0:
                legend_entries.append(legend_entry[0])
                labels_entries.append(legend_entry[1])
        ax1.legend(legend_entries, labels_entries,
                   prop={'size': font_size - 4}, bbox_to_anchor=(1.01, 0), loc="lower left", frameon=False)
        # plot properties
        ax1.grid(color='lightgrey', linewidth=0.75)
        # adjust the y-axis limit
        bottom, top = ax1.get_ylim()
        if top >= abs(bottom):
            ax1.set_ylim(-(top + 0.5), top + 0.5)
        else:
            ax1.set_ylim(bottom - 0.5, -(bottom - 0.5))
        # plt.tight_layout(rect=[0, 0, 1, 1])
        ax1.margins(x=0)

        #  plot heat balance
        # plots
        # plt.subplot(2, 1, 2)
        # fig = plt.figure(figsize=(10, 6))
        plt.rc('font', family='serif')
        font_size = 16
        ax2 = axs[1]
        p1 = ax2.bar(ind, opt_res['boiler_heat_power'], width, bottom=opt_res['sto_heat_power_pos'], color='grey',
                     align='edge')
        p2 = ax2.bar(ind, opt_res['CHP_heat_pow'], width,
                     bottom=opt_res['boiler_heat_power'] + opt_res['sto_heat_power_pos'], color='skyblue', align='edge')
        p3 = ax2.bar(ind, opt_res['HP_heat_power'], width,
                     bottom=opt_res['boiler_heat_power'] + opt_res['CHP_heat_pow'] + opt_res['sto_heat_power_pos'],
                     color='wheat', align='edge')
        p4 = ax2.bar(ind, opt_res['sto_heat_power_pos'], width, color='indianred', align='edge')
        p5 = ax2.bar(ind, opt_res['sto_heat_power_neg'], width, color='indianred', align='edge')
        p6 = ax2.step(indplus1, np.append(opt_res['Last_heat'], 0), linewidth=2, where='post', color='k')

        # xticks
        ax2 = plt.gca()
        ax2.axhline(linewidth=2, color="black")
        # idx_plt = np.arange(0, N, int(N / 5))
        ax2.set_xticks(ind[idx_plt])
        ax2.set_xticklabels(ts[idx_plt])
        ax2.tick_params(axis="x", labelsize=font_size - 2)
        ax2.tick_params(axis="y", labelsize=font_size - 2)
        # ax2.set_xlabel('time [1/4 h]', fontsize=font_size)
        ax2.set_ylabel('Heat load [kW]', fontsize=font_size)
        ax2.set_title('Heat balance', fontsize=font_size)
        # select which legends are to be shown
        selector = {np.count_nonzero(opt_res['boiler_heat_power']): [p1[0], 'Boiler'],
                    np.count_nonzero(opt_res['CHP_heat_pow']): [p2[0], 'CHP'],
                    np.count_nonzero(opt_res['HP_heat_power']): [p3[0], 'HP'],
                    np.count_nonzero(opt_res['sto_heat_power_pos']+opt_res['sto_heat_power_neg']): [p4[0], 'Heat storage']
                    }
        legend_entries = [p6[0]]
        labels_entries = ['Heat load']
        for count_nonzero, legend_entry in selector.items():
            if count_nonzero > 0:
                legend_entries.append(legend_entry[0])
                labels_entries.append(legend_entry[1])
        ax2.legend(legend_entries, labels_entries,
                   prop={'size': font_size-4}, bbox_to_anchor=(1.01, 0), loc='lower left', frameon=False)

        # draw text of dates
        def find_date_index(date_series):
            _N = len(date_series)
            date_list = date_series.values.tolist()
            date_list_offset = iter(date_list[1:])
            date_change_index = [i for i, j in enumerate(date_list[:-1], 1) if j != next(date_list_offset)]
            date_change_index_total = [0] + date_change_index + [N-1]
            _N_index = len(date_change_index_total) - 1
            _date_index = np.zeros(_N_index)
            for _i in np.arange(_N_index):
                _date_index[_i] = (date_change_index_total[_i] + date_change_index_total[_i+1]) / 2
            return _date_index, _N_index
        date_index, N_dates = find_date_index(ts_date)
        for i in np.arange(N_dates):
            ax2.text(date_index[i], -15, ts_date[int(date_index[i])], size=font_size-2)

        # plot properties
        ax2.grid(color='lightgrey', linewidth=0.75)
        # adjust the y-axis limit
        bottom, top = ax2.get_ylim()
        if top >= abs(bottom):
            ax2.set_ylim(-(top + 0.5), top + 0.5)
        else:
            ax2.set_ylim(bottom - 0.5, -(bottom - 0.5))
        # fig.tight_layout(rect=[0, 0, 1, 1])
        ax2.margins(x=0)
        fig.align_ylabels(axs[:])
        plt.tight_layout()

    if show_soc:
        # plot SoC of battery
        fig1 = plt.figure()
        ax2 = plt.subplot(1, 3, 1)
        font_size = 16
        # p8 = plt.plot(ind, bat_cont/bat_max_cont*100,linewidth=1,color='red')

        p8 = plt.step(indplus1, np.append(opt_res['SOC_elec'], 0), linewidth=1, color='red', where='post')
        # plt.xlabel('time [h]', fontsize=font_size)
        plt.title('Battery', fontsize=font_size)
        plt.ylabel('SoC [%]', fontsize=font_size)
        idx_plt = (np.linspace(0, N-1, 4, endpoint=True)).astype(int)
        plt.xticks(ind[idx_plt], ts[idx_plt])
        ax2.tick_params(axis="x", labelsize=font_size - 2)
        ax2.tick_params(axis="y", labelsize=font_size - 2)
        ax2.set_ylim(0, 100)
        ax2.set_xlim(0, N)
        plt.show()

        # plot EV soc
        ax2 = plt.subplot(1, 3, 2)
        # p8 = plt.plot(ind, bat_cont/bat_max_cont*100,linewidth=1,color='red')

        p8 = plt.step(indplus1, np.append(opt_res['EV_SOC'], 0), linewidth=1, color='red', where='post')
        # plt.xlabel('time [h]', fontsize=font_size)
        plt.title('EV', fontsize=font_size)
        plt.xticks(ind[idx_plt], ts[idx_plt])
        plt.setp(ax2.get_yticklabels(), visible=False)
        ax2.tick_params(axis="x", labelsize=font_size - 2)
        ax2.tick_params(axis="y", labelsize=font_size - 2)
        ax2.set_ylim(0, 100)
        ax2.set_xlim(0, N)
        plt.show()

        # plot SoC of heat storage
        ax2 = plt.subplot(1, 3, 3)
        p7 = plt.step(indplus1, np.append(opt_res['SOC_heat'], 0), linewidth=1, where='post', color='red')
        plt.xticks(ind[idx_plt], ts[idx_plt])
        plt.setp(ax2.get_yticklabels(), visible=False)
        ax2.tick_params(axis="x", labelsize=font_size - 2)
        ax2.tick_params(axis="y", labelsize=font_size - 2)
        ax2.set_ylim(0, 100)
        ax2.set_xlim(0, N)
        plt.title('Heat Storage', fontsize=font_size)
        # plt.tight_layout()
