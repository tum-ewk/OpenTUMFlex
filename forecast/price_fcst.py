import pandas as pd
import numpy as np


def get_elect_price_fcst(t_start=pd.Timestamp('2020-1-1 00:00'), t_end=pd.Timestamp('2020-1-1 23:45')):
    # Create a dataframe with placeholders
    price_fcst = pd.DataFrame(-1, columns={'Constant', 'ToU', 'EPEX', 'Random'},
                              index=pd.date_range(start=t_start, end=t_end, freq='15 Min'))

    # Set constant prices ############################################
    # Add an increasing quantity for the solver to always choose the first available slots
    price_fcst['Constant'] = 0.30 + np.linspace(start=0.0001, stop=0.0002, num=len(price_fcst))

    # Set time-of-use tariff prices ##################################
    # According to TOU-D-PRIME: https://www.sce.com/residential/rates/Time-Of-Use-Residential-Rate-Plans
    off_peak_summer_rate = 0.14
    mid_peak_summer_rate = 0.27
    on_peak_summer_rate = 0.39
    super_off_peak_winter_rate = 0.13
    mid_peak_winter_rate = 0.36

    # Go through all time slots and assign appropriate rate
    for i in range(len(price_fcst)):
        # Check for winter or summer rate
        # Summer rate from june till september (6-9)
        if 6 <= price_fcst.index[i].month <= 9:
            # Check weekday (0-4)
            if price_fcst.index[i].weekday() < 5:
                # Check on peak period(4pm - 9pm):
                if 16 <= price_fcst.index[i].hour <= 21:
                    price_fcst['ToU'].iloc[i] = on_peak_summer_rate
                # Off peak period
                else:
                    price_fcst['ToU'].iloc[i] = off_peak_summer_rate
            # Weekend
            else:
                # Check on peak period(4pm - 9pm):
                if 16 <= price_fcst.index[i].hour <= 21:
                    price_fcst['ToU'].iloc[i] = mid_peak_summer_rate
                # Off peak period
                else:
                    price_fcst['ToU'].iloc[i] = off_peak_summer_rate
        # Winter months
        else:
            # Weekdays and weekends are the same
            # Check mid peak period(4pm - 9pm):
            if 16 <= price_fcst.index[i].hour <= 21:
                price_fcst['ToU'].iloc[i] = mid_peak_winter_rate
            # Super off-peak period
            else:
                price_fcst['ToU'].iloc[i] = super_off_peak_winter_rate

    # Set random and EPEX prices ##################################
    price_fcst['EPEX'] = np.random.rand(len(price_fcst))*0.1 + 0.25
    price_fcst['Random'] = np.random.rand(len(price_fcst)) * 0.1 + 0.25

    return price_fcst
