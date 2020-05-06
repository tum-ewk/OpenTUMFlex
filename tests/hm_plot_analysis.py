import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm as cmap
from matplotlib import rcParams
import os
import numpy as np
import seaborn as sb
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Set font style
rcParams["font.family"] = "Times New Roman"
rcParams["font.size"] = 10
rcParams["figure.figsize"] = [11.69, 8.27]

"""
####################################################################
# Read data from hdf files #########################################
####################################################################
"""
# Output and input path
output_path = 'C:/Users/ga47num/PycharmProjects/US CHTS - OpenTUMFlex - EV/Output/'
# Read data
_11_P_pos_tou_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_pos_tou_hm_data.h5', key='df')
_11_P_pos_const_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_pos_const_hm_data.h5', key='df')
_11_P_pos_tou_mi_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_pos_tou_mi_hm_data.h5', key='df')
_11_P_pos_const_mi_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_pos_const_mi_hm_data.h5', key='df')
_11_P_pos_rtp_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_pos_rtp_hm_data.h5', key='df')
_11_P_neg_tou_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_neg_tou_hm_data.h5', key='df')
_11_P_neg_const_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_neg_const_hm_data.h5', key='df')
_11_P_neg_tou_mi_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_neg_tou_mi_hm_data.h5', key='df')
_11_P_neg_const_mi_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_neg_const_mi_hm_data.h5', key='df')
_11_P_neg_rtp_hm = pd.read_hdf(output_path + '11/Aggregated Data/P_neg_rtp_hm_data.h5', key='df')
# Read 3.7 kW data
_37_P_pos_tou_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_pos_tou_hm_data.h5', key='df')
_37_P_pos_const_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_pos_const_hm_data.h5', key='df')
_37_P_pos_tou_mi_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_pos_tou_mi_hm_data.h5', key='df')
_37_P_pos_const_mi_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_pos_const_mi_hm_data.h5', key='df')
_37_P_pos_rtp_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_pos_rtp_hm_data.h5', key='df')
_37_P_neg_tou_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_neg_tou_hm_data.h5', key='df')
_37_P_neg_const_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_neg_const_hm_data.h5', key='df')
_37_P_neg_tou_mi_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_neg_tou_mi_hm_data.h5', key='df')
_37_P_neg_const_mi_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_neg_const_mi_hm_data.h5', key='df')
_37_P_neg_rtp_hm = pd.read_hdf(output_path + '3.7/Aggregated Data/P_neg_rtp_hm_data.h5', key='df')
# Read 22 kW data
_22_P_pos_tou_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_pos_tou_hm_data.h5', key='df')
_22_P_pos_const_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_pos_const_hm_data.h5', key='df')
_22_P_pos_tou_mi_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_pos_tou_mi_hm_data.h5', key='df')
_22_P_pos_const_mi_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_pos_const_mi_hm_data.h5', key='df')
_22_P_pos_rtp_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_pos_rtp_hm_data.h5', key='df')
_22_P_neg_tou_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_neg_tou_hm_data.h5', key='df')
_22_P_neg_const_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_neg_const_hm_data.h5', key='df')
_22_P_neg_tou_mi_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_neg_tou_mi_hm_data.h5', key='df')
_22_P_neg_const_mi_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_neg_const_mi_hm_data.h5', key='df')
_22_P_neg_rtp_hm = pd.read_hdf(output_path + '22/Aggregated Data/P_neg_rtp_hm_data.h5', key='df')

# Set minimum and max
p_neg_min = -50
p_neg_max = 0
p_pos_min = 0
p_pos_max = 20

