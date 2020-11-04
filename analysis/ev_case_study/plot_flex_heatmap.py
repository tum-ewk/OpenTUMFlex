"""
This module creates a heat map of the vehicle availabilities and the flexibility that can be offered.
"""

__author__ = "Michel Zadé"
__copyright__ = "2020 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "1.0"
__maintainer__ = "Michel Zadé"
__email__ = "michel.zade@tum.de"
__status__ = "Development"


from pandas.plotting import register_matplotlib_converters
from pathlib import Path
from matplotlib import rcParams
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
register_matplotlib_converters()


def plot_flex_heatmap(output_path='output/', save_figure=True, figure_path='figures/'):
    """
    This function plots the aggregated flexibility offers as heatmaps

    :param save_figure: boolean whether to save figure or not
    :param output_path: folder that contains single ems results
    :param figure_path: folder where figures are stored
    :return:
    """
    # Set font style
    rcParams["font.family"] = "Times New Roman"
    font_size = rcParams["font.size"] = 10
    rcParams["figure.figsize"] = [9.5, 7.16]

    # Read input from hdf files #########################################
    # Read vehicle availability data
    _11_n_veh_avail_hm = pd.read_hdf(output_path + '11/Aggregated Data/n_veh_avail_hm_data.h5', key='df')
    _37_n_veh_avail_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/n_veh_avail_hm_data.h5', key='df')
    _22_n_veh_avail_hm = pd.read_hdf(output_path + '22/Aggregated Data/n_veh_avail_hm_data.h5', key='df')
    # Read data
    _11_P_pos_tou_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_pos_tou_hm_data.h5', key='df')
    _11_P_pos_con_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_pos_con_hm_data.h5', key='df')
    _11_P_pos_tou_mi_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_pos_tou_mi_hm_data.h5', key='df')
    _11_P_pos_con_mi_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_pos_con_mi_hm_data.h5', key='df')
    _11_P_pos_rtp_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_pos_rtp_hm_data.h5', key='df')
    _11_P_neg_tou_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_neg_tou_hm_data.h5', key='df')
    _11_P_neg_con_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_neg_con_hm_data.h5', key='df')
    _11_P_neg_tou_mi_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_neg_tou_mi_hm_data.h5', key='df')
    _11_P_neg_con_mi_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_neg_con_mi_hm_data.h5', key='df')
    _11_P_neg_rtp_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_neg_rtp_hm_data.h5', key='df')
    # Read 3.7 kW data
    _37_P_pos_tou_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_pos_tou_hm_data.h5', key='df')
    _37_P_pos_con_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_pos_con_hm_data.h5', key='df')
    _37_P_pos_tou_mi_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_pos_tou_mi_hm_data.h5', key='df')
    _37_P_pos_con_mi_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_pos_con_mi_hm_data.h5', key='df')
    _37_P_pos_rtp_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_pos_rtp_hm_data.h5', key='df')
    _37_P_neg_tou_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_neg_tou_hm_data.h5', key='df')
    _37_P_neg_con_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_neg_con_hm_data.h5', key='df')
    _37_P_neg_tou_mi_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_neg_tou_mi_hm_data.h5', key='df')
    _37_P_neg_con_mi_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_neg_con_mi_hm_data.h5', key='df')
    _37_P_neg_rtp_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_neg_rtp_hm_data.h5', key='df')
    # Read 22 kW data
    _22_P_pos_tou_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_pos_tou_hm_data.h5', key='df')
    _22_P_pos_con_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_pos_con_hm_data.h5', key='df')
    _22_P_pos_tou_mi_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_pos_tou_mi_hm_data.h5', key='df')
    _22_P_pos_con_mi_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_pos_con_mi_hm_data.h5', key='df')
    _22_P_pos_rtp_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_pos_rtp_hm_data.h5', key='df')
    _22_P_neg_tou_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_neg_tou_hm_data.h5', key='df')
    _22_P_neg_con_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_neg_con_hm_data.h5', key='df')
    _22_P_neg_tou_mi_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_neg_tou_mi_hm_data.h5', key='df')
    _22_P_neg_con_mi_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_neg_con_mi_hm_data.h5', key='df')
    _22_P_neg_rtp_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_neg_rtp_hm_data.h5', key='df')

    # Set minimum and max
    p_neg_min = -15
    p_neg_max = 0
    p_pos_min = 0
    p_pos_max = 4

    # Charging power
    fig, axs = plt.subplots(nrows=5, ncols=6, sharex=True, sharey=True)
    cm = ['Greens', 'Blues_r']
    # 3.7 kW
    im = sb.heatmap(_37_P_pos_con_hm / _37_n_veh_avail_hm, ax=axs[0, 0], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
    axs[0, 0].set_title('3.7 kW', fontsize=font_size)
    axs[0, 0].set_ylabel('Con')
    sb.heatmap(_37_P_pos_tou_hm / _37_n_veh_avail_hm, ax=axs[1, 0], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
    axs[1, 0].set_ylabel('ToU')
    sb.heatmap(_37_P_pos_con_mi_hm / _37_n_veh_avail_hm, ax=axs[2, 0], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
    axs[2, 0].set_ylabel('Con + MI')
    sb.heatmap(_37_P_pos_tou_mi_hm / _37_n_veh_avail_hm, ax=axs[3, 0], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
    axs[3, 0].set_ylabel('ToU + MI')
    sb.heatmap(_37_P_pos_rtp_hm / _37_n_veh_avail_hm, ax=axs[4, 0], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
    axs[4, 0].set_ylabel('RTP')
    # 11 kW
    sb.heatmap(_11_P_pos_con_hm / _37_n_veh_avail_hm, ax=axs[0, 1], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens', edgecolors=None)
    axs[0, 1].set_title('11 kW', fontsize=font_size)
    sb.heatmap(_11_P_pos_tou_hm / _37_n_veh_avail_hm, ax=axs[1, 1], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
    sb.heatmap(_11_P_pos_con_mi_hm / _37_n_veh_avail_hm, ax=axs[2, 1], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
    sb.heatmap(_11_P_pos_tou_mi_hm / _37_n_veh_avail_hm, ax=axs[3, 1], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
    sb.heatmap(_11_P_pos_rtp_hm / _37_n_veh_avail_hm, ax=axs[4, 1], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
    # 22 kW
    sb.heatmap(_22_P_pos_con_hm / _37_n_veh_avail_hm, ax=axs[0, 2], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
    axs[0, 2].set_title('22 kW', fontsize=font_size)
    sb.heatmap(_22_P_pos_tou_hm / _37_n_veh_avail_hm, ax=axs[1, 2], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
    sb.heatmap(_22_P_pos_con_mi_hm / _37_n_veh_avail_hm, ax=axs[2, 2], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
    sb.heatmap(_22_P_pos_tou_mi_hm / _37_n_veh_avail_hm, ax=axs[3, 2], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
    sb.heatmap(_22_P_pos_rtp_hm / _37_n_veh_avail_hm, ax=axs[4, 2], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
    # axs[0, 0].set_xticklabels(_11_P_pos_con_hm.columns)
    # axs[0, 0].set_yticklabels(_11_P_pos_con_hm.index)
    mappable = im.get_children()[0]
    plt.colorbar(mappable, ax=axs[:, :3], shrink=0.6, orientation='horizontal',
                 label='Positive flexible power per available vehicle $(kW \cdot EV^{-1})$')

    # Negative Flexibility
    # 3.7 kW
    im = sb.heatmap(_37_P_neg_con_hm / _37_n_veh_avail_hm, ax=axs[0, 3], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
    axs[0, 3].set_title('3.7 kW', fontsize=font_size)
    sb.heatmap(_37_P_neg_tou_hm / _37_n_veh_avail_hm, ax=axs[1, 3], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
    sb.heatmap(_37_P_neg_con_mi_hm / _37_n_veh_avail_hm, ax=axs[2, 3], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
    sb.heatmap(_37_P_neg_tou_mi_hm / _37_n_veh_avail_hm, ax=axs[3, 3], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
    sb.heatmap(_37_P_neg_rtp_hm / _37_n_veh_avail_hm, ax=axs[4, 3], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
    # 11 kW
    sb.heatmap(_11_P_neg_con_hm / _37_n_veh_avail_hm, ax=axs[0, 4], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
    axs[0, 4].set_title('11 kW', fontsize=font_size)
    sb.heatmap(_11_P_neg_tou_hm / _37_n_veh_avail_hm, ax=axs[1, 4], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
    sb.heatmap(_11_P_neg_con_mi_hm / _37_n_veh_avail_hm, ax=axs[2, 4], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
    sb.heatmap(_11_P_neg_tou_mi_hm / _37_n_veh_avail_hm, ax=axs[3, 4], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
    sb.heatmap(_11_P_neg_rtp_hm / _37_n_veh_avail_hm, ax=axs[4, 4], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
    # 22 kW
    sb.heatmap(_22_P_neg_con_hm / _37_n_veh_avail_hm, ax=axs[0, 5], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
    axs[0, 5].set_title('22 kW', fontsize=font_size)
    sb.heatmap(_22_P_neg_tou_hm / _37_n_veh_avail_hm, ax=axs[1, 5], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
    sb.heatmap(_22_P_neg_con_mi_hm / _37_n_veh_avail_hm, ax=axs[2, 5], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
    sb.heatmap(_22_P_neg_tou_mi_hm / _37_n_veh_avail_hm, ax=axs[3, 5], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
    sb.heatmap(_22_P_neg_rtp_hm / _37_n_veh_avail_hm, ax=axs[4, 5], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
    mappable = im.get_children()[0]
    plt.colorbar(mappable, ax=axs[:, 3:],  shrink=0.6, orientation='horizontal',
                 label='Negative flexible power per available vehicle $(kW \cdot EV^{-1})$')
    # plt.colorbar(mappable, ax=axs[:, 3:],  shrink=0.6, label='Negative flexible power [kW]', location='bottom')
    plt.subplots_adjust(left=0.08, bottom=0.28, right=0.98, top=0.95, wspace=0.25, hspace=0.2)
    if save_figure:
        plt.savefig(figure_path + 'flexible_power_heatmap.png', dpi=600)

    _37_p_neg_max_con = (_37_P_neg_con_hm / _37_n_veh_avail_hm).min().min()
    _11_p_neg_max_con = (_11_P_neg_con_hm / _37_n_veh_avail_hm).min().min()
    _22_p_neg_max_con = (_22_P_neg_con_hm / _37_n_veh_avail_hm).min().min()
    _37_p_pos_max_con = (_37_P_pos_con_hm / _37_n_veh_avail_hm).max().max()
    _11_p_pos_max_con = (_11_P_pos_con_hm / _37_n_veh_avail_hm).max().max()
    _22_p_pos_max_con = (_22_P_pos_con_hm / _37_n_veh_avail_hm).max().max()
    _37_p_neg_mean_con = (_37_P_neg_con_hm / _37_n_veh_avail_hm).mean().mean()
    _11_p_neg_mean_con = (_11_P_neg_con_hm / _37_n_veh_avail_hm).mean().mean()
    _22_p_neg_mean_con = (_22_P_neg_con_hm / _37_n_veh_avail_hm).mean().mean()
    _37_p_pos_mean_con = (_37_P_pos_con_hm / _37_n_veh_avail_hm).mean().mean()
    _11_p_pos_mean_con = (_11_P_pos_con_hm / _37_n_veh_avail_hm).mean().mean()
    _22_p_pos_mean_con = (_22_P_pos_con_hm / _37_n_veh_avail_hm).mean().mean()
    _37_p_neg_max_tou = (_37_P_neg_tou_hm / _37_n_veh_avail_hm).min().min()
    _11_p_neg_max_tou = (_11_P_neg_tou_hm / _37_n_veh_avail_hm).min().min()
    _22_p_neg_max_tou = (_22_P_neg_tou_hm / _37_n_veh_avail_hm).min().min()
    _37_p_pos_max_tou = (_37_P_pos_tou_hm / _37_n_veh_avail_hm).max().max()
    _11_p_pos_max_tou = (_11_P_pos_tou_hm / _37_n_veh_avail_hm).max().max()
    _22_p_pos_max_tou = (_22_P_pos_tou_hm / _37_n_veh_avail_hm).max().max()
    _37_p_neg_mean_tou = (_37_P_neg_tou_hm / _37_n_veh_avail_hm).mean().mean()
    _11_p_neg_mean_tou = (_11_P_neg_tou_hm / _37_n_veh_avail_hm).mean().mean()
    _22_p_neg_mean_tou = (_22_P_neg_tou_hm / _37_n_veh_avail_hm).mean().mean()
    _37_p_pos_mean_tou = (_37_P_pos_tou_hm / _37_n_veh_avail_hm).mean().mean()
    _11_p_pos_mean_tou = (_11_P_pos_tou_hm / _37_n_veh_avail_hm).mean().mean()
    _22_p_pos_mean_tou = (_22_P_pos_tou_hm / _37_n_veh_avail_hm).mean().mean()
    _37_p_neg_max_con_mi = (_37_P_neg_con_mi_hm / _37_n_veh_avail_hm).min().min()
    _11_p_neg_max_con_mi = (_11_P_neg_con_mi_hm / _37_n_veh_avail_hm).min().min()
    _22_p_neg_max_con_mi = (_22_P_neg_con_mi_hm / _37_n_veh_avail_hm).min().min()
    _37_p_pos_max_con_mi = (_37_P_pos_con_mi_hm / _37_n_veh_avail_hm).max().max()
    _11_p_pos_max_con_mi = (_11_P_pos_con_mi_hm / _37_n_veh_avail_hm).max().max()
    _22_p_pos_max_con_mi = (_22_P_pos_con_mi_hm / _37_n_veh_avail_hm).max().max()
    _37_p_neg_mean_con_mi = (_37_P_neg_con_mi_hm / _37_n_veh_avail_hm).mean().mean()
    _11_p_neg_mean_con_mi = (_11_P_neg_con_mi_hm / _37_n_veh_avail_hm).mean().mean()
    _22_p_neg_mean_con_mi = (_22_P_neg_con_mi_hm / _37_n_veh_avail_hm).mean().mean()
    _37_p_pos_mean_con_mi = (_37_P_pos_con_mi_hm / _37_n_veh_avail_hm).mean().mean()
    _11_p_pos_mean_con_mi = (_11_P_pos_con_mi_hm / _37_n_veh_avail_hm).mean().mean()
    _22_p_pos_mean_con_mi = (_22_P_pos_con_mi_hm / _37_n_veh_avail_hm).mean().mean()
    _37_p_neg_max_tou_mi = (_37_P_neg_tou_mi_hm / _37_n_veh_avail_hm).min().min()
    _11_p_neg_max_tou_mi = (_11_P_neg_tou_mi_hm / _37_n_veh_avail_hm).min().min()
    _22_p_neg_max_tou_mi = (_22_P_neg_tou_mi_hm / _37_n_veh_avail_hm).min().min()
    _37_p_pos_max_tou_mi = (_37_P_pos_tou_mi_hm / _37_n_veh_avail_hm).max().max()
    _11_p_pos_max_tou_mi = (_11_P_pos_tou_mi_hm / _37_n_veh_avail_hm).max().max()
    _22_p_pos_max_tou_mi = (_22_P_pos_tou_mi_hm / _37_n_veh_avail_hm).max().max()
    _37_p_neg_mean_tou_mi = (_37_P_neg_tou_mi_hm / _37_n_veh_avail_hm).mean().mean()
    _11_p_neg_mean_tou_mi = (_11_P_neg_tou_mi_hm / _37_n_veh_avail_hm).mean().mean()
    _22_p_neg_mean_tou_mi = (_22_P_neg_tou_mi_hm / _37_n_veh_avail_hm).mean().mean()
    _37_p_pos_mean_tou_mi = (_37_P_pos_tou_mi_hm / _37_n_veh_avail_hm).mean().mean()
    _11_p_pos_mean_tou_mi = (_11_P_pos_tou_mi_hm / _37_n_veh_avail_hm).mean().mean()
    _22_p_pos_mean_tou_mi = (_22_P_pos_tou_mi_hm / _37_n_veh_avail_hm).mean().mean()
    _37_p_neg_max_rtp = (_37_P_neg_rtp_hm / _37_n_veh_avail_hm).min().min()
    _11_p_neg_max_rtp = (_11_P_neg_rtp_hm / _37_n_veh_avail_hm).min().min()
    _22_p_neg_max_rtp = (_22_P_neg_rtp_hm / _37_n_veh_avail_hm).min().min()
    _37_p_pos_max_rtp = (_37_P_pos_rtp_hm / _37_n_veh_avail_hm).max().max()
    _11_p_pos_max_rtp = (_11_P_pos_rtp_hm / _37_n_veh_avail_hm).max().max()
    _22_p_pos_max_rtp = (_22_P_pos_rtp_hm / _37_n_veh_avail_hm).max().max()
    _37_p_neg_mean_rtp = (_37_P_neg_rtp_hm / _37_n_veh_avail_hm).mean().mean()
    _11_p_neg_mean_rtp = (_11_P_neg_rtp_hm / _37_n_veh_avail_hm).mean().mean()
    _22_p_neg_mean_rtp = (_22_P_neg_rtp_hm / _37_n_veh_avail_hm).mean().mean()
    _37_p_pos_mean_rtp = (_37_P_pos_rtp_hm / _37_n_veh_avail_hm).mean().mean()
    _11_p_pos_mean_rtp = (_11_P_pos_rtp_hm / _37_n_veh_avail_hm).mean().mean()
    _22_p_pos_mean_rtp = (_22_P_pos_rtp_hm / _37_n_veh_avail_hm).mean().mean()


if __name__ == '__main__':
    plot_flex_heatmap(output_path='../output/', figure_path='../figures/')
