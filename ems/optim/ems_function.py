from ems.init_ems import update_time_data


def initialize_time_setting(t_inval, start_time, end_time, d_inval=15, days=1):
    """ create one ems model only with basic time settings

    Args:
        - t_inval: global time interval (minutes) in ems environment including optimization, flexibility calculation, saving
          results and plotting
        - start_time: start time in format 'yyyy-MM-dd HH:mm' to be simulated
        - end_time: end time in format 'yyyy-MM-dd HH:mm' to be simulated
        - d_inval: time interval of input data (xlsx or csv) in minutes
        - days: determine how many days the simulation lasts

    Returns:
        ems model with basic time settings

    """
    ems = {'time_data': {}}
    ems['time_data']['t_inval'] = t_inval  # set the time interval in OpenTUMFlex
    ems['time_data']['d_inval'] = d_inval  # set the t ime inverval of the input data (load profiles, prices, weather..)
    ems['time_data']['start_time'] = start_time  # '2019-12-18 00:00'
    ems['time_data']['end_time'] = end_time  # '2019-12-18 23:45'
    ems['time_data']['days'] = days
    ems.update(update_time_data(ems))
    return ems