# Charging power
fig3, axs = plt.subplots(nrows=5, ncols=6, sharex=True, sharey=True)
cm = ['Greens', 'Blues_r']
# 3.7 kW
im = sb.heatmap(_37_P_pos_tou_hm, ax=axs[0, 0], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
axs[0, 0].set_title('3.7 kW')
axs[0, 0].set_ylabel('ToU')
sb.heatmap(_37_P_pos_const_hm, ax=axs[1, 0], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
axs[1, 0].set_ylabel('Constant')
sb.heatmap(_37_P_pos_tou_mi_hm, ax=axs[2, 0], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
axs[2, 0].set_ylabel('ToU_mi')
sb.heatmap(_37_P_pos_const_mi_hm, ax=axs[3, 0], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
axs[3, 0].set_ylabel('Constant_mi')
sb.heatmap(_37_P_pos_rtp_hm, ax=axs[4, 0], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
axs[4, 0].set_ylabel('RTP')
# 11 kW
sb.heatmap(_11_P_pos_tou_hm, ax=axs[0, 1], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens', edgecolors=None)
axs[0, 1].set_title('11 kW')
sb.heatmap(_11_P_pos_const_hm, ax=axs[1, 1], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
sb.heatmap(_11_P_pos_tou_mi_hm, ax=axs[2, 1], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
sb.heatmap(_11_P_pos_const_mi_hm, ax=axs[3, 1], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
sb.heatmap(_11_P_pos_rtp_hm, ax=axs[4, 1], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
# 22 kW
sb.heatmap(_22_P_pos_tou_hm, ax=axs[0, 2], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
axs[0, 2].set_title('22 kW')
sb.heatmap(_22_P_pos_const_hm, ax=axs[1, 2], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
sb.heatmap(_22_P_pos_tou_mi_hm, ax=axs[2, 2], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
sb.heatmap(_22_P_pos_const_mi_hm, ax=axs[3, 2], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
sb.heatmap(_22_P_pos_rtp_hm, ax=axs[4, 2], cbar=False, vmin=p_pos_min, vmax=p_pos_max, cmap='Greens')
axs[0, 0].set_xticklabels(_11_P_pos_const_hm.columns)
axs[0, 0].set_yticklabels(_11_P_pos_const_hm.index)
mappable = im.get_children()[0]
plt.colorbar(mappable, ax=axs[:, :3], shrink=0.6, orientation='horizontal', label='Positive flexible power [kW]')

# Negative Flexibility
# 3.7 kW
im = sb.heatmap(_37_P_neg_tou_hm, ax=axs[0, 3], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
axs[0, 3].set_title('3.7 kW')
sb.heatmap(_37_P_neg_const_hm, ax=axs[1, 3], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
sb.heatmap(_37_P_neg_tou_mi_hm, ax=axs[2, 3], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
sb.heatmap(_37_P_neg_const_mi_hm, ax=axs[3, 3], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
sb.heatmap(_37_P_neg_rtp_hm, ax=axs[4, 3], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
# 11 kW
sb.heatmap(_11_P_neg_tou_hm, ax=axs[0, 4], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
axs[0, 4].set_title('11 kW')
sb.heatmap(_11_P_neg_const_hm, ax=axs[1, 4], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
sb.heatmap(_11_P_neg_tou_mi_hm, ax=axs[2, 4], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
sb.heatmap(_11_P_neg_const_mi_hm, ax=axs[3, 4], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
sb.heatmap(_11_P_neg_rtp_hm, ax=axs[4, 4], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
# 22 kW
sb.heatmap(_22_P_neg_tou_hm, ax=axs[0, 5], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
axs[0, 5].set_title('22 kW')
sb.heatmap(_22_P_neg_const_hm, ax=axs[1, 5], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
sb.heatmap(_22_P_neg_tou_mi_hm, ax=axs[2, 5], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
sb.heatmap(_22_P_neg_const_mi_hm, ax=axs[3, 5], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
sb.heatmap(_22_P_neg_rtp_hm, ax=axs[4, 5], cbar=False, vmin=p_neg_min, vmax=p_neg_max, cmap='Blues_r')
mappable = im.get_children()[0]
plt.colorbar(mappable, ax=axs[:, 3:],  shrink=0.6, orientation='horizontal', label='Negative flexible power [kW]')

fig3.subplots_adjust(bottom=0.28) # or whatever

plt.savefig(output_path + 'Flexible_power.png', dpi=600)