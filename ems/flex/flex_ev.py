import numpy as np
import pandas as pd
import math
import statistics


def calc_flex_ev(my_ems):
    ######################################################################################
    ################################## vorbereitung ######################################

    n_time_steps = my_ems['time_data']['nsteps']    # Zeiten und timesteps
    temp_res = my_ems['time_data']['t_inval']
    n_time_steps_phour = my_ems['time_data']['t_inval']
    tsteps = range(len(my_ems['devices']['ev']['aval']))

    # Flexibility Table for entire time period
    ev_flex = pd.DataFrame(0, columns={'Opt_Power', 'Remaining_Energy', 'Pos_Flex_Power', 'Neg_Flex_Power',
                                            'Pos_Flex_Energy', 'Neg_Flex_Energy', 'Pos_Cum_Flex_Energy',
                                            'Neg_Cum_Flex_Energy'},
                                index=pd.date_range(start=my_ems['time_data']['start_time'],
                                                    end=my_ems['time_data']['end_time'],
                                                    freq=str(my_ems['time_data']['t_inval']) + 'Min'))

    ev_flex.Opt_Power.at[:] = my_ems['optplan']['EV_power']

    # Check number of periods ev is available
    n_avail_periods = len(my_ems['devices']['ev']['initSOC'])

    # Go through all availability periods and calculate flexibility
    for j in range(n_avail_periods):
        ev_flex_temp = pd.DataFrame(0.0, columns={'Opt_Power', 'Remaining_Energy', 'Pos_Flex_Power', 'Neg_Flex_Power',
                                                'Pos_Flex_Energy', 'Neg_Flex_Energy', 'Pos_Cum_Flex_Energy',
                                                'Neg_Cum_Flex_Energy'},
                                    index=pd.date_range(start=my_ems['devices']['ev']['aval_init'][j],
                                                        end=my_ems['devices']['ev']['aval_end'][j],
                                                        freq=str(my_ems['time_data']['t_inval'])+'Min'))

        # Copy optimal power to flex table
        ev_flex_temp.Opt_Power.at[:] = ev_flex.Opt_Power[my_ems['devices']['ev']['aval_init'][j]:my_ems['devices']['ev']['aval_end'][j]]

        # Calculate remaining energy that needs to be charged in kWh ####
        # Initially remaining energy is equal to desired end soc minus start soc multiplied by capacity
        ev_flex_temp['Remaining_Energy'].iat[0] = (my_ems['devices']['ev']['endSOC'][j] -
                                             my_ems['devices']['ev']['initSOC'][j]) / 100 * \
                                            my_ems['devices']['ev']['stocap']
        # Goes through all time steps and checks how much more energy needs to be charged
        for i in range(len(ev_flex_temp) - 1):
            ev_flex_temp.Remaining_Energy.iat[i + 1] = ev_flex_temp.Remaining_Energy.iat[i] - \
                                                       ev_flex_temp.Opt_Power.iat[i] / \
                                                       my_ems['time_data']['ntsteps'] \
                                                       * my_ems['devices']['ev']['eta']   # wird aktuell vom Optimierer nicht berücksichtigt
            # Reset all values of remaining energy if smaller zero
            if ev_flex_temp.Remaining_Energy.iat[i + 1] < 0:
                ev_flex_temp.Remaining_Energy.iat[i + 1] = 0

        # Calculation FlexPower ######################
        for i in range(len(ev_flex_temp)):
            # wenn gerade nicht geladen wird und das EV noch nicht fertig geladen ist
            if ev_flex_temp.Opt_Power.iat[i] == 0 and ev_flex_temp.Remaining_Energy.iat[i] > 0:
                # NegFlexPower[i] mit maximal möglicher Ladeleistung benennen
                ev_flex_temp.Neg_Flex_Power.iat[i] = my_ems['devices']['ev']['maxpow']
            else:
                ev_flex_temp.Pos_Flex_Power.iat[i] = ev_flex_temp.Opt_Power.iat[i]

        # Calculation FlexEnergy ###################
        for i in range(t_end, t_start - 1, -1):
            if plan_dataframe.at[tsteps[i], 'evpower'] > 0:  # wenn das EV gerade geladen wird
                if i == t_end:
                    PosFlexEnergy[i] = req_energy[i]
                else:
                    PosFlexEnergy[i] = req_energy[i] - req_energy[
                        i + 1]  # PosFlexEnergy[i] ist die Energiemenge, die im Zeitabschnitt geladen wird
            else:  # wenn das EV gerade nicht geladen wird
                NegFlexEnergy[i] = NegFlexPower[i] / n_time_steps_phour


    # Calculation FlexEnergy ###################
    for i in range(t_end, t_start-1, -1):
        if plan_dataframe.at[tsteps[i], 'evpower'] > 0:                                                                 # wenn das EV gerade geladen wird
            if i == t_end:
                PosFlexEnergy[i] = req_energy[i]
            else:
                PosFlexEnergy[i] = req_energy[i] - req_energy[i + 1]                                                        # PosFlexEnergy[i] ist die Energiemenge, die im Zeitabschnitt geladen wird
        else:                                                                                                           # wenn das EV gerade nicht geladen wird
            NegFlexEnergy[i] = NegFlexPower[i] / n_time_steps_phour                                                     # NegFlexEnergy[i] ist die maximal mögliche Energiemente, die in dem Zeitabschnitt geladen werden kann

    ################ Cumulated Flex Energy #####################
    for i in range(t_end, t_start-1, -1):                                                                               # In the last step there cannot be a summed flex offer
        if i == t_end:                                                                                                  # für den letzten Zeitschritt des Ladezeitraums
            NegCumFlexEnergy[i] = NegFlexEnergy[i]
            PosCumFlexEnergy[i] = PosFlexEnergy[i]
        elif NegFlexEnergy[i] == 0:                                                                                     # wenn es keine NegFlexEnergy gibt, gibt es positive
            PosCumFlexEnergy[i] = PosFlexEnergy[i] + PosCumFlexEnergy[i + 1]                                            # "aufsummieren" der PosCumFlexEnergies
        else:
            NegCumFlexEnergy[i] = NegFlexEnergy[i] + NegCumFlexEnergy[i + 1]                                            # "aufsummieren" der NegCumFlexEnergies

    ################ Check wether offered flex energy is positive or negative #######################
    for i in range(n_time_steps):
        endpunkt_posflex[i] = round(tsteps[i] + n_time_steps_phour * PosCumFlexEnergy[i] / PosFlexPower[i])
        n_timeslots_remaining = t_end - i
        if t_end-endpunkt_posflex[i] < req_time[i]:
            PosCumFlexEnergy[i] = (n_timeslots_remaining - req_time[i]) / n_time_steps_phour * ev_dict["maxpow"]
        elif plan_dataframe.at[tsteps[i], 'evpower'] > 0 and n_timeslots_remaining == 0:
            PosCumFlexEnergy[i] = (n_timeslots_remaining-req_time[i]) / n_time_steps_phour * ev_dict["maxpow"]
        if PosCumFlexEnergy[i] < 0:
            PosCumFlexEnergy[i] = 0
            PosFlexPower[i] = 0

    neg_flex_indices = np.argwhere(NegCumFlexEnergy != 0)
    for i in neg_flex_indices:                                                                                          # NegFlexIndices
        if NegCumFlexEnergy[i] > req_energy[i]:                                                                         # Überprüfen, ob der errechnete Wert im Rahmen der Möglichkeiten liegt
            NegCumFlexEnergy[i] = req_energy[i]

    ################ Cleaning tables ###################
    for i in range(n_time_steps):
        PosFlexEnergy[i] = PosCumFlexEnergy[i]
        NegFlexEnergy[i] = NegCumFlexEnergy[i]

    PosCumFlexEnergy = np.zeros(n_time_steps)
    NegCumFlexEnergy = np.zeros(n_time_steps)

    ################ Calculating Flex Prices #################

    for i in range(t_start, t_end):
        if PosFlexEnergy[i] > 0:                                                                                        # PosFlexEnergy:
            timesteps = np.linspace(i+1, t_end, t_end-i)                                                                # für alle Zeitwerte von i+1 bis t_end werden alle Zeitpunkte gesucht, an denen PosFlexEnergy = 0 gilt. Von all diesen Zeitschritten wird der preisliche Mittelwert gebildet und als FlexPrice[i] eingetragen
            PosFlexEnergyAct = np.zeros(n_time_steps)
            for j in range(i+1, t_end+1):
                PosFlexEnergyAct[j] = PosFlexEnergy[j]
            search = np.argwhere(PosFlexEnergyAct == 0)
            result = np.zeros(n_time_steps)
            for k in search:
                result[k] = plan_dataframe.at[tsteps[int(k)], 'cost']
            result.sort()
            FlexPrice[i] = statistics.mean(plan_dataframe["cost"]) * (1+user_dict["riskmarg"])

        elif NegFlexEnergy[i] > 0:                                                                                      # NegFlexEnergy:
            d = np.zeros(n_time_steps)                                                                                  # vorher: n_time_steps - i  #   für alle Zeitwerte von i+1 bis t_end wird der preisliche Mittelwert gebildet und als FlexPrice[i] eingetragen
            x = np.linspace(i+1, t_end, t_end-i)
            for k in range(i, t_end+1):
                d[k] = plan_dataframe.at[tsteps[int(k)], 'cost']
