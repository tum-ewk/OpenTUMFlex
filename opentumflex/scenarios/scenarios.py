"""
The "scenarios.py" generate diverse scenarios to simplify the modeling procedure
"""

__author__ = "Babu Kumaran Nalini" "Michel Zadé" "Zhengjie You"
__copyright__ = "2020 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "1.0"
__maintainer__ = "Babu Kumaran Nalini"
__email__ = "babu.kumaran-nalini@tum.de"
__status__ = "Development"

from opentumflex.configuration.devices import create_device

# Input only scenario. Read all parameters from input file with no modifications
def scenario_asinput(ems):
    """ change the device parameters according to scenario heat pump 01

    Args:
        - ems: ems model instance
        
    """
    return ems


# HP only scenario
def scenario_hp(ems):
    """ change the device parameters according to scenario heat pump 01

    Args:
        - ems: ems model instance

    """

    ems['devices']['sto']['maxpow'] = 10
    ems['devices']['sto']['stocap'] = 15
    ems['devices']['boiler']['maxpow'] = 3
    ems['devices'].update(create_device(device_name='hp', minpow=0, maxpow=4, supply_temp=45))

    return ems


# PV only scenario
def scenario_pv(ems):
    """ change the device parameters according to scenario heat pump 01

    Args:
        - ems: ems model instance

    """
    ems['devices'].update(create_device(device_name='pv', minpow=0.5, maxpow=3, eta=0.95))
    ems['devices']['sto']['maxpow'] = 10
    ems['devices']['sto']['stocap'] = 15
    ems['devices']['boiler']['maxpow'] = 6
    return ems


# Battery only scenario
def scenario_bat(ems):
    """ change the device parameters according to scenario heat pump 01

    Args:
        - ems: ems model instance

    """
    ems['devices'].update(create_device(device_name='bat', minpow=0, maxpow=3, stocap=15, init_soc=0, eta=0.95))
    ems['devices']['sto']['maxpow'] = 10
    ems['devices']['sto']['stocap'] = 15
    ems['devices']['boiler']['maxpow'] = 6
    return ems


# EV only scenario
def scenario_ev(ems):
    """ change the device parameters according to scenario heat pump 01

    Args:
        - ems: ems model instance

    """
    ems['devices'].update(create_device(device_name='ev', minpow=0, maxpow=10,
                                        stocap=20, eta=0.98, timesetting=ems['time_data'],
                                        ev_aval=['2019-12-18 00:00', '2019-12-18 08:00',
                                                 '2019-12-18 18:00', '2019-12-18 23:45'],
                                        init_soc=[30, 50], end_soc=[80, 100]))
    ems['devices']['sto']['maxpow'] = 10
    ems['devices']['sto']['stocap'] = 15
    ems['devices']['boiler']['maxpow'] = 6
    return ems


# Simple house with PV and battery
def scenario_simple_house(ems):
    """ change the device parameters according to scenario heat pump 01

    Args:
        - ems: ems model instance

    """
    ems['devices'].update(create_device(device_name='pv', minpow=0.5, maxpow=3, eta=0.95))
    ems['devices'].update(create_device(device_name='bat', minpow=0, maxpow=3, stocap=5, init_soc=50, eta=0.95))
    ems['devices']['sto']['maxpow'] = 10
    ems['devices']['sto']['stocap'] = 15
    ems['devices']['boiler']['maxpow'] = 6
    return ems


# Residential house with PV, battery and HP
def scenario_residential_house(ems):
    """ change the device parameters according to scenario heat pump 01

    Args:
        - ems: ems model instance

    """
    ems['devices'].update(create_device(device_name='pv', minpow=0.5, maxpow=3, eta=0.95))
    ems['devices'].update(create_device(device_name='bat', minpow=0, maxpow=3, stocap=5, init_soc=5, eta=0.95))
    ems['devices']['sto']['maxpow'] = 10
    ems['devices']['sto']['stocap'] = 15
    ems['devices']['boiler']['maxpow'] = 3
    ems['devices'].update(create_device(device_name='hp', minpow=0, maxpow=4, supply_temp=45))
    return ems


