import pandas as pd
import os
import numpy as np

from ems.ems_mod import ems as ems_loc
from forecast import price_fcst

"""
#################################################################
# Preparation ###################################################
#################################################################
"""
# Output and input path
output_path = 'C:/Users/ga47num/PycharmProjects/GER MP - OpenTUMFlex - EV/Output/'
input_path = 'C:/Users/ga47num/PycharmProjects/GER MP - OpenTUMFlex - EV/Input/'
# List all file names, for all scenarios (ToU & Constant, with and without minimally increasing prices) the same
file_names = os.listdir(output_path + 'ToU/')
rtp_file_names = os.listdir(input_path + 'RTP/')
rtp_price_forecast = pd.read_hdf(input_path + 'RTP/' + rtp_file_names[rtp_file_names == 'rtp_15min'], key='df')
# Set minimal and maximal time
t_min = rtp_price_forecast.index.min()
t_max = rtp_price_forecast.index.max()
# Date range from minimal to maximal time
t_range = pd.date_range(start=t_min, end=t_max, freq='15Min')
# Create df for sum of optimal charging plans
opt_sum_df = pd.DataFrame(0, index=t_range, columns={'P_ev_opt_sum_tou',
                                                     'P_ev_opt_sum_const',
                                                     'P_ev_opt_sum_tou_mi',
                                                     'P_ev_opt_sum_const_mi',
                                                     'P_ev_opt_sum_rtp',
                                                     'n_veh_avail',
                                                     'c_elect_in_tou',
                                                     'c_elect_in_const',
                                                     'c_elect_in_tou_mi',
                                                     'c_elect_in_const_mi',
                                                     'c_elect_in_rtp',
                                                     'Daytime_ID'})
# Create df for sum of flexibility
flex_sum_df = pd.DataFrame(0, index=t_range, columns={'P_pos_sum_tou',
                                                      'P_pos_sum_tou_mi',
                                                      'P_pos_sum_const',
                                                      'P_pos_sum_const_mi',
                                                      'P_pos_sum_rtp',
                                                      'P_neg_sum_tou',
                                                      'P_neg_sum_tou_mi',
                                                      'P_neg_sum_const',
                                                      'P_neg_sum_const_mi',
                                                      'P_neg_sum_rtp',
                                                      'E_pos_sum_tou',
                                                      'E_pos_sum_tou_mi',
                                                      'E_pos_sum_const',
                                                      'E_pos_sum_const_mi',
                                                      'E_pos_sum_rtp',
                                                      'E_neg_sum_tou',
                                                      'E_neg_sum_tou_mi',
                                                      'E_neg_sum_const',
                                                      'E_neg_sum_const_mi',
                                                      'E_neg_sum_rtp',
                                                      'c_flex_pos_tou',
                                                      'c_flex_pos_tou_mi',
                                                      'c_flex_pos_const',
                                                      'c_flex_pos_const_mi',
                                                      'c_flex_pos_rtp',
                                                      'c_flex_neg_tou',
                                                      'c_flex_neg_tou_mi',
                                                      'c_flex_neg_const',
                                                      'c_flex_neg_const_mi',
                                                      'c_flex_neg_rtp',
                                                      'Daytime_ID'})
# Get forecast electricity prices for each time step
price_forecast = price_fcst.get_elect_price_fcst(t_start=t_min, t_end=t_max, pr_constant=0.19)
price_forecast.insert(value=rtp_price_forecast['price'].loc[t_min:t_max], loc=0, column='RTP')
opt_sum_df.loc[:, 'c_elect_in_tou'] = price_forecast['ToU']
opt_sum_df.loc[:, 'c_elect_in_const'] = price_forecast['Constant']
opt_sum_df.loc[:, 'c_elect_in_tou_mi'] = price_forecast['ToU_minimally_increasing']
opt_sum_df.loc[:, 'c_elect_in_const_mi'] = price_forecast['Constant_minimally_increasing']
opt_sum_df.loc[:, 'c_elect_in_rtp'] = price_forecast['RTP']
# Create a daytime identifier for weekday and time for heat map
opt_sum_df['Daytime_ID'] = opt_sum_df.index.weekday_name.array + \
                                ', ' + \
                           opt_sum_df.index.strftime('%H:%M').array
flex_sum_df['Daytime_ID'] = opt_sum_df.index.weekday_name.array + \
                                ', ' + \
                            opt_sum_df.index.strftime('%H:%M').array
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


