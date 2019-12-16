import pandas as pd

from ems.ems_mod import ems as ems_loc
from ems.devices.devices import devices as dev
from ems.devices.devices import device_write as dev_write
from tests.fcst import load_data as input_data
from ems.optim.opt_test import run_hp_opt as opt
# from ems.flex.flexhp import flexhp as flexhp
from ems.ems_mod import ems_write as ems_loc_write
from ems.flex.plot import plot_flex as plot
from ems.flex.flex_draw import plot_flex as plot_flex
from ems.flex.flex_draw import save_results as save_results
from ems.flex.flexhp import calc_flex_hp
from ems.flex.flexchp import calc_flex_chp
from ems.flex.Bat import Batflex
from ems.flex.PV import PVflex

path = r"C:\Users\ge57vam\emsflex\tests\config.xlsx"
technic_config = pd.read_excel(path, sheet_name='technical_config', usecols='B:AY', nrows=170)
elec_load = pd.read_excel(path, sheet_name='elec_load', usecols='A:AX', nrows=170)
heat_load = pd.read_excel(path, sheet_name='heat_load', usecols='A:AX', nrows=170)
elec_price_in = pd.read_excel(path, sheet_name='elec_price_in', usecols='A:AX')
elec_price_out = pd.read_excel(path, sheet_name='elec_price_out', usecols='A:AX', nrows=170)
gas_price = pd.read_excel(path, sheet_name='gas_price', usecols='A:AX', nrows=170)
temperature = pd.read_excel(path, sheet_name='temperature', usecols='A:AX', nrows=170)
solar = pd.read_excel(path, sheet_name='solar', usecols='A:AX', nrows=170)

# create my_ems
my_ems = ems_loc(initialize=True, path='C:/Users/ge57vam/emsflex/ems/test_chp.txt')
day = 7
day_type = "Sun"

fcst = {'temp': list(temperature.iloc[(day - 1) * 24:(day * 24), 0]),
        'solar': list(solar.iloc[(day - 1) * 24:(day * 24), 0]),
        'last_heat': 0,
        'last_elec': 0,
        'ele_price_in': list(elec_price_in.iloc[(day - 1) * 24:(day * 24), 0]),
        'gas': list(gas_price.iloc[(day - 1) * 24:(day * 24), 0]),
        'ele_price_out': list(elec_price_out.iloc[(day - 1) * 24:(day * 24), 0])}

# hp
hp_pow = technic_config.iloc[1]
# heat storage
hs_cap = technic_config.iloc[4]
# boiler
boli_pow = technic_config.iloc[6]
# chp
chp_pow = technic_config.iloc[8]
# pv
pv_pow = technic_config.iloc[12]
# bat
bat_cap = technic_config.iloc[14]

nr_haushalt_start = 1
nr_haushalt_end = 3

for i in range(nr_haushalt_start, nr_haushalt_end + 1):
    print(i)

    my_ems['devices'].update(dev(device_name='hp', minpow=0, maxpow=hp_pow[i - 1] + 0.0001))
    # my_ems['devices'].update(dev(device_name='hp', minpow=0, maxpow=3))
    my_ems['devices']['sto']['stocap'] = hs_cap[i - 1]
    my_ems['devices']['boiler']['maxpow'] = boli_pow[i - 1]
    my_ems['devices']['chp']['maxpow'] = chp_pow[i - 1] + 0.00001
    my_ems['devices']['pv']['maxpow'] = pv_pow[i - 1] / 0.3
    my_ems['devices']['bat']['stocap'] = bat_cap[i - 1] + 0.001
    my_ems['devices']['bat']['maxpow'] = bat_cap[i - 1] + 0.01
    my_ems['devices']['ev']['maxpow'] = 0

    # my_ems['devices']['sto']['stocap'] = 24
    # my_ems['devices']['boiler']['maxpow'] = 20
    # my_ems['devices']['chp']['maxpow'] = 0.01
    # my_ems['devices']['pv']['maxpow'] = 5
    # my_ems['devices']['bat']['stocap'] = 10
    # my_ems['devices']['bat']['maxpow'] = 5
    # my_ems['devices']['ev']['maxpow'] = 2

    fcst['last_heat'] = list(heat_load.iloc[(day - 1) * 24:(day * 24), i - 1])
    fcst['last_elec'] = list(elec_load.iloc[(day - 1) * 24:(day * 24), i - 1])

    my_ems['fcst'] = fcst
    my_ems['optplan'] = opt(my_ems, plot_fig=False, result_folder='C:/data/')

    if hp_pow[i - 1] > 0.1:
        my_ems['flexopts']['hp'] = calc_flex_hp(my_ems)
        save_results(my_ems['flexopts']['hp'], "C:\data" + "\haushalt_" + str(i) + "_" + day_type + "_hp.csv")
    if chp_pow[i - 1] > 0.1:
        my_ems['flexopts']['chp'] = calc_flex_chp(my_ems)
        save_results(my_ems['flexopts']['chp'], "C:\data" + "\haushalt_" + str(i) + "_" + day_type + "_chp.csv")
    if bat_cap[i - 1] > 0.1:
        my_ems['flexopts']['bat'] = Batflex(my_ems)
        save_results(my_ems['flexopts']['bat'], "C:\data" + "\haushalt_" + str(i) + "_" + day_type + "_bat.csv")
    if pv_pow[i - 1] > 0.1:
        my_ems['flexopts']['pv'] = PVflex(my_ems)
        save_results(my_ems['flexopts']['pv'], "C:\data" + "\haushalt_" + str(i) + "_" + day_type + "_pv.csv")
