# -*- coding: utf-8 -*-
"""
optimization for unit commitment of the household devices.

@author: ge57vam
"""
import sys
import pyomo.core as pyen
# import pyomo.environ
# from pyomo.core import *
from pyomo.opt import SolverFactory
from pyomo.opt import SolverManagerFactory
import pandas as pd
import numpy as np
from decimal import Decimal
import pyomo.core as py
import os
from scipy.interpolate import UnivariateSpline
import time as tm

from pyomo.environ import *
import matplotlib.pyplot as plt
import scipy.io

from ems.ems_mod import ems as ems_loc


def run_hp_opt(ems_local, plot_fig=True, result_folder='C:'):
    #    input_file = 'C:\Optimierung\Eingangsdaten_hp.xlsx'
    #    data = read_xlsdata(input_file);

    prob, timesteps = run_hp(ems_local)

    # chece if the results have been initialized
    try:
        # value(prob.ev_power[0])
        value(prob.ev_power[ems_local['time_data']['isteps']])
    except ValueError as error:
        print(error)
        raise ImportError(
            'the solver can not find a solution, try to change the device parameters to fulfill the requirements')

    length = len(timesteps)

    # print('Load Results ...\n')

    # ev parameters
    ev_node = ems_local['devices']['ev']['node']

    # electricity variable
    HP_ele_cap, HP_ele_run, elec_import, elec_export, lastprofil_elec, ev_pow, ev_soc, CHP_cap, pv_power, bat_cont, \
    bat_power, pv_pv2demand, pv_pv2grid, bat_grid2bat, \
    bat_power_pos, bat_power_neg, CHP_elec_run, CHP_operation, elec_supply_price, opt_ele_price = \
        (np.zeros(length) for i in range(20))
    # heat variable
    boiler_cap, CHP_heat_run, HP_heat_run, HP_heat_cap, CHP_operation, HP_operation, lastprofil_heat, sto_e_pow, sto_e_pow_pos, \
    CHP_gas_run, sto_e_pow_neg, sto_e_cont = \
        (np.zeros(length) for i in range(12))

    # final cost
    cost_min = np.zeros(length)
    # heat balance

    bat_max_cont = value(prob.bat_cont_max)
    sto_cont_max = value(prob.sto_cont)
    bat_cont_init = bat_max_cont * 0.5
    sto_cont_init = sto_cont_max * 0.5

    i = 0

    # timesteps = sorted(get_entity(prob, 't').index)
    # demand, ext, pro, sto = get_timeseries(prob, timesteps

    for idx in timesteps:
        # electricity balance

        ev_pow[i] = value(prob.ev_power[idx])
        ev_soc[i] = value(prob.ev_cont[idx]) / value(prob.ev_sto_cap) * 100 if value(prob.ev_sto_cap) > 0 else 0
        elec_import[i] = value(prob.elec_import[idx])
        elec_export[i] = value(prob.elec_export[idx])
        lastprofil_elec[i] = value(prob.lastprofil_elec[idx])
        pv_power[i] = value(prob.PV_cap[idx] * prob.pv_effic * prob.solar[idx])

        bat_cont[i] = value(prob.bat_cont[idx])
        bat_power_pos[i] = value(prob.bat_pow_neg[idx])
        bat_power_neg[i] = -value(prob.bat_pow_pos[idx])
        pv_pv2demand[i] = min(pv_power[i], lastprofil_elec[i])
        pv_pv2grid[i] = max(0, min(pv_power[i] - pv_pv2demand[i] + bat_power_neg[i], elec_export[i]))
        bat_grid2bat[i] = min(elec_import[i], -bat_power_neg[i])

        ##heat balance
        boiler_cap[i] = value(prob.boiler_cap[idx])
        # CHP
        if value(prob.chp_elec_run[idx]) > 0:
            CHP_operation[i] = value(prob.CHP_run[idx])
            CHP_cap[i] = value(prob.CHP_run[idx] * prob.chp_elec_run[idx])
            CHP_heat_run[i] = value(prob.chp_heat_run[idx])
            CHP_elec_run[i] = value(prob.chp_elec_run[idx])
            CHP_gas_run[i] = value(prob.chp_gas_run[idx])
        # HP
        if value(prob.hp_ther_pow[idx]) > 0:
            HP_operation[i] = value(prob.hp_run[idx])
            HP_heat_cap[i] = value(prob.hp_run[idx] * prob.hp_ther_pow[idx])
            HP_ele_cap[i] = value(prob.hp_run[idx] * prob.hp_ele_pow[idx])
            HP_heat_run[i] = value(prob.hp_ther_pow[idx])
            HP_ele_run[i] = value(prob.hp_ele_pow[idx])

        # supply prices

        elec_supply_price[i] = (elec_import[i] * value(prob.ele_price_in[idx]) + pv_power[i] * value(
            prob.ele_price_out[idx]) + CHP_gas_run[i] * CHP_operation[i] * value(prob.gas_price[idx]) + 0.000011) / \
                               (elec_import[i] + pv_power[i] + CHP_cap[i] + 0.0001)        
        lastprofil_heat[i] = value(prob.lastprofil_heat[idx])
        sto_e_pow[i] = value(prob.sto_e_pow[idx])
        sto_e_cont[i] = value(prob.sto_e_cont[idx])
        
        # Optimized electricity price (Import - Export)                      
        opt_ele_price[i] = elec_import[i]*value(prob.ele_price_in[idx]) - pv_pv2grid[i] \
            *value(prob.ele_price_out[idx]) - (elec_export[i] - pv_pv2grid[i]) * value(prob.gas_price[idx])

        # the total cost
        cost_min[i] = value(prob.costs[idx])

        i += 1

    SOC_heat = sto_e_cont / sto_cont_max * 100 if sto_cont_max > 0 else 0 * sto_e_cont
    SOC_elec = bat_cont / bat_max_cont * 100 if bat_max_cont > 0 else 0 * bat_cont
    # battery_power

    # heat storage power
    for i in range(length):
        if sto_e_pow[i] > 0:
            sto_e_pow_neg[i] = -sto_e_pow[i]
        else:
            sto_e_pow_pos[i] = -sto_e_pow[i]

            # plt.plot(c)
    # plt.plot(a)
    # plt.plot(b)
    # plt.plot(d)

    # plot electricity balance
    N = len(timesteps)
    ind = np.arange(N)  # the x locations for the groups
    # ts = ems_local['time_data']['time_slots'].tolist()
    isteps = ems_local['time_data']['isteps']
    nsteps = ems_local['time_data']['nsteps']
    ts = ems_local['time_data']['time_slots'][isteps:nsteps]
    ts = np.asarray(ts)
    # ind = ems_local['time_data']['time_slots'].tolist()
    width = 1  # the width of the bars: can also be len(x) sequence

    print('Optimized electricity net cost (€):', sum(opt_ele_price))
    print('Results Loaded.' + '\n')
    # plt.clf()

    COLOURS = {
        0: 'lightsteelblue',
        1: 'cornflowerblue',
        2: 'royalblue',
        3: 'lightgreen',
        4: 'salmon',
        5: 'mediumseagreen',
        6: 'orchid',
        7: 'burlywood',
        8: 'palegoldenrod',
        9: 'darkkhaki',
        10: 'lightskyblue',
        11: 'firebrick',
        12: 'blue',
        13: 'darkgreen'}

    if plot_fig is True:
        # figure properties
        fig = plt.figure(figsize=(10, 6))
        plt.rc('font', family='serif')
        font_size = 16
        # plots
        p1 = plt.bar(ind, CHP_cap, width, bottom=bat_power_pos, color='skyblue', align='edge')
        p2 = plt.bar(ind, pv_power, width,
                     bottom=bat_power_pos + CHP_cap, color='goldenrod', align='edge')
        p3 = plt.bar(ind, bat_power_pos, width, color='indianred', align='edge')
        p4 = plt.bar(ind, bat_power_neg, width, color='indianred', align='edge')
        p5 = plt.bar(ind, elec_import, width, bottom=bat_power_pos +
                                                     CHP_cap + pv_power, color='grey', align='edge')
        p6 = plt.bar(ind, -elec_export, width, bottom=bat_power_neg, color='darkseagreen', align='edge')
        # p7 = plt.plot(ind, lastprofil_elec,linewidth=3,color='k', align='edge')
        p7 = plt.step(ind, lastprofil_elec, linewidth=2, where='post', color='k')
        p8 = plt.bar(ind, -ev_pow, width, bottom=bat_power_neg - elec_export, color='plum', align='edge')
        p9 = plt.bar(ind, -HP_ele_cap, width, bottom=bat_power_neg -
                                                     elec_export - ev_pow, color='wheat', align='edge')
        # xticks
        ax = plt.gca()
        ax.axhline(linewidth=2, color="black")
        idx_plt = np.arange(0, len(timesteps), int(len(timesteps) / 5))
        plt.xticks(ind[idx_plt], ts[idx_plt], rotation=20)
        plt.tick_params(axis="x", labelsize=font_size - 2)
        plt.tick_params(axis="y", labelsize=font_size - 2)
        # plt.yticks(np.arange(-10, 10, 2))
        # ax1.set_xlim(0, len(timesteps) - 1)
        # labels
        plt.xlabel('Time [h]', fontsize=font_size)
        plt.ylabel('Electrical demand [kW]', fontsize=font_size)
        # plt.title('Cost optimal plan', fontsize=20)
        plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0], p6[0], p7[0], p8[0], p9[0]),
                   ('CHP', 'PV', 'Bat_Discharge', 'Bat_Charge', 'Import', 'Export', 'E_Demand', 'EV_charge', 'HP'),
                   prop={'size': font_size - 2}, bbox_to_anchor=(1.01, 0), loc="lower left")
        # plot properties
        plt.grid(color='lightgrey', linewidth=0.75)
        plt.tight_layout(rect=[0, 0, 1, 1])
        plt.margins(x=0)

        fig1 = plt.figure()
        ax2 = plt.subplot()
        # p8 = plt.plot(ind, bat_cont/bat_max_cont*100,linewidth=1,color='red')

        p8 = plt.step(ind, SOC_elec, linewidth=1, color='red', where='mid')
        plt.xlabel('time [h]', fontsize=font_size)
        plt.ylabel('SOC [%]', fontsize=font_size)
        # plt.title('SOC of Battery', fontsize=font_size)
        plt.xticks(ind[idx_plt], ts[idx_plt], rotation=20)
        ax2.set_xlim(0, len(timesteps) - 1)
        plt.show()

        # plot EV soc
        fig1 = plt.figure()
        ax3 = plt.subplot()
        # p8 = plt.plot(ind, bat_cont/bat_max_cont*100,linewidth=1,color='red')

        p8 = plt.step(ind, ev_soc, linewidth=1, color='red', where='mid')
        plt.xlabel('time [h]', fontsize=font_size)
        plt.ylabel('SOC [%]', fontsize=font_size)
        # plt.title('SOC of EV', fontsize=font_size)
        plt.xticks(ind[idx_plt], ts[idx_plt], rotation=20)
        ax2.set_xlim(0, len(timesteps) - 1)
        for i in np.arange(0, len(ev_node), 2):
            plt.axvspan(ev_node[i], ev_node[i + 1], facecolor='#b9ebeb', alpha=0.5)
        plt.show()

    #  plot heat balance
    # plots
    if plot_fig is True:
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.axhline(linewidth=2, color="black")
        p1 = plt.bar(ind, boiler_cap, width, bottom=sto_e_pow_pos, color='#689eb8')
        p2 = plt.bar(ind, CHP_heat_run, width,
                     bottom=boiler_cap + sto_e_pow_pos, color='skyblue')
        p3 = plt.bar(ind, HP_heat_cap, width, bottom=boiler_cap + CHP_heat_run + sto_e_pow_pos, color='#a79b94')
        p4 = plt.bar(ind, sto_e_pow_pos, width, color='#ff5a60')
        p5 = plt.bar(ind, sto_e_pow_neg, width, color='#ff5a60')
        p6 = plt.step(ind, lastprofil_heat, linewidth=2, where='mid', color='k')

        plt.xlabel('time [1/4 h]', fontsize=font_size)
        plt.ylabel('power and heat load [kW]', fontsize=font_size)
        # plt.title('heat balance', fontsize=font_size)
        plt.xticks([0, 24, 2, 2], fontsize=font_size)
        plt.yticks(fontsize=font_size)
        idx_plt = np.arange(0, len(timesteps), int(len(timesteps) / 5))
        plt.xticks(ind[idx_plt], ts[idx_plt], rotation=20)
        ax1.set_xlim(0, len(timesteps) - 1)
        # plt.yticks(np.arange(-10, 10, 2))
        plt.legend((p1[0], p2[0], p3[0], p4[0], p6[0]), ('boiler', 'CHP', 'HP', 'heat storage', 'heat demand'),
                   prop={'size': font_size}, loc='lower left')
        fig1 = plt.figure()
        ax2 = plt.subplot()

        p7 = plt.step(ind, SOC_heat, linewidth=1, where='mid', color='red')
        plt.xlabel('time [h]', fontsize=font_size)
        plt.ylabel('SOC [%]', fontsize=font_size)
        plt.xticks(ind[idx_plt], ts[idx_plt], rotation=20)
        ax2.set_xlim(0, len(timesteps) - 1)
        # plt.title('SOC of heat storage', fontsize=font_size)
        plt.show()

    # # save the data
    # from datetime import datetime
    # print('Save Results to Reportfile...\n')
    #
    # # Create Name of Resultfile
    # t0 = tm.time()
    # # inputfilename = input_file
    # now = datetime.now().strftime('%Y%m%dT%H%M')
    # resultfile = os.path.join(result_folder, 'result_optimization_{}.xlsx'.format(now))
    # writer = pd.ExcelWriter(resultfile)

    data_input = {'HP_operation': list(HP_operation), 'HP_heat_power': list(HP_heat_cap),
                  'HP_heat_run': list(HP_heat_run),
                  'HP_ele_run': list(HP_ele_run),
                  'CHP_operation': list(CHP_operation),
                  'CHP_heat_run': list(CHP_heat_run),
                  'CHP_elec_run': list(CHP_elec_run),
                  'CHP_gas_run': list(CHP_gas_run),
                  'SOC_heat': list(SOC_heat),
                  'SOC_elec': list(SOC_elec),
                  'PV_power': list(pv_power), 'pv_pv2demand': list(pv_pv2demand), 'pv_pv2grid': list(pv_pv2grid),
                  'grid_import': list(elec_import),
                  'Last_elec': list(lastprofil_elec), 'grid_export': list(elec_export),
                  'bat_grid2bat': list(bat_grid2bat),
                  'bat_input_power': list(-bat_power_neg), 'bat_output_power': list(bat_power_pos),
                  'bat_SOC': list(SOC_elec),
                  'EV_power': list(ev_pow),
                  'EV_SOC': list(ev_soc),
                  'elec_supply_price': list(elec_supply_price),
                  'min cost': list(cost_min),
                  'opt_ele_price':list(opt_ele_price)}

    # df = pd.DataFrame(data=data_input)
    # df.to_excel(writer, 'operation_plan', merge_cells=False)
    # scipy.io.savemat('data/operationalPlan.mat', {'struct1': df.to_dict("list")})
    # writer.save()  # save

    # print('Results Saved. time: ' + "{:.1f}".format(tm.time() - t0) + ' s\n')

    return data_input


