import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sb

from ems.ems_mod import ems as ems_loc
from forecast import price_fcst

"""
#################################################################
# Preparation ###################################################
#################################################################
"""
# minimal and maximal time of all files (known)
t_min = pd.Timestamp('2012-02-01 11:30:00')
t_max = pd.Timestamp('2013-02-04 06:15:00')
# Date range from minimal to maximal time
t_range = pd.date_range(start=t_min, end=t_max, freq='15Min')
# Create df for sum of optimal charging plans
chts_opt_sum_df = pd.DataFrame(0, index=t_range, columns={'P_ev_opt_sum_tou',
                                                          'P_ev_opt_sum_const',
                                                          'P_ev_opt_sum_tou_mi',
                                                          'P_ev_opt_sum_const_mi',
                                                          'n_veh_avail',
                                                          'c_elect_in_tou',
                                                          'c_elect_in_const',
                                                          'c_elect_in_tou_mi',
                                                          'c_elect_in_const_mi',
                                                          'Daytime_ID'})
# Create df for sum of flexibility
chts_flex_sum_df = pd.DataFrame(0, index=t_range, columns={'P_pos_sum_tou',
                                                           'P_pos_sum_tou_mi',
                                                           'P_pos_sum_const',
                                                           'P_pos_sum_const_mi',
                                                           'P_neg_sum_tou',
                                                           'P_neg_sum_tou_mi',
                                                           'P_neg_sum_const',
                                                           'P_neg_sum_const_mi',
                                                           'E_pos_sum_tou',
                                                           'E_pos_sum_tou_mi',
                                                           'E_pos_sum_const',
                                                           'E_pos_sum_const_mi',
                                                           'E_neg_sum_tou',
                                                           'E_neg_sum_tou_mi',
                                                           'E_neg_sum_const',
                                                           'E_neg_sum_const_mi',
                                                           'c_flex_pos_tou',
                                                           'c_flex_pos_tou_mi',
                                                           'c_flex_pos_const',
                                                           'c_flex_pos_const_mi',
                                                           'c_flex_neg_tou',
                                                           'c_flex_neg_tou_mi',
                                                           'c_flex_neg_const',
                                                           'c_flex_neg_const_mi',
                                                           'Daytime_ID'})
# Get forecast electricity prices for each time step
price_forecast = price_fcst.get_elect_price_fcst(t_start=t_min, t_end=t_max, pr_constant=0.19)
chts_opt_sum_df.loc[:, 'c_elect_in_tou'] = price_forecast['ToU']
chts_opt_sum_df.loc[:, 'c_elect_in_const'] = price_forecast['Constant']
chts_opt_sum_df.loc[:, 'c_elect_in_tou_mi'] = price_forecast['ToU_minimally_increasing']
chts_opt_sum_df.loc[:, 'c_elect_in_const_mi'] = price_forecast['Constant_minimally_increasing']
# Create a daytime identifier for weekday and time for heat map
chts_opt_sum_df['Daytime_ID'] = chts_opt_sum_df.index.weekday_name.array + \
                                ', ' + \
                                chts_opt_sum_df.index.strftime('%H:%M').array
chts_flex_sum_df['Daytime_ID'] = chts_opt_sum_df.index.weekday_name.array + \
                                ', ' + \
                                chts_opt_sum_df.index.strftime('%H:%M').array
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


"""
#################################################################################
# Read ems results, sum charging power, flexibility and veh availability ########
#################################################################################
"""
# List all file names, for all scenarios (ToU & Constant, with and without minimally increasing prices) the same
file_names = os.listdir('C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/ToU/')