"""
#################################################################################
# Read ems results, sum charging power, flexibility and veh availability ########
#################################################################################
"""
# read all results and store them in result lists
for result_name in file_names:
    my_ems_tou_mi = ems_loc(initialize=True, path=output_path + 'ToU_minimally_increasing/' + result_name)
    my_ems_tou = ems_loc(initialize=True, path=output_path + 'ToU/' + result_name)
    my_ems_const_mi = ems_loc(initialize=True, path=output_path + 'Constant_minimally_increasing/' + result_name)
    my_ems_const = ems_loc(initialize=True, path=output_path + 'Constant/' + result_name)
    my_ems_rtp = ems_loc(initialize=True, path=output_path + 'RTP/' + result_name)

    opt_result_df = pd.DataFrame({'P_ev_opt_tou_mi': my_ems_tou_mi['optplan']['EV_power'],
                                  'P_ev_opt_tou': my_ems_tou['optplan']['EV_power'],
                                  'P_ev_opt_const_mi': my_ems_const_mi['optplan']['EV_power'],
                                  'P_ev_opt_const': my_ems_const['optplan']['EV_power'],
                                  'P_ev_opt_rtp': my_ems_rtp['optplan']['EV_power']},
                                 index=pd.date_range(start=my_ems_tou_mi['time_data']['time_slots'][0],
                                                     end=my_ems_tou_mi['time_data']['time_slots'][-1],
                                                     freq='15Min'))
    flex_result_df = pd.DataFrame({'P_pos_tou': my_ems_tou['flexopts']['ev']['Pos_P'],
                                   'P_pos_tou_mi': my_ems_tou_mi['flexopts']['ev']['Pos_P'],
                                   'P_pos_const': my_ems_const['flexopts']['ev']['Pos_P'],
                                   'P_pos_const_mi': my_ems_const_mi['flexopts']['ev']['Pos_P'],
                                   'P_pos_rtp': my_ems_rtp['flexopts']['ev']['Pos_P'],
                                   'P_neg_tou': my_ems_tou['flexopts']['ev']['Neg_P'],
                                   'P_neg_tou_mi': my_ems_tou_mi['flexopts']['ev']['Neg_P'],
                                   'P_neg_const': my_ems_const['flexopts']['ev']['Neg_P'],
                                   'P_neg_const_mi': my_ems_const_mi['flexopts']['ev']['Neg_P'],
                                   'P_neg_rtp': my_ems_rtp['flexopts']['ev']['Neg_P'],
                                   'E_pos_tou': my_ems_tou['flexopts']['ev']['Pos_E'],
                                   'E_pos_tou_mi': my_ems_tou_mi['flexopts']['ev']['Pos_E'],
                                   'E_pos_const': my_ems_const['flexopts']['ev']['Pos_E'],
                                   'E_pos_const_mi': my_ems_const_mi['flexopts']['ev']['Pos_E'],
                                   'E_pos_rtp': my_ems_rtp['flexopts']['ev']['Pos_E'],
                                   'E_neg_tou': my_ems_tou['flexopts']['ev']['Neg_E'],
                                   'E_neg_tou_mi': my_ems_tou_mi['flexopts']['ev']['Neg_E'],
                                   'E_neg_const': my_ems_const['flexopts']['ev']['Neg_E'],
                                   'E_neg_const_mi': my_ems_const_mi['flexopts']['ev']['Neg_E'],
                                   'E_neg_rtp': my_ems_rtp['flexopts']['ev']['Neg_E']
                                   },
                                  index=pd.date_range(start=my_ems_tou_mi['time_data']['time_slots'][0],
                                                      end=my_ems_tou_mi['time_data']['time_slots'][-1],
                                                      freq='15Min'))
    # Optimal charging power addition
    opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_tou_mi'] \
        += opt_result_df['P_ev_opt_tou_mi']
    opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_tou'] \
        += opt_result_df['P_ev_opt_tou']
    opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_const_mi'] \
        += opt_result_df['P_ev_opt_const_mi']
    opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_const'] \
        += opt_result_df['P_ev_opt_const']
    opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_rtp'] \
        += opt_result_df['P_ev_opt_rtp']
    opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'n_veh_avail'] += 1
    # Flexible power addition
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_tou'] \
        += flex_result_df['P_pos_tou']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_tou_mi'] \
        += flex_result_df['P_pos_tou_mi']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_const'] \
        += flex_result_df['P_pos_const']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_const_mi'] \
        += flex_result_df['P_pos_const_mi']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_rtp'] \
        += flex_result_df['P_pos_rtp']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_tou'] \
        += flex_result_df['P_neg_tou']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_tou_mi'] \
        += flex_result_df['P_neg_tou_mi']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_const'] \
        += flex_result_df['P_neg_const']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_const_mi'] \
        += flex_result_df['P_neg_const_mi']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_rtp'] \
        += flex_result_df['P_neg_rtp']
    # Flexible energy addition
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_tou'] \
        += flex_result_df['E_pos_tou']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_tou_mi'] \
        += flex_result_df['E_pos_tou_mi']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_const'] \
        += flex_result_df['E_pos_const']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_const_mi'] \
        += flex_result_df['E_pos_const_mi']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_rtp'] \
        += flex_result_df['E_pos_rtp']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_tou'] \
        += flex_result_df['E_neg_tou']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_tou_mi'] \
        += flex_result_df['E_neg_tou_mi']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_const'] \
        += flex_result_df['E_neg_const']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_const_mi'] \
        += flex_result_df['E_neg_const_mi']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_rtp'] \
        += flex_result_df['E_neg_rtp']