#            d.sort()
            test = abs(NegFlexEnergy[i]/NegFlexPower[i]*n_time_steps_phour)
            FlexPrice[i] = statistics.mean(plan_dataframe["cost"]) * (user_dict["riskmarg"]-1)
#            FlexPrice[i] = statistics.mean(d[:len(x)]) * (user_dict["riskmarg"]-1)
#            FlexPrice[i] = statistics.mean(np.argmin(d, abs(NegFlexEnergy[i])/abs(NegFlexPower[i])*n_time_steps_phour))*(user_dict["riskmarg"]-1)

    ######################################################################################
    #################################### ausgabe #########################################
    flex_dataframe = pd.DataFrame(index=tsteps, columns={'optpow', 'pospow', 'negpower', 'posenergy', 'negenergy', 'posprice', 'negprice'})

    for i in range(n_time_steps):                                                                                       # Ausgeben der Werte
        flex_dataframe.at[tsteps[i], 'optpow'] = plan_dataframe.at[tsteps[i], 'evpower']
        flex_dataframe.at[tsteps[i], 'pospow'] = PosFlexPower[i]
        flex_dataframe.at[tsteps[i], 'negpower'] = NegFlexPower[i]
        flex_dataframe.at[tsteps[i], 'posenergy'] = PosFlexEnergy[i]
        flex_dataframe.at[tsteps[i], 'negenergy'] = NegFlexEnergy[i]
        flex_dataframe.at[tsteps[i], 'posprice'] = FlexPrice[i]
        flex_dataframe.at[tsteps[i], 'negprice'] = NegFlexPrice[i]

    return flex_dataframe