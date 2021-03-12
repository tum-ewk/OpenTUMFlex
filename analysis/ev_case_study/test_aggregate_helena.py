for result_name in file_names:
    my_ems_tou_mi = opentumflex.init_ems_js(path=output_path + str(power) + '/ToU_mi/' + result_name)
    my_ems_tou = opentumflex.init_ems_js(path=output_path + str(power) + '/ToU/' + result_name)
    my_ems_con_mi = opentumflex.init_ems_js(path=output_path + str(power) + '/Con_mi/' + result_name)
    my_ems_con = opentumflex.init_ems_js(path=output_path + str(power) + '/Constant/' + result_name)
    my_ems_rtp = opentumflex.init_ems_js(path=output_path + str(power) + '/RTP/' + result_name)

    opt_result_df = pd.DataFrame({'P_ev_opt_tou_mi': my_ems_tou_mi['optplan']['EV_power'],
                                  'P_ev_opt_tou': my_ems_tou['optplan']['EV_power'],
                                  'P_ev_opt_con_mi': my_ems_con_mi['optplan']['EV_power'],
                                  'P_ev_opt_con': my_ems_con['optplan']['EV_power'],
                                  'P_ev_opt_rtp': my_ems_rtp['optplan']['EV_power']},
                                 index=pd.date_range(start=my_ems_tou_mi['time_data']['time_slots'][0],
                                                     end=my_ems_tou_mi['time_data']['time_slots'][-1],
                                                     freq='15Min'))
    flex_result_df = pd.DataFrame({'P_pos_tou': my_ems_tou['flexopts']['ev']['Pos_P'],
                                   'P_pos_tou_mi': my_ems_tou_mi['flexopts']['ev']['Pos_P'],
                                   'P_pos_con': my_ems_con['flexopts']['ev']['Pos_P'],
                                   'P_pos_con_mi': my_ems_con_mi['flexopts']['ev']['Pos_P'],
                                   'P_pos_rtp': my_ems_rtp['flexopts']['ev']['Pos_P'],
                                   'P_neg_tou': my_ems_tou['flexopts']['ev']['Neg_P'],
                                   'P_neg_tou_mi': my_ems_tou_mi['flexopts']['ev']['Neg_P'],
                                   'P_neg_con': my_ems_con['flexopts']['ev']['Neg_P'],
                                   'P_neg_con_mi': my_ems_con_mi['flexopts']['ev']['Neg_P'],
                                   'P_neg_rtp': my_ems_rtp['flexopts']['ev']['Neg_P'],
                                   'E_pos_tou': my_ems_tou['flexopts']['ev']['Pos_E'],
                                   'E_pos_tou_mi': my_ems_tou_mi['flexopts']['ev']['Pos_E'],
                                   'E_pos_con': my_ems_con['flexopts']['ev']['Pos_E'],
                                   'E_pos_con_mi': my_ems_con_mi['flexopts']['ev']['Pos_E'],
                                   'E_pos_rtp': my_ems_rtp['flexopts']['ev']['Pos_E'],
                                   'E_neg_tou': my_ems_tou['flexopts']['ev']['Neg_E'],
                                   'E_neg_tou_mi': my_ems_tou_mi['flexopts']['ev']['Neg_E'],
                                   'E_neg_con': my_ems_con['flexopts']['ev']['Neg_E'],
                                   'E_neg_con_mi': my_ems_con_mi['flexopts']['ev']['Neg_E'],
                                   'E_neg_rtp': my_ems_rtp['flexopts']['ev']['Neg_E'],
                                   'c_flex_pos_tou': my_ems_tou['flexopts']['ev']['Pos_Pr'],
                                   'c_flex_pos_tou_mi': my_ems_tou_mi['flexopts']['ev']['Pos_Pr'],
                                   'c_flex_pos_con': my_ems_con['flexopts']['ev']['Pos_Pr'],
                                   'c_flex_pos_con_mi': my_ems_con_mi['flexopts']['ev']['Pos_Pr'],
                                   'c_flex_pos_rtp': my_ems_rtp['flexopts']['ev']['Pos_Pr'],
                                   'c_flex_neg_tou': my_ems_tou['flexopts']['ev']['Neg_Pr'],
                                   'c_flex_neg_tou_mi': my_ems_tou_mi['flexopts']['ev']['Neg_Pr'],
                                   'c_flex_neg_con': my_ems_con['flexopts']['ev']['Neg_Pr'],
                                   'c_flex_neg_con_mi': my_ems_con_mi['flexopts']['ev']['Neg_Pr'],
                                   'c_flex_neg_rtp': my_ems_rtp['flexopts']['ev']['Neg_Pr']
                                   },
                                  index=pd.date_range(start=my_ems_tou_mi['time_data']['time_slots'][0],
                                                      end=my_ems_tou_mi['time_data']['time_slots'][-1],
                                                      freq='15Min'))
    # Optimal charging power addition
    opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_tou_mi'] \
        += opt_result_df['P_ev_opt_tou_mi']
    opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_tou'] \
        += opt_result_df['P_ev_opt_tou']
    opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_con_mi'] \
        += opt_result_df['P_ev_opt_con_mi']
    opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_con'] \
        += opt_result_df['P_ev_opt_con']
    opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'P_ev_opt_sum_rtp'] \
        += opt_result_df['P_ev_opt_rtp']
    opt_sum_df.loc[opt_result_df.index[0]:opt_result_df.index[-1], 'n_veh_avail'] += 1
    # Flexible power addition
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_tou'] \
        += flex_result_df['P_pos_tou']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_tou_mi'] \
        += flex_result_df['P_pos_tou_mi']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_con'] \
        += flex_result_df['P_pos_con']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_con_mi'] \
        += flex_result_df['P_pos_con_mi']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_pos_sum_rtp'] \
        += flex_result_df['P_pos_rtp']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_tou'] \
        += flex_result_df['P_neg_tou']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_tou_mi'] \
        += flex_result_df['P_neg_tou_mi']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_con'] \
        += flex_result_df['P_neg_con']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_con_mi'] \
        += flex_result_df['P_neg_con_mi']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'P_neg_sum_rtp'] \
        += flex_result_df['P_neg_rtp']
    # Flexible energy addition
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_tou'] \
        += flex_result_df['E_pos_tou']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_tou_mi'] \
        += flex_result_df['E_pos_tou_mi']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_con'] \
        += flex_result_df['E_pos_con']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_con_mi'] \
        += flex_result_df['E_pos_con_mi']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_pos_sum_rtp'] \
        += flex_result_df['E_pos_rtp']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_tou'] \
        += flex_result_df['E_neg_tou']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_tou_mi'] \
        += flex_result_df['E_neg_tou_mi']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_con'] \
        += flex_result_df['E_neg_con']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_con_mi'] \
        += flex_result_df['E_neg_con_mi']
    flex_sum_df.loc[flex_result_df.index[0]:flex_result_df.index[-1], 'E_neg_sum_rtp'] \
        += flex_result_df['E_neg_rtp']

