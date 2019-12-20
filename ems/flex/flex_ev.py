import numpy as np
import pandas as pd
import math
import statistics
from heapq import nsmallest
from heapq import nlargest


def calc_flex_ev(my_ems):
    # Time Data ###########################
    n_time_steps = my_ems['time_data']['nsteps']
    temp_res = my_ems['time_data']['t_inval']
    n_time_steps_phour = my_ems['time_data']['ntsteps']
    tsteps = range(len(my_ems['devices']['ev']['aval']))

    # Risk Margin comes in from user preferences
    risk_margin = 0.3

    # Flexibility Table for entire time period #############################################
    ev_flex = pd.DataFrame(0, columns={'Opt_Power', 'Pos_Flex_Power', 'Neg_Flex_Power', 'Pos_Flex_Energy',
                                       'Neg_Flex_Energy', 'Pos_Flex_Price', 'Neg_Flex_Price', 'Price_Fcst'},
                           index=pd.date_range(start=my_ems['time_data']['start_time'],
                                               end=my_ems['time_data']['end_time'],
                                               freq=str(my_ems['time_data']['t_inval']) + 'Min'))

    ev_flex.Opt_Power.at[:] = my_ems['optplan']['EV_power']
    ev_flex.Price_Fcst.at[:] = my_ems['fcst']['ele_price_in']

    # Check number of periods ev is available
    n_avail_periods = len(my_ems['devices']['ev']['initSOC'])

    # Go through all availability periods and calculate flexibility
    for j in range(n_avail_periods):
        ev_flex_temp = pd.DataFrame(0.0, columns={'Opt_Power', 'Remaining_Energy', 'Pos_Flex_Power', 'Neg_Flex_Power',
                                                  'Pos_Flex_Energy', 'Neg_Flex_Energy', 'Pos_Cum_Flex_Energy',
                                                  'Neg_Cum_Flex_Energy', 'Pos_Flex_Price', 'Neg_Flex_Price', 'Price_Fcst'},
                                    index=pd.date_range(start=my_ems['devices']['ev']['aval_init'][j],
                                                        end=my_ems['devices']['ev']['aval_end'][j],
                                                        freq=str(my_ems['time_data']['t_inval'])+'Min'))

        # Copy optimal power to flex table
        ev_flex_temp.Opt_Power.at[:] = ev_flex.Opt_Power[my_ems['devices']['ev']['aval_init'][j]:my_ems['devices']['ev']['aval_end'][j]]
        ev_flex_temp.Price_Fcst.at[:] = ev_flex.Price_Fcst[my_ems['devices']['ev']['aval_init'][j]:my_ems['devices']['ev']['aval_end'][j]]

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
        for i in range(len(ev_flex_temp)):
            # If EV is being charged
            if ev_flex_temp.Opt_Power.iat[i] > 0:
                # PosFlexEnergy[i] ist die Energiemenge, die im Zeitabschnitt geladen wird
                if i == len(ev_flex_temp)-1:
                    ev_flex_temp.Pos_Flex_Energy.iat[i] = ev_flex_temp.Remaining_Energy.iat[i]
                else:
                    ev_flex_temp.Pos_Flex_Energy.iat[i] = ev_flex_temp.Remaining_Energy.iat[i] \
                                                          - ev_flex_temp.Remaining_Energy.iat[i + 1]
            # If EV is not charged
            else:
                ev_flex_temp.Neg_Flex_Energy[i] = ev_flex_temp.Neg_Flex_Power.iat[i] / n_time_steps_phour

        # Cumulated Flex Energy #####################
        for i in range(len(ev_flex_temp)-1, -1, -1):
            if i == len(ev_flex_temp)-1:  # für den letzten Zeitschritt des Ladezeitraums
                ev_flex_temp.Neg_Cum_Flex_Energy.iat[i] = ev_flex_temp.Neg_Flex_Energy.iat[i]
                ev_flex_temp.Pos_Cum_Flex_Energy.iat[i] = ev_flex_temp.Pos_Flex_Energy.iat[i]
            # Positive flex energy
            elif ev_flex_temp.Neg_Flex_Energy.iat[i] == 0:
                ev_flex_temp.Pos_Cum_Flex_Energy.iat[i] = ev_flex_temp.Pos_Flex_Energy.iat[i] \
                                                          + ev_flex_temp.Pos_Cum_Flex_Energy.iat[i + 1]
            # Negative flex energy
            else:
                ev_flex_temp.Neg_Cum_Flex_Energy.iat[i] = ev_flex_temp.Neg_Flex_Energy.iat[i] + ev_flex_temp.Neg_Cum_Flex_Energy.iat[i + 1]

        # Check whether offered flex energy can be caught up later #######################
        for i in range(len(ev_flex_temp)):
            end_idx_pos = round(i + n_time_steps_phour * ev_flex_temp.Pos_Cum_Flex_Energy.iat[i] /
                                ev_flex_temp.Pos_Flex_Power.iat[i])
            n_tsteps_remaining = len(ev_flex_temp) - i
            idx_required = math.ceil(ev_flex_temp.Remaining_Energy.iat[i] /
                                     (my_ems['devices']['ev']['maxpow'] / n_time_steps_phour))
            if len(ev_flex_temp) - end_idx_pos < idx_required:
                ev_flex_temp.Pos_Cum_Flex_Energy.iat[i] = (n_tsteps_remaining - idx_required) / n_time_steps_phour \
                                                          * my_ems['devices']['ev']['maxpow']
            elif ev_flex_temp.Opt_Power.iat[i] > 0 and n_tsteps_remaining == 0:
                ev_flex_temp.Pos_Cum_Flex_Energy.iat[i] = (n_tsteps_remaining - idx_required) / n_time_steps_phour \
                                                          * my_ems['devices']['ev']['maxpow']
            if ev_flex_temp.Pos_Cum_Flex_Energy.iat[i] < 0:
                ev_flex_temp.Pos_Cum_Flex_Energy.iat[i] = 0
                ev_flex_temp.Pos_Flex_Power.iat[i] = 0

        # Get all indices for negative and positive flex offers
        neg_flex_idx = [i for i, x in enumerate(ev_flex_temp.Neg_Cum_Flex_Energy) if x]
        pos_flex_indices = [i for i, x in enumerate(ev_flex_temp.Pos_Cum_Flex_Energy) if x]
        # check whether offered negative energy is above remaining energy amount
        for i in neg_flex_idx:
            if ev_flex_temp.Neg_Cum_Flex_Energy.iat[i] > ev_flex_temp.Remaining_Energy.iat[i]:
                ev_flex_temp.Neg_Cum_Flex_Energy.iat[i] = ev_flex_temp.Remaining_Energy.iat[i]

        # From now the cumulated energy is the offered flexible energy ###############################
        # Copy cumulated energy to energy tables
        ev_flex_temp.Pos_Flex_Energy = ev_flex_temp.Pos_Cum_Flex_Energy
        ev_flex_temp.Neg_Flex_Energy = ev_flex_temp.Neg_Cum_Flex_Energy

        # Calculating Flex Prices ###########################################################################
        for i in range(len(ev_flex_temp)):
            # Positive flexibility
            if ev_flex_temp.Pos_Flex_Energy.iat[i] > 0:
                # Calculate how many time steps energy needs to be charged after flex call
                n_charge_remainder_tsteps = math.ceil(ev_flex_temp.Remaining_Energy.iat[i] / \
                                    my_ems['devices']['ev']['maxpow'] * n_time_steps_phour)
                n_flex_delivery_tsteps = math.ceil(ev_flex_temp.Pos_Flex_Energy.iat[i] / \
                                                   ev_flex_temp.Pos_Flex_Power.iat[i] * n_time_steps_phour)
                ev_flex_temp.Pos_Flex_Price.iat[i] = statistics.mean(nsmallest
                                                                     (n_charge_remainder_tsteps,
                                                                      ev_flex_temp.Price_Fcst[i + n_flex_delivery_tsteps:])) * (1 + risk_margin)

            # Negative flexibility
            elif ev_flex_temp.Neg_Flex_Energy.iat[i] > 0:
                n_flex_delivery_tsteps = math.ceil(ev_flex_temp.Neg_Flex_Energy.iat[i] / \
                                                   ev_flex_temp.Neg_Flex_Power.iat[i] * n_time_steps_phour)
                ev_flex_temp.Neg_Flex_Price.iat[i] = statistics.mean(nlargest(n_flex_delivery_tsteps,
                                                                              ev_flex_temp.Price_Fcst[i + n_flex_delivery_tsteps:])) * (risk_margin - 1)

            print(i)


        # Clean-up ##########################################
        # Drop unnecessary cumulated energy column
        ev_flex_temp = ev_flex_temp.drop(columns={'Remaining_Energy', 'Pos_Cum_Flex_Energy', 'Neg_Cum_Flex_Energy'})

        # Copy temporary data frame to overall dataframe
        ev_flex[my_ems['devices']['ev']['aval_init'][j]:my_ems['devices']['ev']['aval_end'][j]] = ev_flex_temp

    return ev_flex