# read all results and store them in result lists
for result_name in file_names:
    my_ems_tou_mi = ems_loc(initialize=True,
                            path='C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/'
                                 'ToU_with_price_increment/'
                                 + result_name)
    my_ems_tou = ems_loc(initialize=True,
                         path='C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/ToU/'
                              + result_name)
    my_ems_const_mi = ems_loc(initialize=True,
                              path='C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/'
                                   'Constant_with_price_increment/'
                                   + result_name)
    my_ems_const = ems_loc(initialize=True,
                           path='C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/Constant/'
                                + result_name)

    opt_result_df = pd.DataFrame({'P_ev_opt_tou_mi': my_ems_tou_mi['optplan']['EV_power'],
                                  'P_ev_opt_tou': my_ems_tou['optplan']['EV_power'],
                                  'P_ev_opt_const_mi': my_ems_const_mi['optplan']['EV_power'],
                                  'P_ev_opt_const': my_ems_const['optplan']['EV_power']},
                                 index=pd.date_range(start=my_ems_tou_mi['time_data']['time_slots'][0],
                                                     end=my_ems_tou_mi['time_data']['time_slots'][-1],
                                                     freq='15Min'))
    flex_result_df = pd.DataFrame({'P_pos_tou': my_ems_tou['flexopts']['ev']['Pos_P'],
                                   'P_pos_tou_mi': my_ems_tou_mi['flexopts']['ev']['Pos_P'],
                                   'P_pos_const': my_ems_const['flexopts']['ev']['Pos_P'],
                                   'P_pos_const_mi': my_ems_const_mi['flexopts']['ev']['Pos_P'],
                                   'P_neg_tou': my_ems_tou['flexopts']['ev']['Neg_P'],
                                   'P_neg_tou_mi': my_ems_tou_mi['flexopts']['ev']['Neg_P'],
                                   'P_neg_const': my_ems_const['flexopts']['ev']['Neg_P'],
                                   'P_neg_const_mi': my_ems_const_mi['flexopts']['ev']['Neg_P'],
                                   'E_pos_tou': my_ems_tou['flexopts']['ev']['Pos_E'],
                                   'E_pos_tou_mi': my_ems_tou_mi['flexopts']['ev']['Pos_E'],
                                   'E_pos_const': my_ems_const['flexopts']['ev']['Pos_E'],
                                   'E_pos_const_mi': my_ems_const_mi['flexopts']['ev']['Pos_E'],
                                   'E_neg_tou': my_ems_tou['flexopts']['ev']['Neg_E'],
                                   'E_neg_tou_mi': my_ems_tou_mi['flexopts']['ev']['Neg_E'],
                                   'E_neg_const': my_ems_const['flexopts']['ev']['Neg_E'],
                                   'E_neg_const_mi': my_ems_const_mi['flexopts']['ev']['Neg_E']
                                   },
                                  index=pd.date_range(start=my_ems_tou_mi['time_data']['time_slots'][0],
                                                      end=my_ems_tou_mi['time_data']['time_slots'][-1],
                                                      freq='15Min'))
    # Optimal charging power addition
    chts_opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_tou_mi'] \
        += opt_result_df['P_ev_opt_tou_mi']
    chts_opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_tou'] \
        += opt_result_df['P_ev_opt_tou']
    chts_opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_const_mi'] \
        += opt_result_df['P_ev_opt_const_mi']
    chts_opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_const'] \
        += opt_result_df['P_ev_opt_const']
    chts_opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'n_veh_avail'] += 1
    # Flexible power addition
    chts_flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_tou'] \
        += flex_result_df['P_pos_tou']
    chts_flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_tou_mi'] \
        += flex_result_df['P_pos_tou_mi']
    chts_flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_const'] \
        += flex_result_df['P_pos_const']
    chts_flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_const_mi'] \
        += flex_result_df['P_pos_const_mi']
    chts_flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_tou'] \
        += flex_result_df['P_neg_tou']
    chts_flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_tou_mi'] \
        += flex_result_df['P_neg_tou_mi']
    chts_flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_const'] \
        += flex_result_df['P_neg_const']
    chts_flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_const_mi'] \
        += flex_result_df['P_neg_const_mi']
    # Flexible energy addition
    chts_flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_tou'] \
        += flex_result_df['E_pos_tou']
    chts_flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_tou_mi'] \
        += flex_result_df['E_pos_tou_mi']
    chts_flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_const'] \
        += flex_result_df['E_pos_const']
    chts_flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_const_mi'] \
        += flex_result_df['E_pos_const_mi']
    chts_flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_tou'] \
        += flex_result_df['E_neg_tou']
    chts_flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_tou_mi'] \
        += flex_result_df['E_neg_tou_mi']
    chts_flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_const'] \
        += flex_result_df['E_neg_const']
    chts_flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_const_mi'] \
        += flex_result_df['E_neg_const_mi']


# Save data to hdf files for further analysis
chts_flex_sum_df.to_hdf('C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/Aggregated Data/chts_flex_sum_data.h5', mode='a', key='df')
chts_opt_sum_df.to_hdf('C:/Users/ga47num/PycharmProjects/CHTS - OpenTUMFlex - EV - Results/Aggregated Data/chts_opt_sum_data.h5', mode='a', key='df')
