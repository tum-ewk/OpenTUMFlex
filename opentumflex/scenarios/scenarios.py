from opentumflex.configuration.devices import create_device


def scenario_hp01(ems):
    """ change the device parameters according to scenario heat pump 01

    Args:
        - ems: ems model instance

    """

    ems['devices']['sto']['maxpow'] = 10
    ems['devices']['sto']['stocap'] = 15
    ems['devices']['boiler']['maxpow'] = 3
    ems['devices'].update(create_device(device_name='hp', minpow=0, maxpow=4, supply_temp=45))

    return ems