###########
###########
###########
###########
###########
###########
###########
###########
###########


    # lists of all flex prices for combination in for loop
    flex_prices_list = ['c_flex_pos_tou', 'c_flex_pos_tou_mi', 'c_flex_pos_con',
                        'c_flex_pos_con_mi', 'c_flex_pos_rtp', 'c_flex_neg_tou',
                        'c_flex_neg_tou_mi', 'c_flex_neg_con', 'c_flex_neg_con_mi',
                        'c_flex_neg_rtp']
    pos_neg_list = ['Pos_Pr', 'Neg_Pr']

    # preparing the columns with zeros (necessary?)
    for flexprice in flex_prices_list:
        flex_sum_df[flexprice] = 0
    # flex_sum_df['c_flex_pos_tou'] = 0
    # flex_sum_df['c_flex_pos_tou_mi'] = 0
    # flex_sum_df['c_flex_pos_con'] = 0
    # flex_sum_df['c_flex_pos_con_mi'] = 0
    # flex_sum_df['c_flex_pos_rtp'] = 0
    # flex_sum_df['c_flex_neg_tou'] = 0
    # flex_sum_df['c_flex_neg_tou_mi'] = 0
    # flex_sum_df['c_flex_neg_con'] = 0
    # flex_sum_df['c_flex_neg_con_mi'] = 0
    # flex_sum_df['c_flex_neg_rtp'] = 0

    # obtaining the max value - absolute values to not get negative prices closer to zero, but what if
    # positive prices for positive power or the other way round?
    for flexprice in flex_prices_list:
        flex_sum_df[flexprice] = np.where(flex_sum_df[flexprice].abs() <= flex_result_df[flexprice].abs(),
                                              flex_result_df[flexprice], flex_sum_df[flexprice])




        ##### alt, Unsinn
        flex_sum_df['c_flex_pos_tou_mi'] = my_ems_tou_mi['flexopts']['ev']['Pos_Pr']
        flex_sum_df['c_flex_pos_con'] = my_ems_con['flexopts']['ev']['Pos_Pr']
        flex_sum_df['c_flex_pos_con_mi'] = my_ems_con_mi['flexopts']['ev']['Pos_Pr']
        flex_sum_df['c_flex_pos_rtp'] = my_ems_rtp['flexopts']['ev']['Pos_Pr']
        flex_sum_df['c_flex_neg_tou'] = my_ems_tou['flexopts']['ev']['Neg_Pr']
        flex_sum_df['c_flex_neg_tou_mi'] = my_ems_tou_mi['flexopts']['ev']['Neg_Pr']
        flex_sum_df['c_flex_neg_con'] = my_ems_con['flexopts']['ev']['Neg_Pr']
        flex_sum_df['c_flex_neg_con_mi'] = my_ems_con_mi['flexopts']['ev']['Neg_Pr']
        flex_sum_df['c_flex_neg_rtp'] = my_ems_rtp['flexopts']['ev']['Neg_Pr']



        #### weighted average of flex prices