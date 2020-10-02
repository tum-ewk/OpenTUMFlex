"""
The flex_ev module calculates the flexibility and prices of an ev based on an optimal charging schedule.
"""

__author__ = "Michel Zadé"
__copyright__ = "2020 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "1.0"
__maintainer__ = "Michel Zadé"
__email__ = "michel.zade@tum.de"
__status__ = "Development"

import pandas as pd
import math


def calc_flex_ev(my_ems, reopt=0):
    """
    Calculates the flexibility of an electric vehicle based on the optimal charging schedule.

    :param my_ems:  an opentumflex object that contains time settings, optimal charging schedules and electricity prices
    :param reopt:   ???

    :return:        an opentumflex object with the calculated ev flexibility
    """
    #print('EV Flex Calculation ...')
    # Time Data ###########################
    n_time_steps = my_ems['time_data']['nsteps']
    temp_res = my_ems['time_data']['t_inval']
    n_time_steps_phour = my_ems['time_data']['ntsteps']
    tsteps = range(len(my_ems['devices']['ev']['aval']))

    # Risk Margin comes in from user preferences
    risk_margin = 0.3

    # Column names
    p_opt = 'Sch_P'
    p_pos = 'Pos_P'
    p_neg = 'Neg_P'
    e_pos = 'Pos_E'
    e_neg = 'Neg_E'
    e_remain = 'Remain_E'
    pr_pos = 'Pos_Pr'
    pr_neg = 'Neg_Pr'
    pr_fcst = 'Fcst_Pr'

    # Flexibility Table for entire time period #############################################
    ev_flex = pd.DataFrame(0, columns={p_pos, p_neg, e_pos, e_neg, pr_pos, pr_neg, pr_fcst, p_opt},
                           index=my_ems['time_data']['time_slots'])
    # Fixing column order
    ev_flex = ev_flex[[p_pos, p_neg, e_pos, e_neg, pr_pos, pr_neg, pr_fcst, p_opt]]

    ev_flex[p_opt].at[:] = my_ems['optplan']['EV_power']
    ev_flex[pr_fcst].at[:] = my_ems['fcst']['ele_price_in']

    # Check number of periods ev is available
    n_avail_periods = len(my_ems['devices']['ev']['initSOC'])

    # Go through all availability periods and calculate flexibility
    for j in range(n_avail_periods):
        ev_flex_temp = pd.DataFrame(0.0, columns={p_pos, p_neg, e_pos, e_neg, pr_pos, pr_neg, pr_fcst, p_opt, e_remain},
                                    index=pd.date_range(start=my_ems['devices']['ev']['aval_init'][j],
                                                        end=my_ems['devices']['ev']['aval_end'][j],
                                                        freq=str(my_ems['time_data']['t_inval'])+'Min'))

        # Fixing column order
        ev_flex_temp = ev_flex_temp[[p_pos, p_neg, e_pos, e_neg, pr_pos, pr_neg, pr_fcst, p_opt, e_remain]]

        # Copy optimal power to flex table
        ev_flex_temp[p_opt].at[:] = ev_flex[p_opt][my_ems['devices']['ev']['aval_init'][j]:my_ems['devices']['ev']['aval_end'][j]]
        ev_flex_temp[pr_fcst].at[:] = ev_flex[pr_fcst][my_ems['devices']['ev']['aval_init'][j]:my_ems['devices']['ev']['aval_end'][j]]

        # Calculate remaining energy that needs to be charged in kWh ####
        remaining_energy = list((ev_flex_temp[p_opt] / n_time_steps_phour).sum() -
                                (ev_flex_temp[p_opt] / n_time_steps_phour).cumsum())
        remaining_energy.insert(0, (ev_flex_temp[p_opt] / n_time_steps_phour).sum())
        remaining_energy = remaining_energy[:-1]
        ev_flex_temp[e_remain] = remaining_energy

        # Calculation flexible power ######################
        ev_flex_temp[p_pos] = ev_flex_temp[p_opt]
        ev_flex_temp[p_neg] = my_ems['devices']['ev']['maxpow'] - ev_flex_temp[p_opt]
        # Reset flex power if power or energy is smaller or equal to zero
        ev_flex_temp.loc[ev_flex_temp[e_remain] <= 0, p_neg] = 0
        ev_flex_temp.loc[ev_flex_temp[p_pos] <= 0, p_pos] = 0
        ev_flex_temp.loc[ev_flex_temp[p_neg] <= 0, p_neg] = 0

        # Calculation of flex energy ###################
        for i in range(len(ev_flex_temp)):
            # Calculate how many hours flexible power is available
            t_neg_flex_avail = ((ev_flex_temp[p_neg].iloc[i:] < ev_flex_temp[p_neg].iat[i]).idxmax()
                                - ev_flex_temp.index[i]) / pd.Timedelta('1 hour')
            t_pos_flex_avail = ((ev_flex_temp[p_pos].iloc[i:] < ev_flex_temp[p_pos].iat[i]).idxmax()
                                - ev_flex_temp.index[i]) / pd.Timedelta('1 hour')
            # Calculate flexible energy
            ev_flex_temp[e_neg][i] = ev_flex_temp[p_neg].iat[i] * t_neg_flex_avail
            ev_flex_temp[e_pos][i] = ev_flex_temp[p_pos].iat[i] * t_pos_flex_avail

        # Round entire df to three decimals
        ev_flex_temp = round(ev_flex_temp, 3)

        # Check whether offered flex energy can be caught up later #######################
        for i in range(len(ev_flex_temp)):
            # Positive flex offers
            if ev_flex_temp[p_pos].iat[i] > 0:
                # Calculate last index of positive flex offer
                idx_remaining = len(ev_flex_temp) - round(i + n_time_steps_phour * ev_flex_temp[e_pos].iat[i] /
                                                          ev_flex_temp[p_pos].iat[i])
                idx_required = math.ceil(ev_flex_temp[e_pos].iat[i] /
                                         (my_ems['devices']['ev']['maxpow'] / n_time_steps_phour))
                if idx_remaining < idx_required:
                    e_max = idx_remaining / n_time_steps_phour * my_ems['devices']['ev']['maxpow']
                    ev_flex_temp[e_pos].iat[i] = math.floor(e_max / ev_flex_temp[p_pos].iat[i] * n_time_steps_phour) * \
                                                 ev_flex_temp[p_pos].iat[i] / n_time_steps_phour

            # Negative flex offers
            if ev_flex_temp[p_neg].iat[i] > 0:
                # Calculate for how many time steps negative flex can be offered
                # check whether power is not available anymore
                if (ev_flex_temp[p_neg].iloc[i:] < ev_flex_temp[p_neg].iloc[i]).any():
                    idx_p_neg_max = int(((ev_flex_temp[p_neg].iloc[i:] < ev_flex_temp[p_neg].iloc[i]).idxmax() -
                                         ev_flex_temp.index[i]).total_seconds() / 3600 * n_time_steps_phour)
                # power is available for entire time period
                else:
                    idx_p_neg_max = len(ev_flex_temp[p_neg].iloc[i:])
                # Offers with maximum negative power
                if ev_flex_temp[p_neg].iat[i] == my_ems['devices']['ev']['maxpow']:
                    if ev_flex_temp[e_neg].iat[i] > ev_flex_temp[e_remain].iat[i]:
                        ev_flex_temp[e_neg].iat[i] = ev_flex_temp[e_remain].iat[i]
                        if ev_flex_temp[e_neg].iat[i] == 0:
                            ev_flex_temp[p_neg].iat[i] = 0
                        else:
                            ev_flex_temp[p_neg].iat[i] = ev_flex_temp[e_neg].iat[i] * n_time_steps_phour / \
                                                         math.ceil(ev_flex_temp[e_neg].iat[i] /
                                                                   my_ems['devices']['ev']['maxpow'] *
                                                                   n_time_steps_phour)
                    if ev_flex_temp[e_neg].iat[i] <= 0:
                        ev_flex_temp[p_neg].iat[i] = 0
                # Offers with modulated power
                elif ev_flex_temp[p_neg].iat[i] < my_ems['devices']['ev']['maxpow']:
                    # Calculate the cumulated sum of flex and optimal charging schedule
                    temp_flex_df = pd.DataFrame(0, columns={'E_opt', 'E_flex', 'E_opt_cumsum',
                                                            'E_flex_cumsum', 'E_flex_opt_cumsum'},
                                                 index=ev_flex_temp.index[i:i + idx_p_neg_max])
                    temp_flex_df['E_opt'] = (ev_flex_temp[p_opt].iloc[i:i+idx_p_neg_max] / n_time_steps_phour)
                    temp_flex_df['E_flex'] = (ev_flex_temp[p_neg].iat[i] / n_time_steps_phour)
                    temp_flex_df['E_opt_cumsum'] = temp_flex_df['E_opt'].cumsum()
                    temp_flex_df['E_flex_cumsum'] = temp_flex_df['E_flex'].cumsum()
                    temp_flex_df['E_flex_opt_cumsum'] = (temp_flex_df['E_opt'] + temp_flex_df['E_flex']).cumsum()
                    # Check whether maximal possible energy is more than remaining energy
                    if max(temp_flex_df['E_flex_opt_cumsum']) < ev_flex_temp[e_remain].iat[i]:
                        pass
                    else:
                        # Find number of time steps until remaining energy has been charged
                        idx_allowed = int((temp_flex_df['E_flex_opt_cumsum'][temp_flex_df['E_flex_opt_cumsum'] >
                                                                             ev_flex_temp[e_remain].iat[i]].index[0] -
                                           ev_flex_temp.index[i]).total_seconds() / 3600 * n_time_steps_phour)
                        # Calculate maximal available time steps negative flex can be offered
                        # if number of available time steps is lower do not change offered energy
                        if idx_p_neg_max <= idx_allowed:
                            pass
                        else:
                            # Flexible energy is the sum of energy for maximal power
                            ev_flex_temp[e_neg].iat[i] = temp_flex_df['E_flex'][:idx_allowed].sum()

        # Reset negative power if energy has been reset as well
        ev_flex_temp.loc[ev_flex_temp[e_neg] <= 0, p_neg] = 0

        # # Calculating Flex Prices ###########################################################################
        for i in range(len(ev_flex_temp)):

            # Positive flexibility
            if ev_flex_temp[e_pos].iat[i] > 0 and ev_flex_temp[p_pos].iat[i] > 0:
                idx_required = math.ceil(ev_flex_temp[e_pos].iat[i] / my_ems['devices']['ev']['maxpow']
                                         / n_time_steps_phour)
                idx_flex = math.ceil(ev_flex_temp[e_pos].iat[i] / ev_flex_temp[p_pos].iat[i]
                                         * n_time_steps_phour)
                ev_flex_temp[pr_pos].iat[i] = ev_flex_temp[pr_fcst][i + idx_flex - 1:].nsmallest(idx_required).mean()\
                                                     * (1 + risk_margin)
            # Negative flexibility
            if ev_flex_temp[e_neg].iat[i] > 0 and ev_flex_temp[p_neg].iat[i] > 0:
                idx_flex = math.ceil(ev_flex_temp[e_neg].iat[i] / \
                                                   ev_flex_temp[p_neg].iat[i] * n_time_steps_phour)
                ev_flex_temp[pr_neg].iat[i] = ev_flex_temp[pr_fcst][i + idx_flex - 1:].nlargest(idx_flex).mean()\
                                                     * (risk_margin - 1)

        # Clean-up ##########################################
        # Drop unnecessary columns
        ev_flex_temp = ev_flex_temp.drop(columns={e_remain})

        # Copy temporary data frame to overall dataframe
        ev_flex[my_ems['devices']['ev']['aval_init'][j]:my_ems['devices']['ev']['aval_end'][j]] = ev_flex_temp

    #print('EV Flex Calculation completed!')
    ev_flex[p_opt] = -ev_flex[p_opt]
    ev_flex[p_neg] = -ev_flex[p_neg]
    ev_flex[e_neg] = -ev_flex[e_neg]

    my_ems['flexopts']['ev'] = ev_flex

    return my_ems