def run_hp(ems_local):
    # record the time
    t0 = tm.time()
    # get all the data from the external file
    # ems_local = ems_loc(initialize=True, path='C:/Users/ge57vam/emsflex/ems/ems01_ems.txt')
    devices = ems_local['devices']

    # read data from excel file

    # print('Data Read. time: ' + "{:.1f}".format(tm.time() - t0) + ' s\n')
    # print('Prepare Data ...\n')
    t = tm.time()
    time_interval = ems_local['time_data']['t_inval']  # x minutes for one time step
    # write in the time series from the data
    df_time_series = ems_local['fcst']
    time_series = pd.DataFrame.from_dict(df_time_series)
    # time = time_series.index.values

    # print('Data Prepared. time: ' + "{:.1f}".format(tm.time() - t0) + ' s\n')
    #    lastprofil =data['Lastprofil']
    #    source_import =data['import']
    #    source_export =data['export']

    # system
    # get the initial time step
    # time_step_initial = parameter.loc['System']['value']
    time_step_initial = ems_local['time_data']['isteps']
    # time_step_end = int(60 / time_interval * 24)
    time_step_end = ems_local['time_data']['nsteps']
    timesteps = np.arange(time_step_initial, time_step_end)
    # timestep_1 = timesteps[0]

    # timesteps = timesteps_all[time_step_initial:time_step_end]
    t_dn = 2
    # 6*time_step_end/96
    t_up = 2
    # 6*time_step_end/96
    timesteps_dn = timesteps[time_step_initial + 1:time_step_end - t_dn]
    timesteps_up = timesteps[time_step_initial + 1:time_step_end - t_up]

    # 15 min for every timestep/ timestep by one hour
    # create the concrete model
    p2e = time_interval / 60

    # create the model object m
    m = pyen.ConcreteModel()

    # heat storage
    sto_param = devices['sto']
    # storage_cap = sto_param['stocap']
    tem_min_sto = sto_param['mintemp']
    tem_max_sto = sto_param['maxtemp']
    soc_init = sto_param['initSOC']
    self_discharge = sto_param['self_discharge']
    # unit in kWh
    sto_cont = sto_param['stocap']

    # boiler
    boil_param = devices['boiler']
    boil_cap = boil_param['maxpow']
    boil_eff = boil_param['eta']
    # EV, availability should be added
    ev_param = devices['ev']
    ev_min_power = ev_param['minpow']
    ev_max_power = ev_param['maxpow']
    ev_sto_cap = ev_param['stocap']
    ev_soc_init = ev_param['initSOC']
    ev_eta = ev_param['eta']
    ev_soc_end = ev_param['endSOC']
    ev_aval = ev_param['aval']
    ev_init_soc_check = ev_param['init_soc_check']
    ev_end_soc_check = ev_param['end_soc_check']
    # CHP
    chp_param = devices['chp']
    chp_elec_eff = chp_param['eta'][0]
    chp_ther_eff = chp_param['eta'][1]
    chp_elec_cap = chp_param['maxpow']
    # heat pump
    hp_param = devices['hp']
    hp_ther_cap = pd.DataFrame.from_dict(hp_param['maxpow'])
    hp_cop = pd.DataFrame.from_dict(hp_param['COP'])
    # PV
    pv_param = devices['pv']
    pv_peak_pow = pv_param['maxpow']
    pv_eff = pv_param['eta']
    # battery
    bat_param = devices['bat']
    bat_max_cont = bat_param['stocap']
    bat_SOC_init = bat_param['initSOC']
    bat_pow_max = bat_param['maxpow']
    bat_eta = bat_param['eta']

    ## create the parameter
    # print('Define Model ...\n')
    #
    m.t = pyen.Set(ordered=True, initialize=timesteps)

    #    m.t_end = pyen.Set(initialize=timesteps,
    #		doc='Timesteps without zero')
    m.t_DN = pyen.Set(ordered=True, initialize=timesteps_dn)
    m.t_UP = pyen.Set(ordered=True, initialize=timesteps_up)

    # heat_storage
    m.sto_max_cont = pyen.Param(initialize=sto_cont)

    m.SOC_init = pyen.Param(initialize=soc_init)

    # battery
    m.bat_cont_max = pyen.Param(initialize=bat_max_cont)
    m.bat_SOC_init = pyen.Param(initialize=bat_SOC_init)
    m.bat_power_max = pyen.Param(initialize=bat_pow_max)
    m.bat_eta = pyen.Param(initialize=bat_eta)

    # hp
    m.hp_ther_pow = pyen.Param(m.t, initialize=1, mutable=True, within=pyen.NonNegativeReals)
    m.sto_cont = pyen.Param(initialize=sto_cont)
    m.hp_COP = pyen.Param(m.t, initialize=1, mutable=True, within=pyen.NonNegativeReals)
    m.hp_ele_pow = pyen.Param(m.t, initialize=1, mutable=True, within=pyen.NonNegativeReals)
    m.T_DN = pyen.Param(initialize=t_dn, mutable=True)
    m.T_UP = pyen.Param(initialize=t_up, mutable=True)

    # elec_vehicle
    m.ev_min_pow = pyen.Param(initialize=ev_min_power)
    m.ev_max_pow = pyen.Param(initialize=ev_max_power)
    m.ev_sto_cap = pyen.Param(initialize=ev_sto_cap)
    # m.ev_soc_init = pyen.Param(m.aval_block, initialize=ev_soc_init)
    m.ev_eta = pyen.Param(initialize=ev_eta)
    # m.ev_soc_end = pyen.Param(m.aval_block, initialize=ev_soc_end)
    m.ev_aval = pyen.Param(m.t, initialize=1, mutable=True)
    m.ev_charg_amount = ev_sto_cap * (ev_soc_end[-1] - ev_soc_init[0]) / 100

    # boilder
    m.boiler_max_cap = pyen.Param(initialize=boil_cap)
    m.boiler_eff = pyen.Param(initialize=boil_eff)
    # chp
    m.chp_elec_effic = pyen.Param(m.t, initialize=chp_elec_eff)
    m.chp_ther_effic = pyen.Param(m.t, initialize=chp_ther_eff)
    m.chp_elec_run = pyen.Param(m.t, initialize=chp_elec_cap)
    m.chp_heat_run = pyen.Param(m.t, initialize=0, mutable=True)
    m.chp_gas_run = pyen.Param(m.t, initialize=0, mutable=True)
    # solar
    m.pv_effic = pyen.Param(initialize=pv_eff)
    m.pv_peak_power = pyen.Param(initialize=pv_peak_pow)
    m.solar = pyen.Param(m.t, initialize=1, mutable=True)

    #    for t in m.t_UP:
    #        m.t_dn[t] = t_dn
    #        m.t_up[t] = t_dn

    # price
    m.ele_price_in, m.ele_price_out, m.gas_price = (pyen.Param(m.t, initialize=1, mutable=True) for i in range(3))

    # lastprofil
    m.lastprofil_heat, m.lastprofil_elec = (pyen.Param(m.t, initialize=1, mutable=True) for i in range(2))

    for t in m.t:
        # weather data
        m.ele_price_in[t] = time_series.loc[t]['ele_price_in']
        m.gas_price[t] = time_series.loc[t]['gas']
        m.ele_price_out[t] = time_series.loc[t]['ele_price_out']
        m.lastprofil_heat[t] = time_series.loc[t]['last_heat']
        m.lastprofil_elec[t] = time_series.loc[t]['last_elec']
        m.solar[t] = time_series.loc[t]['solar']
        # fill the ev availability
        m.ev_aval[t] = ev_aval[t]
        # calculate the spline function for thermal power of heat pump
        spl_ther_pow = UnivariateSpline(list(map(float, hp_ther_cap.columns.values)), list(hp_ther_cap.iloc[0, :]))
        m.hp_ther_pow[t] = spl_ther_pow(time_series.loc[t]['temp'] + 273.15).item(0)
        # calculate the spline function for COP of heat pump
        spl_cop = UnivariateSpline(list(map(float, hp_cop.columns.values)), list(hp_cop.iloc[0, :]))
        m.hp_COP[t] = spl_cop(time_series.loc[t]['temp'] + 273.15).item(0)
        m.hp_ele_pow[t] = m.hp_ther_pow[t] / m.hp_COP[t]
        # calculate the chp electric and thermal power when it's running
        m.chp_heat_run[t] = m.chp_elec_run[t] / m.chp_elec_effic[t] * m.chp_ther_effic[t]
        m.chp_gas_run[t] = m.chp_elec_run[t] / m.chp_elec_effic[t]

    # m.ele_price = ele_price

    # Variables

    m.hp_run = pyen.Var(m.t, within=pyen.Boolean,
                        doc='operation of the heat pump')
    m.CHP_run = pyen.Var(m.t, within=pyen.Boolean,
                         doc='operation of the CHP')

    m.ev_power = pyen.Var(m.t, within=pyen.NonNegativeReals, bounds=(ev_min_power, ev_max_power),
                          doc='power of the EV')
    m.boiler_cap, m.PV_cap, m.elec_import, m.elec_export, m.bat_cont, m.sto_e_cont, m.bat_pow_pos, m.bat_pow_neg, \
    m.ev_cont, m.ev_var_pow, m.soc_diff = (pyen.Var(m.t, within=pyen.NonNegativeReals) for i in range(11))
    m.sto_e_pow, m.costs = (pyen.Var(m.t, within=pyen.Reals) for i in range(2))

    # Constrains

    # heat_storage
    def sto_e_cont_def_rule(m, t):
        if t > m.t[1]:
            return m.sto_e_cont[t] == m.sto_e_cont[t - 1] + m.sto_e_pow[t] * p2e
        else:
            return m.sto_e_cont[t] == m.sto_max_cont * m.SOC_init / 100 + m.sto_e_pow[t] * p2e

    m.sto_e_cont_def = pyen.Constraint(m.t,
                                       rule=sto_e_cont_def_rule,
                                       doc='heat_storage_balance')

    def heat_balance_rule(m, t):
        return m.boiler_cap[t] + m.CHP_run[t] * m.chp_heat_run[t] + \
               m.hp_run[t] * m.hp_ther_pow[t] - m.lastprofil_heat[t] - m.sto_e_pow[t] == 0

    m.heat_power_balance = pyen.Constraint(m.t,
                                           rule=heat_balance_rule,
                                           doc='heat_storage_balance')

    # battery
    def battery_e_cont_def_rule(m, t):
        if t > m.t[1]:
            return m.bat_cont[t] == m.bat_cont[t - 1] + (
                    m.bat_pow_pos[t] * m.bat_eta - m.bat_pow_neg[t] / m.bat_eta) * p2e
        else:
            return m.bat_cont[t] == m.bat_cont_max * m.bat_SOC_init / 100 + (m.bat_pow_pos[t] * m.bat_eta -
                                                                             m.bat_pow_neg[t] / m.bat_eta) * p2e

    m.bat_e_cont_def = pyen.Constraint(m.t,
                                       rule=battery_e_cont_def_rule,
                                       doc='battery_balance')

    def elec_balance_rule(m, t):
        return m.elec_import[t] + m.CHP_run[t] * m.chp_elec_run[t] + m.PV_cap[t] * m.pv_effic * m.solar[t] - \
               m.elec_export[t] - m.hp_run[t] * m.hp_ele_pow[t] - m.lastprofil_elec[t] - \
               (m.bat_pow_pos[t] - m.bat_pow_neg[t]) - m.ev_power[t] == 0

    m.elec_power_balance = pyen.Constraint(m.t, rule=elec_balance_rule, doc='elec_balance')

    def cost_sum_rule(m, t):
        return m.costs[t] == p2e * (m.boiler_cap[t] / m.boiler_eff * m.gas_price[t]
                                    + m.CHP_run[t] * m.chp_gas_run[t] * m.gas_price[t] +
                                    m.elec_import[t] * m.ele_price_in[t]
                                    - m.elec_export[t] * m.ele_price_out[t]) + m.soc_diff[t] * 1000

    m.cost_sum = pyen.Constraint(m.t,
                                 rule=cost_sum_rule)

    ##processes
    # EV
    # def EV_cap_max_rule(m, t):
    #     if t > m.t[int(len(m.t) / 2)]:
    #         # return pyen.Constraint.Skip;
    #         return m.ev_run[t] <= 0
    #     else:
    #         return m.ev_run[t] <= 0
    #
    # m.EV_cap_max_def= pyen.Constraint(m.t,
    # rule = EV_cap_max_rule)

    #    def EV_cap_min_rule(m,t):
    #        if t < m.t[int(len(m.t)/2)]:
    #          return m.ev_power[t] >= m.ev_max_pow;
    #        else:
    #          return pyen.Constraint.Skip;
    #
    #    m.EV_cap_min_def= pyen.Constraint(m.t,
    #			rule = EV_cap_min_rule)

    # ev battery balance
    def ev_cont_def_rule(m, t):
        if t > m.t[1]:
            return m.ev_cont[t] == m.ev_cont[t - 1] + m.ev_power[t] * p2e * ev_eta - m.ev_var_pow[t]
        else:
            return m.ev_cont[t] == m.ev_sto_cap * ev_soc_init[0] / 100 + m.ev_power[t] * p2e * ev_eta

    m.ev_cont_def = pyen.Constraint(m.t, rule=ev_cont_def_rule, doc='EV_balance')

    def EV_end_soc_rule(m, t):
        return m.ev_cont[t] >= m.ev_sto_cap * ev_end_soc_check[t] / 100 - m.soc_diff[t]

    m.EV_end_soc_def = pyen.Constraint(m.t, rule=EV_end_soc_rule)

    def EV_init_soc_rule(m, t):
        return m.ev_cont[t] <= m.ev_sto_cap * ev_init_soc_check[t] / 100

    m.EV_init_soc_def = pyen.Constraint(m.t, rule=EV_init_soc_rule)

    def EV_aval_rule(m, t):
        return m.ev_power[t] <= m.ev_aval[t] * m.ev_max_pow

    m.EV_aval_def = pyen.Constraint(m.t, rule=EV_aval_rule)

    # CHP
    # def chp_max_cap_rule(m, t):
    #     return m.CHP_run[t] <= m.chp_elec_run;
    #
    # m.chp_max_cap_def = pyen.Constraint(m.t,
    #                                     rule=chp_max_cap_rule)

    ##hp
    def hp_min_still_t_rule(m, t):
        return (m.hp_run[t - 1] - m.hp_run[t]) * m.T_DN <= m.T_DN - (
            # m.hp_run[t] + m.hp_run[t + 1] + m.hp_run[t + 2] + m.hp_run[t + 3] + m.hp_run[t + 4] + m.hp_run[t + 5])
                m.hp_run[t] + m.hp_run[t + 1])

    # m.hp_min_still_t_def = pyen.Constraint(m.t_DN,
    #                                     rule=hp_min_still_t_rule)

    def hp_min_lauf_t_rule(m, t):

        return (m.hp_run[t] - m.hp_run[t - 1]) * m.T_UP <= m.hp_run[t] + m.hp_run[t + 1]
        # + m.hp_run[t + 2] + m.hp_run[
        # t + 3] + m.hp_run[t + 4] + m.hp_run[t + 5]

    #  return (m.hp_run[t]-m.hp_run[t-1])*m.t_up[t] <= m.t_up[t]; m.hp_run[k]
    # m.hp_min_lauf_t_def = pyen.Constraint(m.t_UP,
    #                rule=hp_min_lauf_t_rule)

    def chp_min_still_t_rule(m, t):
        return (m.CHP_run[t - 1] - m.CHP_run[t]) * m.T_DN <= m.T_DN - (
                m.CHP_run[t] + m.CHP_run[t + 1])
        # + m.CHP_cap[t + 2] + m.CHP_cap[t + 3] + m.CHP_cap[t + 4] +
        # m.CHP_cap[t + 5]);

    # m.chp_min_still_t_def = pyen.Constraint(m.t_DN,
    #                            rule=chp_min_still_t_rule)

    def chp_min_lauf_t_rule(m, t):

        return (m.CHP_run[t] - m.CHP_run[t - 1]) * m.T_UP <= m.CHP_run[t] + m.CHP_run[t + 1]
        # + m.CHP_cap[t + 2] + \
        # m.CHP_cap[t + 3] + m.CHP_cap[t + 4] + m.CHP_cap[t + 5];

    #  return (m.hp_run[t]-m.hp_run[t-1])*m.t_up[t] <= m.t_up[t]; m.hp_run[k]
    # m.chp_min_lauf_t_def = pyen.Constraint(m.t_UP,
    #                 rule=chp_min_lauf_t_rule)

    # boiler
    def boiler_max_cap_rule(m, t):
        return m.boiler_cap[t] <= m.boiler_max_cap;

    m.boiler_max_cap_def = pyen.Constraint(m.t,
                                           rule=boiler_max_cap_rule)

    # PV
    def pv_max_cap_rule(m, t):
        return m.PV_cap[t] <= m.pv_peak_power;

    m.pv_max_cap_def = pyen.Constraint(m.t,
                                       rule=pv_max_cap_rule)

    # elec_import
    def elec_import_rule(m, t):
        return m.elec_import[t] <= 50 * 5000;

    m.elec_import_def = pyen.Constraint(m.t,
                                        rule=elec_import_rule)

    # elec_export
    def elec_export_rule(m, t):
        return m.elec_export[t] <= 50 * 5000;

    m.elec_export_def = pyen.Constraint(m.t,
                                        rule=elec_export_rule)

    # storage
    # storage content
    if m.sto_cont > 0:
        def sto_e_cont_min_rule(m, t):
            return m.sto_e_cont[t] / m.sto_cont >= 0.1;

        m.sto_e_cont_min = pyen.Constraint(m.t,
                                           rule=sto_e_cont_min_rule)

        def sto_e_cont_max_rule(m, t):
            return m.sto_e_cont[t] / m.sto_cont <= 0.9;

        m.sto_e_cont_max = pyen.Constraint(m.t,
                                           rule=sto_e_cont_max_rule)
    if m.bat_cont_max > 0:
        def bat_e_cont_min_rule(m, t):
            return m.bat_cont[t] / m.bat_cont_max >= 0.1

        m.bat_e_cont_min = pyen.Constraint(m.t,
                                           rule=bat_e_cont_min_rule)

        def bat_e_cont_max_rule(m, t):
            return m.bat_cont[t] / m.bat_cont_max <= 0.9

        m.bat_e_cont_max = pyen.Constraint(m.t, rule=bat_e_cont_max_rule)

    # def bat_pv_demand_rule(m, t):
    #     return m.pv2demand[t] == min(m.lastprofil_elec[t], m.PV_cap[t] * m.pv_effic * m.solar[t])
    #
    # m.bat_PV_demand = pyen.Constraint(m.t, rule=bat_pv_demand_rule)
    #
    # def bat_grid2battery_rule(m, t):
    #     return m.grid2bat[t] == min(m.elec_import[t], m.bat_pow_pos[t])
    #
    # m.grid2battery = pyen.Constraint(m.t, rule=bat_grid2battery_rule)

    # storage power

    def sto_e_max_pow_rule_1(m, t):
        return m.sto_e_pow[t] <= m.sto_cont

    m.sto_e_pow_max_1 = pyen.Constraint(m.t,
                                        rule=sto_e_max_pow_rule_1)

    def sto_e_max_pow_rule_2(m, t):
        return m.sto_e_pow[t] >= -m.sto_cont

    m.sto_e_pow_max_2 = pyen.Constraint(m.t,
                                        rule=sto_e_max_pow_rule_2)

    def bat_e_max_pow_rule_1(m, t):
        return m.bat_pow_pos[t] <= min(m.bat_power_max, m.bat_cont_max)

    m.bat_e_pow_max_1 = pyen.Constraint(m.t,
                                        rule=bat_e_max_pow_rule_1)

    def bat_e_max_pow_rule_2(m, t):
        return m.bat_pow_neg[t] <= min(m.bat_power_max, m.bat_cont_max)

    m.bat_e_pow_max_2 = pyen.Constraint(m.t,
                                        rule=bat_e_max_pow_rule_2)

    # end state of storage and battery
    m.sto_e_cont_end = pyen.Constraint(expr=(m.sto_e_cont[m.t[-1]] >= 0.5 * m.sto_cont))
    m.bat_e_cont_end = pyen.Constraint(expr=(m.bat_cont[m.t[-1]] >= 0.5 * m.bat_cont_max))

    # m.sto_e_cont_initial = pyen.Constraint(expr=(m.sto_e_cont[m.t0] == 0.5))
    # m.cc_bal = pyen.Constraint(expr=(pyen.summation(m.hp_run) >= 4))

    def obj_rule(m):
        # Return sum of total costs over all cost types.
        # Simply calculates the sum of m.costs over all m.cost_types.
        return pyen.summation(m.costs)

    m.obj = pyen.Objective(
        sense=pyen.minimize,
        rule=obj_rule,
        doc='Sum costs by cost type')

    # print('Model Defined. time: ' + "{:.1f}".format(tm.time() - t0) + ' s\n')
    # print('Solve Model ...\n')
    optimizer = SolverFactory('glpk')
    solver_opt = dict()
    # solver_opt['SolTimeLimit'] = 50
    solver_opt['mipgap'] = 0.001
    solver_manager = SolverManagerFactory('neos')
    # result = solver_manager.solve(m,opt=optimizer,tee=True,load_solutions=True)
    optimizer.solve(m, load_solutions=True, options=solver_opt, timelimit=15)
    # m.solutions.load_from(result);
    # aa = 1 if results['solution'] else 0

    print('Model Solved in: ' + "{:.1f}".format(tm.time() - t0) + 's (time)')
    return m, timesteps


def read_xlsdata(input_file):
    # read sheets of excel file and put them in one dictionary xls_data
    xls = pd.ExcelFile(input_file)  # read excel file

    xls_data = {}  # create dictionary
    xls_data.update({'input_file': input_file})
    xls_data.update({'time_series': xls.parse('time_series').set_index(['time'])})
    xls_data.update({'parameter': xls.parse('Einstellung').set_index(['process'])})

    ## neue Sheet am 10.09.2018 for variable COP

    return xls_data


if __name__ == "__main__":
    # 3th argument for input file, and 4th argument for the result folder (dont have to be the same)
    run_hp_opt('C:\Optimierung\Eingangsdaten_hp.xlsx', 'C:\Optimierung')