# Save data to hdf files for further analysis
flex_sum_df.to_hdf(output_path + 'Aggregated Data/flex_sum_data.h5', mode='w', key='df')
opt_sum_df.to_hdf(output_path + 'Aggregated Data/opt_sum_data.h5', mode='w', key='df')

"""
####################################################################
# Group optimal and flexible power schedules by daytime ID #########
####################################################################
"""
# Prepare heat map for optimal charging power
opt_per_daytime = pd.DataFrame()
opt_per_daytime_temp = opt_sum_df.groupby(by='Daytime_ID').mean()
opt_per_daytime = opt_per_daytime.append(opt_per_daytime_temp.iloc[96:192, :])
opt_per_daytime = opt_per_daytime.append(opt_per_daytime_temp.iloc[480:, :])
opt_per_daytime = opt_per_daytime.append(opt_per_daytime_temp.iloc[384:480, :])
opt_per_daytime = opt_per_daytime.append(opt_per_daytime_temp.iloc[0:96, :])
opt_per_daytime = opt_per_daytime.append(opt_per_daytime_temp.iloc[192:384, :])
opt_per_daytime = opt_per_daytime.reset_index()
# Calculate percentiles per daytime
opt_per_daytime_qt = pd.DataFrame()
n_percentiles = 11           # Define number of percentiles
percentiles = np.linspace(start=0, stop=1, num=n_percentiles)
opt_per_daytime_temp = opt_sum_df.groupby(by='Daytime_ID').quantile(percentiles)
opt_per_daytime_qt = opt_per_daytime_qt.append(opt_per_daytime_temp.iloc[96 * n_percentiles:192 * n_percentiles, :])
opt_per_daytime_qt = opt_per_daytime_qt.append(opt_per_daytime_temp.iloc[480 * n_percentiles:, :])
opt_per_daytime_qt = opt_per_daytime_qt.append(opt_per_daytime_temp.iloc[384 * n_percentiles:480 * n_percentiles, :])
opt_per_daytime_qt = opt_per_daytime_qt.append(opt_per_daytime_temp.iloc[0:96 * n_percentiles, :])
opt_per_daytime_qt = opt_per_daytime_qt.append(opt_per_daytime_temp.iloc[192 * n_percentiles:384 * n_percentiles, :])
opt_per_daytime_qt = opt_per_daytime_qt.reset_index()
# Prepare heat map for flexible power
flex_per_daytime = pd.DataFrame()
flex_per_daytime_temp = flex_sum_df.groupby(by='Daytime_ID').mean()
flex_per_daytime = flex_per_daytime.append(flex_per_daytime_temp.iloc[96:192, :])
flex_per_daytime = flex_per_daytime.append(flex_per_daytime_temp.iloc[480:, :])
flex_per_daytime = flex_per_daytime.append(flex_per_daytime_temp.iloc[384:480, :])
flex_per_daytime = flex_per_daytime.append(flex_per_daytime_temp.iloc[0:96, :])
flex_per_daytime = flex_per_daytime.append(flex_per_daytime_temp.iloc[192:384, :])
flex_per_daytime = flex_per_daytime.reset_index()

