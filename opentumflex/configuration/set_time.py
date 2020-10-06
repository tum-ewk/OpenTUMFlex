from opentumflex.configuration.init_ems import update_time_data
from opentumflex.configuration.devices import devices


def initialize_time_setting(t_inval, start_time, end_time, d_inval=15, days=1):
    """ create one ems object only with basic time settings

    Args:
        - t_inval: global time interval (minutes) in the ems object including optimization, flexibility calculation, saving
          results and plotting
        - start_time: start time in format 'yyyy-MM-dd HH:mm' to be simulated
        - end_time: end time in format 'yyyy-MM-dd HH:mm' to be simulated
        - d_inval: time interval of input data (xlsx or csv) in minutes
        - days: determine how many days the simulation lasts

    Returns:
        ems object with basic time settings

    """
    ems = {'time_data': {}}
    ems['time_data']['t_inval'] = t_inval  # set the time interval in OpenTUMFlex
    ems['time_data']['d_inval'] = d_inval  # set the t ime inverval of the input data (load profiles, prices, weather..)
    ems['time_data']['start_time'] = start_time  # '2019-12-18 00:00'
    ems['time_data']['end_time'] = end_time  # '2019-12-18 23:45'
    ems['time_data']['days'] = days
    ems.update(update_time_data(ems))

    # Initialize EMS
    initialize_ems(ems)

    return ems


def initialize_ems(my_ems):
    """ assign default values to the device parameters (Power=0, ...)

    :param my_ems: ems object
    :return: none
    """
    key_new = {'devices': {}, 'flexopts': {}, 'optplan': {}, 'reoptim': {}}
    my_ems.update(key_new)
    dict_devices_normal = ['hp', 'boiler', 'pv', 'sto', 'bat']
    for device_name in dict_devices_normal:
        my_ems['devices'].update(devices(device_name=device_name, minpow=0, maxpow=0))
        my_ems['devices'].update(devices(device_name='chp', minpow=0, maxpow=0, eta=[0.5, 0.5]))
        my_ems['devices'].update(devices(device_name='ev', minpow=0, maxpow=0, stocap=0, eta=0.98,
                                         init_soc=[20], end_soc=[20],
                                         ev_aval=[my_ems['time_data']['start_time'],
                                                  my_ems['time_data']['end_time']],
                                         timesetting=my_ems['time_data']))