# Apartment with PV, battery, HP and EV
def scenario_mini_apartment(ems):
    """ change the device parameters according to scenario heat pump 01

    Args:
        - ems: ems model instance

    """
    ems['devices'].update(create_device(device_name='pv', minpow=0.5, maxpow=3, eta=0.95))
    ems['devices'].update(create_device(device_name='bat', minpow=0, maxpow=3, stocap=5, init_soc=50, eta=0.95))
    ems['devices']['sto']['maxpow'] = 10
    ems['devices']['sto']['stocap'] = 15
    ems['devices']['boiler']['maxpow'] = 3
    ems['devices'].update(create_device(device_name='hp', minpow=0, maxpow=4, supply_temp=45))
    ems['devices'].update(create_device(device_name='ev', minpow=0, maxpow=8,
                                        stocap=20, eta=0.98, timesetting=ems['time_data'],
                                        ev_aval=['2019-12-18 00:00', '2019-12-18 08:00',
                                                 '2019-12-18 18:00', '2019-12-18 23:45'],
                                        init_soc=[30, 50], end_soc=[80, 100]))
    return ems


# Apartment with PV, battery, HP, CHP and EV
def scenario_apartment(ems):
    """ change the device parameters according to scenario heat pump 01

    Args:
        - ems: ems model instance

    """
    ems['devices'].update(create_device(device_name='pv', minpow=0.5, maxpow=3, eta=0.95))
    ems['devices'].update(create_device(device_name='bat', minpow=0, maxpow=3, stocap=5, init_soc=50, eta=0.95))
    ems['devices']['chp']['maxpow'] = 2
    ems['devices']['sto']['maxpow'] = 10
    ems['devices']['sto']['stocap'] = 15
    ems['devices']['boiler']['maxpow'] = 3
    ems['devices'].update(create_device(device_name='hp', minpow=0, maxpow=4, supply_temp=45))
    ems['devices'].update(create_device(device_name='ev', minpow=0, maxpow=8,
                                        stocap=20, eta=0.98, timesetting=ems['time_data'],
                                        ev_aval=['2019-12-18 00:00', '2019-12-18 08:00',
                                                 '2019-12-18 18:00', '2019-12-18 23:45'],
                                        init_soc=[30, 50], end_soc=[80, 100]))
    return ems


# For testing purpose only. Try all combinations of scenarios
def scenario_combination_test(my_ems, test_code):
    """
    

    Parameters
    ----------
    my_ems : dict
        ems model
    test_code : string
        Device availability booleans merged as string.

    Returns
    -------
    my_ems : dict
        ems model.

    """
    s_pv = int(test_code[0])
    s_bat = int(test_code[1])
    s_ev = int(test_code[2])
    s_hp = int(test_code[3])
    s_chp = int(test_code[4])

    # add or change the utility/devices
    my_ems['devices']['boiler']['maxpow'] = 4
    if s_chp: my_ems['devices']['chp']['maxpow'] = 2
    if s_hp: my_ems['devices'].update(create_device(device_name='hp', minpow=0, maxpow=2, supply_temp=45))
    if s_pv: my_ems['devices'].update(create_device(device_name='pv', minpow=0.5, maxpow=3, eta=0.95))
    if s_bat: my_ems['devices'].update(
        create_device(device_name='bat', minpow=0.5, maxpow=3, stocap=5, init_soc=45, eta=0.95))
    if s_ev: my_ems['devices'].update(create_device(device_name='ev', minpow=0, maxpow=11,
                                                    stocap=20, eta=0.98, timesetting=my_ems['time_data'],
                                                    ev_aval=['2019-12-18 00:00', '2019-12-18 08:00',
                                                             '2019-12-18 18:00', '2019-12-18 23:45'],
                                                    init_soc=[30, 50], end_soc=[80, 100]))

    if not s_chp: my_ems['devices']['chp']['maxpow'] = 0
    if not s_hp: my_ems['devices'].update(create_device(device_name='hp', minpow=0, maxpow=0, supply_temp=45))
    if not s_pv: my_ems['devices'].update(create_device(device_name='pv', minpow=0, maxpow=0, eta=0.95))
    if not s_bat: my_ems['devices'].update(
        create_device(device_name='bat', minpow=0, maxpow=0, stocap=0, init_soc=0, eta=0.95))
    if not s_ev: my_ems['devices'].update(create_device(device_name='ev', minpow=0, maxpow=0,
                                                        stocap=20, eta=0.98, timesetting=my_ems['time_data'],
                                                        ev_aval=['2019-12-18 00:00', '2019-12-18 08:00',
                                                                 '2019-12-18 18:00', '2019-12-18 23:45'],
                                                        init_soc=[30, 50], end_soc=[80, 100]))

    return my_ems


def scenario_customized(ems):
    """ change the device parameters and obtain the input time series
        according to customized scenario from spreadsheet(xlsx)
        this function is only a placeholder, which serves as tag for selector in run_scenario.py

    Args:
        - ems: ems model instance
    """

    return ems
