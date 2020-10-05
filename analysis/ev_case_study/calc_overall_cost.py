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
import matplotlib.pyplot as plt
import opentumflex
from matplotlib import rcParams


def calc_overall_cost():
    """
    This function calculates the overall costs of the optimal charging schedules

    :return:
    """
    # Preparation ###################################################
    # Output and input path
    output_path = 'output/'
    # List all file names, for all scenarios (ToU & Constant, with and without minimally increasing prices) the same
    folder_names = os.listdir(output_path)
    """
    #################################################################################
    # Read opentumflex results, sum charging power, flexibility and veh availability ########
    #################################################################################
    """
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
            my_ems_tou_mi = opentumflex.ems(initialize=True, path=output_path + folder_name + '/ToU_mi/' + result_name)
            my_ems_tou = opentumflex.ems(initialize=True, path=output_path + folder_name + '/ToU/' + result_name)
            my_ems_const_mi = opentumflex.ems(initialize=True, path=output_path + folder_name + '/Con_mi/' + result_name)
            my_ems_const = opentumflex.ems(initialize=True, path=output_path + folder_name + '/Constant/' + result_name)
            my_ems_rtp = opentumflex.ems(initialize=True, path=output_path + folder_name + '/RTP/' + result_name)

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

    # Create a bar plot showing the different prices
    # Set font/figure style
    rcParams["font.family"] = "Times New Roman"
    rcParams["font.size"] = 10
    rcParams["figure.figsize"] = [3.5, 2.5]
    chts_color = 'tab:blue'
    mp_color = 'brown'

    # Subplots
    ax = plt.subplot(111)
    w = 0.5
    x = [3.7, 11, 22]
    ax.bar([i - 2*w for i in x], [_37_total_cost_con, _11_total_cost_con, _22_total_cost_con],
           label='Con', width=w, color='b', align='center')
    ax.bar([i - 1*w for i in x], [_37_total_cost_con_mi, _11_total_cost_con_mi, _22_total_cost_con_mi], label='Con + MI', width=w)
    ax.bar(x, [_37_total_cost_tou, _11_total_cost_tou, _22_total_cost_tou], label='ToU', width=w)
    ax.bar([i + 1*w for i in x], [_37_total_cost_tou_mi, _11_total_cost_tou_mi, _22_total_cost_tou_mi], label='ToU + MI', width=w)
    ax.bar([i + 2*w for i in x], [_37_total_cost_rtp, _11_total_cost_rtp, _22_total_cost_rtp], label='RTP', width=w)
    ax.xaxis_date()
    ax.autoscale(tight=True)
    # ax.set_xlim([0, 25])
    # ax.set_ylim([0, 16000])
    ax.set_xticks(x)
    ax.legend(loc='lower right')
    ax.grid(axis='y')
    ax.set_xlabel('Maximum Charging Power Level (kW)')
    ax.set_ylabel('Cumulated Charging Costs (€)')
    ax.set_xticklabels(['3.7', '11', '22'])
    plt.subplots_adjust(left=0.2, bottom=0.2, right=0.95, top=0.95, wspace=0.2, hspace=0.2)
    plt.savefig('figures\\' + 'Total_charging_cost' + '.png', dpi=600)

    print('Finished')

    return total_cost_tou, total_cost_con, total_cost_tou_mi, total_cost_con_mi, total_cost_rtp


if __name__ == '__main__':
    calc_overall_cost()
