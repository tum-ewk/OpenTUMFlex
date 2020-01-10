import numpy as np
import pandas as pd
import math
import statistics
from heapq import nsmallest
from heapq import nlargest


def calc_flex_ev(my_ems):
    print('\nEV Flex Calculation ...')
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

    ev_flex = ev_flex[['Pos_Flex_Power', 'Pos_Flex_Energy', 'Pos_Flex_Price',
                       'Neg_Flex_Power', 'Neg_Flex_Energy', 'Neg_Flex_Price',
                       'Price_Fcst', 'Opt_Power']]

    ev_flex.Opt_Power.at[:] = my_ems['optplan']['EV_power']
    ev_flex.Price_Fcst.at[:] = my_ems['fcst']['ele_price_in']

    # Check number of periods ev is available
    n_avail_periods = len(my_ems['devices']['ev']['initSOC'])

    # Go through all availability periods and calculate flexibility
    for j in range(n_avail_periods):
        ev_flex_temp = pd.DataFrame(0.0, columns={'Opt_Power', 'Remaining_Energy', 'Pos_Flex_Power', 'Neg_Flex_Power',
                                                  'Pos_Flex_Energy', 'Neg_Flex_Energy', 'Pos_Flex_Price',
                                                  'Neg_Flex_Price', 'Price_Fcst'},
                                    index=pd.date_range(start=my_ems['devices']['ev']['aval_init'][j],
                                                        end=my_ems['devices']['ev']['aval_end'][j],
                                                        freq=str(my_ems['time_data']['t_inval'])+'Min'))

        ev_flex_temp = ev_flex_temp[['Pos_Flex_Power', 'Pos_Flex_Energy', 'Pos_Flex_Price',
                                     'Neg_Flex_Power', 'Neg_Flex_Energy', 'Neg_Flex_Price',
                                     'Price_Fcst', 'Opt_Power', 'Remaining_Energy']]

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
        ev_flex_temp.Pos_Flex_Power = ev_flex_temp.Opt_Power
        ev_flex_temp.Neg_Flex_Power = my_ems['devices']['ev']['maxpow'] - ev_flex_temp.Opt_Power
        # Reset negative flex power if remaining energy is smaller or equal to zero
        ev_flex_temp.loc[ev_flex_temp.Remaining_Energy <= 0, 'Neg_Flex_Power'] = 0

        # Calculation of flex energy ###################
        for i in range(len(ev_flex_temp)):
            t_neg_flex_avail = ((ev_flex_temp.Neg_Flex_Power.iloc[i:] < ev_flex_temp.Neg_Flex_Power.iat[i]).idxmax()
                                - ev_flex_temp.index[i]) / pd.Timedelta('1 hour')
            t_pos_flex_avail = ((ev_flex_temp.Pos_Flex_Power.iloc[i:] < ev_flex_temp.Pos_Flex_Power.iat[i]).idxmax()
                                - ev_flex_temp.index[i]) / pd.Timedelta('1 hour')

            ev_flex_temp.Neg_Flex_Energy[i] = ev_flex_temp.Neg_Flex_Power.iat[i] * t_neg_flex_avail
            ev_flex_temp.Pos_Flex_Energy[i] = ev_flex_temp.Pos_Flex_Power.iat[i] * t_pos_flex_avail

        # Check whether offered flex energy can be caught up later #######################
        for i in range(len(ev_flex_temp)):
            # Positive flex offers
            if ev_flex_temp.Pos_Flex_Power.iat[i] > 0:
                # Calculate last index of positive flex offer
                idx_flex_end = round(i + n_time_steps_phour * ev_flex_temp.Pos_Flex_Energy.iat[i] /
                                     ev_flex_temp.Pos_Flex_Power.iat[i])
                n_tsteps_remaining = len(ev_flex_temp) - i      # remaining time steps
                idx_required = math.ceil(ev_flex_temp.Remaining_Energy.iat[i] /
                                         (my_ems['devices']['ev']['maxpow'] / n_time_steps_phour))
                if len(ev_flex_temp) - idx_flex_end < idx_required:
                    ev_flex_temp.Pos_Flex_Energy.iat[i] = (n_tsteps_remaining - idx_required) / n_time_steps_phour \
                                                              * my_ems['devices']['ev']['maxpow']
                elif ev_flex_temp.Opt_Power.iat[i] > 0 and n_tsteps_remaining == 0:
                    ev_flex_temp.Pos_Flex_Energy.iat[i] = (n_tsteps_remaining - idx_required) / n_time_steps_phour \
                                                              * my_ems['devices']['ev']['maxpow']
                if ev_flex_temp.Pos_Flex_Energy.iat[i] < 0:
                    ev_flex_temp.Pos_Flex_Energy.iat[i] = 0
                    ev_flex_temp.Pos_Flex_Power.iat[i] = 0

            # Negative flex offers
            if ev_flex_temp.Neg_Flex_Power.iat[i] > 0:
                if ev_flex_temp.Neg_Flex_Energy.iat[i] > ev_flex_temp.Remaining_Energy.iat[i]:
                    ev_flex_temp.Neg_Flex_Energy.iat[i] = ev_flex_temp.Remaining_Energy.iat[i]
                if ev_flex_temp.Neg_Flex_Energy.iat[i] <= 0:
                    ev_flex_temp.Neg_Flex_Power.iat[i] = 0

        # # Calculating Flex Prices ###########################################################################
        for i in range(len(ev_flex_temp)):
            # Positive flexibility
            if ev_flex_temp.Pos_Flex_Energy.iat[i] > 0:
                # Calculate number of time steps for flex offer
                n_flex_delivery_tsteps = math.ceil(ev_flex_temp.Pos_Flex_Energy.iat[i] / \
                                                   ev_flex_temp.Pos_Flex_Power.iat[i] * n_time_steps_phour)
                # Create pricing df
                pricing = pd.DataFrame(0, columns={'P_avail', 'C_fcst', 'E_charge', 'E_cumsum', 'C_energy'}, index=ev_flex_temp.index[i+n_flex_delivery_tsteps:])
                pricing.C_fcst = ev_flex_temp.Price_Fcst
                # Calculate remaining charging power besides optimal plan (considers also modulated charging power)
                pricing.P_avail = my_ems['devices']['ev']['maxpow'] - ev_flex_temp.Opt_Power
                pricing = pricing.sort_values(by=['C_fcst'])
                pricing.E_charge = pricing.P_avail / n_time_steps_phour
                pricing.E_cumsum = pricing.E_charge.cumsum()
                pricing.C_energy = pricing.C_fcst * pricing.E_charge
                # Get index at which energy is caught up (considers modulated charging power)
                idx_pricing_caught_up = pricing.index[pricing['E_cumsum'] >= ev_flex_temp.Pos_Flex_Energy.iat[i]][0]
                # Calculate pos flex price by taking cheapest remaining t-steps and taking average of energy costs
                ev_flex_temp.Pos_Flex_Price.iat[i] = pricing.C_energy.loc[:idx_pricing_caught_up].sum()\
                                                     * (1 + risk_margin) \
                                                     / pricing.E_cumsum.loc[idx_pricing_caught_up]

            # Negative flexibility
            if ev_flex_temp.Neg_Flex_Energy.iat[i] > 0:
                n_flex_delivery_tsteps = math.ceil(ev_flex_temp.Neg_Flex_Energy.iat[i] / \
                                                   ev_flex_temp.Neg_Flex_Power.iat[i] * n_time_steps_phour)
                ev_flex_temp.Neg_Flex_Price.iat[i] = statistics.mean(nlargest(n_flex_delivery_tsteps,
                                                                              ev_flex_temp.Price_Fcst[
                                                                              i + n_flex_delivery_tsteps:]))\
                                                     * (risk_margin - 1)

        # Clean-up ##########################################
        # Drop unnecessary cumulated energy column
        ev_flex_temp = ev_flex_temp.drop(columns={'Remaining_Energy'})

        # Copy temporary data frame to overall dataframe
        ev_flex[my_ems['devices']['ev']['aval_init'][j]:my_ems['devices']['ev']['aval_end'][j]] = ev_flex_temp

    print('\nEV Flex Calculation completed!')

    return ev_flex
