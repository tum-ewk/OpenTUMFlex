"""
The calc_overall_cost module calculates and plots the overall costs of all calculated optimal charging procedures.
"""

__author__ = "Michel Zadé"
__copyright__ = "2020 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "1.0"
__maintainer__ = "Michel Zadé"
__email__ = "michel.zade@tum.de"
__status__ = "Development"

import os
import opentumflex


def calc_overall_cost(output_path='output/'):
    """
    This function calculates the overall costs of the optimal charging schedules

    :return:
    """

    # List all file names, for all scenarios (ToU & Constant, with and without minimally increasing prices) the same
    folder_names = os.listdir(output_path)
    # Initialize variables
    _37_total_cost_tou = 0
    _37_total_cost_con = 0
    _37_total_cost_tou_mi = 0
    _37_total_cost_con_mi = 0
    _37_total_cost_rtp = 0
    _11_total_cost_tou = 0
    _11_total_cost_con = 0
    _11_total_cost_tou_mi = 0
    _11_total_cost_con_mi = 0
    _11_total_cost_rtp = 0
    _22_total_cost_tou = 0
    _22_total_cost_con = 0
    _22_total_cost_tou_mi = 0
    _22_total_cost_con_mi = 0
    _22_total_cost_rtp = 0
    # Go through all sub-folders and the files therein and add the costs up
    for folder_name in folder_names:
        # Get all file names in folder
        file_names = os.listdir(output_path + folder_name + '/ToU/')
        total_cost_tou = 0
        total_cost_con = 0
        total_cost_tou_mi = 0
        total_cost_con_mi = 0
        total_cost_rtp = 0

        # read all results and store them in result lists
        for result_name in file_names[:]:
            # print('Folder: ' + folder_name + ' ### File: ' + result_name)
            my_ems_tou_mi = opentumflex.init_ems_js(path=output_path + folder_name + '/ToU_mi/' + result_name)
            my_ems_tou = opentumflex.init_ems_js(path=output_path + folder_name + '/ToU/' + result_name)
            my_ems_const_mi = opentumflex.init_ems_js(path=output_path + folder_name + '/Con_mi/' + result_name)
            my_ems_const = opentumflex.init_ems_js(path=output_path + folder_name + '/Constant/' + result_name)
            my_ems_rtp = opentumflex.init_ems_js(path=output_path + folder_name + '/RTP/' + result_name)

            total_cost_tou += sum([a * b for a, b in zip(my_ems_tou['fcst']['ele_price_in'], my_ems_tou['optplan']['EV_power'])]) * 0.25
            total_cost_con += sum([a * b for a, b in zip(my_ems_const['fcst']['ele_price_in'], my_ems_const['optplan']['EV_power'])]) * 0.25
            total_cost_tou_mi += sum([a * b for a, b in zip(my_ems_tou_mi['fcst']['ele_price_in'], my_ems_tou_mi['optplan']['EV_power'])]) * 0.25
            total_cost_con_mi += sum([a * b for a, b in zip(my_ems_const_mi['fcst']['ele_price_in'], my_ems_const_mi['optplan']['EV_power'])]) * 0.25
            total_cost_rtp += sum([a * b for a, b in zip(my_ems_rtp['fcst']['ele_price_in'], my_ems_rtp['optplan']['EV_power'])]) * 0.25

        if folder_name == '3.7':
            _37_total_cost_tou = total_cost_tou
            _37_total_cost_con = total_cost_con
            _37_total_cost_tou_mi = total_cost_tou_mi
            _37_total_cost_con_mi = total_cost_con_mi
            _37_total_cost_rtp = total_cost_rtp
        elif folder_name == '11':
            _11_total_cost_tou = total_cost_tou
            _11_total_cost_con = total_cost_con
            _11_total_cost_tou_mi = total_cost_tou_mi
            _11_total_cost_con_mi = total_cost_con_mi
            _11_total_cost_rtp = total_cost_rtp
        elif folder_name == '22':
            _22_total_cost_tou = total_cost_tou
            _22_total_cost_con = total_cost_con
            _22_total_cost_tou_mi = total_cost_tou_mi
            _22_total_cost_con_mi = total_cost_con_mi
            _22_total_cost_rtp = total_cost_rtp

    # Calculate overall costs of different charging powers and pricing strategies
    _37_total_cost = _37_total_cost_tou + _37_total_cost_con + _37_total_cost_tou_mi + _37_total_cost_con_mi + _37_total_cost_rtp
    _11_total_cost = _11_total_cost_tou + _11_total_cost_con + _11_total_cost_tou_mi + _11_total_cost_con_mi + _11_total_cost_rtp
    _22_total_cost = _22_total_cost_tou + _22_total_cost_con + _22_total_cost_tou_mi + _22_total_cost_con_mi + _22_total_cost_rtp

    overall_costs = {'_37_total_cost_tou': _37_total_cost_tou,
                     '_37_total_cost_con': _37_total_cost_con,
                     '_37_total_cost_tou_mi': _37_total_cost_tou_mi,
                     '_37_total_cost_con_mi': _37_total_cost_con_mi,
                     '_37_total_cost_rtp': _37_total_cost_rtp,
                     '_37_total_cost': _37_total_cost,
                     '_11_total_cost_tou': _11_total_cost_tou,
                     '_11_total_cost_con': _11_total_cost_con,
                     '_11_total_cost_tou_mi': _11_total_cost_tou_mi,
                     '_11_total_cost_con_mi': _11_total_cost_con_mi,
                     '_11_total_cost_rtp': _11_total_cost_rtp,
                     '_11_total_cost': _11_total_cost,
                     '_22_total_cost_tou': _22_total_cost_tou,
                     '_22_total_cost_con': _22_total_cost_con,
                     '_22_total_cost_tou_mi': _22_total_cost_tou_mi,
                     '_22_total_cost_con_mi': _22_total_cost_con_mi,
                     '_22_total_cost_rtp': _22_total_cost_rtp,
                     '_22_total_cost': _22_total_cost}

    return overall_costs


if __name__ == '__main__':
    output_data = '../output/'

    overall_cost = calc_overall_cost(output_path=output_data)