# Save data to hdf files for further analysis
opt_per_daytime.to_hdf(output_path + 'Aggregated Data/opt_per_daytime_data.h5', mode='w', key='df')
opt_per_daytime_qt.to_hdf(output_path + 'Aggregated Data/opt_per_daytime_qt_data.h5', mode='w', key='df')
flex_per_daytime.to_hdf(output_path + 'Aggregated Data/flex_per_daytime_data.h5', mode='w', key='df')

# prepare df for week heat map
P_pos_tou_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                            columns=days)
P_pos_const_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                              columns=days)
P_pos_tou_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                               columns=days)
P_pos_const_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                 columns=days)
P_pos_rtp_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                            columns=days)
P_neg_tou_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                            columns=days)
P_neg_const_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                              columns=days)
P_neg_tou_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                               columns=days)
P_neg_const_mi_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                                 columns=days)
P_neg_rtp_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                            columns=days)
n_avail_veh_hm = pd.DataFrame(0, index=pd.date_range(start='00:00', end='23:45', freq='15Min').strftime('%H:%M'),
                              columns=days)

# Copy power to single day columns
for i in range(7):
    P_pos_tou_hm[days[i]].iloc[:] = flex_per_daytime['P_pos_sum_tou'].iloc[i * 96:i * 96 + 96].values
    P_pos_const_hm[days[i]].iloc[:] = flex_per_daytime['P_pos_sum_const'].iloc[i * 96:i * 96 + 96].values
    P_pos_tou_mi_hm[days[i]].iloc[:] = flex_per_daytime['P_pos_sum_tou_mi'].iloc[i * 96:i * 96 + 96].values
    P_pos_const_mi_hm[days[i]].iloc[:] = flex_per_daytime['P_pos_sum_const_mi'].iloc[i * 96:i * 96 + 96].values
    P_pos_rtp_hm[days[i]].iloc[:] = flex_per_daytime['P_pos_sum_rtp'].iloc[i * 96:i * 96 + 96].values
    P_neg_tou_hm[days[i]].iloc[:] = flex_per_daytime['P_neg_sum_tou'].iloc[i * 96:i * 96 + 96].values
    P_neg_const_hm[days[i]].iloc[:] = flex_per_daytime['P_neg_sum_const'].iloc[i * 96:i * 96 + 96].values
    P_neg_tou_mi_hm[days[i]].iloc[:] = flex_per_daytime['P_neg_sum_tou_mi'].iloc[i * 96:i * 96 + 96].values
    P_neg_const_mi_hm[days[i]].iloc[:] = flex_per_daytime['P_neg_sum_const_mi'].iloc[i * 96:i * 96 + 96].values
    P_neg_rtp_hm[days[i]].iloc[:] = flex_per_daytime['P_neg_sum_rtp'].iloc[i * 96:i * 96 + 96].values

# Save heat map dataframes to files
P_pos_tou_hm.to_hdf(output_path + 'Aggregated Data/P_pos_tou_hm_data.h5', mode='w', key='df')
P_pos_const_hm.to_hdf(output_path + 'Aggregated Data/P_pos_const_hm_data.h5', mode='w', key='df')
P_pos_tou_mi_hm.to_hdf(output_path + 'Aggregated Data/P_pos_tou_mi_hm_data.h5', mode='w', key='df')
P_pos_const_mi_hm.to_hdf(output_path + 'Aggregated Data/P_pos_const_mi_hm_data.h5', mode='w', key='df')
P_pos_rtp_hm.to_hdf(output_path + 'Aggregated Data/P_pos_rtp_hm_data.h5', mode='w', key='df')
P_neg_tou_hm.to_hdf(output_path + 'Aggregated Data/P_neg_tou_hm_data.h5', mode='w', key='df')
P_neg_const_hm.to_hdf(output_path + 'Aggregated Data/P_neg_const_hm_data.h5', mode='w', key='df')
P_neg_tou_mi_hm.to_hdf(output_path + 'Aggregated Data/P_neg_tou_mi_hm_data.h5', mode='w', key='df')
P_neg_const_mi_hm.to_hdf(output_path + 'Aggregated Data/P_neg_const_mi_hm_data.h5', mode='w', key='df')
P_neg_rtp_hm.to_hdf(output_path + 'Aggregated Data/P_neg_rtp_hm_data.h5', mode='w', key='df')
