"""
The price_fcst_sim.py module simulates an artificial price forecast for a specific time.
"""

__author__ = "Michel Zadé"
__copyright__ = "2020 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "1.0"
__maintainer__ = "Michel Zadé"
__email__ = "michel.zade@tum.de"
__status__ = "Development"

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


def simulate_elect_price_fcst(rtp_input_data_path='../analysis/input/RTP/',
                              t_start=pd.Timestamp('2020-1-1 00:00'),
                              t_end=pd.Timestamp('2020-1-1 23:45'),
                              pr_constant=0.20,
                              pricing={'ToU', 'Constant', 'Con_mi', 'ToU_mi', 'RTP'}):
    """
    This function simulates an electricity price forecast. ToU tariffs are from Southern California Edison, RTP from
     ComEd, Illinois, Constant prices can be inserted.

    :param rtp_input_data_path: path to rtp h5 files
    :param t_start: Start time in quarter hours as pandas time stamp
    :param t_end:   end time in quarter hours as pandas time stamp
    :param pr_constant: constant electricity price, default is 20 ct/kWh
    :param pricing: defines which pricing strategies shall be inserted

    :return: returns a input frame with ToU, Constant and RTP prices
    """
    # Check whether start time is before end time otherwise return
    if t_start >= t_end:
        return

    # Create a dataframe with placeholders
    price_fcst = pd.DataFrame(-1, columns=pricing, index=pd.date_range(start=t_start, end=t_end, freq='15 Min'))

    # Set constant prices ############################################
    if 'Constant' in price_fcst.columns:
        price_fcst['Constant'] = pr_constant

    # Set time-of-use tariff prices ##################################
    if 'ToU' in price_fcst.columns:
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
                    if 16 <= price_fcst.index[i].hour < 21:
                        price_fcst.loc[price_fcst.index[i], 'ToU'] = on_peak_summer_rate
                    # Off peak period
                    else:
                        price_fcst.loc[price_fcst.index[i], 'ToU'] = off_peak_summer_rate
                # Weekend
                else:
                    # Check on peak period(4pm - 9pm):
                    if 16 <= price_fcst.index[i].hour < 21:
                        price_fcst.loc[price_fcst.index[i], 'ToU'] = mid_peak_summer_rate
                    # Off peak period
                    else:
                        price_fcst.loc[price_fcst.index[i], 'ToU'] = off_peak_summer_rate
            # Winter months
            else:
                # Weekdays and weekends are the same
                # Check mid peak period(4pm - 9pm):
                if 16 <= price_fcst.index[i].hour < 21:
                    price_fcst.loc[price_fcst.index[i], 'ToU'] = mid_peak_winter_rate
                # Super off-peak period
                else:
                    price_fcst.loc[price_fcst.index[i], 'ToU'] = super_off_peak_winter_rate

    # Set random and EPEX prices ##################################
    if 'Random' in price_fcst.columns:
        price_fcst['Random'] = np.random.rand(len(price_fcst)) * 0.1 + 0.25

    if 'ToU_mi' in price_fcst.columns:
        price_fcst['ToU_mi'] = price_fcst['ToU'] + np.linspace(start=0.00001,
                                                               stop=0.00002,
                                                               num=len(price_fcst))
    if 'Con_mi' in price_fcst.columns:
        price_fcst['Con_mi'] = price_fcst['Constant'] + np.linspace(start=0.00001,
                                                                    stop=0.00002,
                                                                    num=len(price_fcst))

    if 'RTP' in price_fcst.columns:
        # Read RTP data
        rtp_files = os.listdir(rtp_input_data_path)
        # If time is 2012 then use data from 2017, because data from 2012 is insufficient
        if t_start.year == 2012 and t_end.year == 2012:
            rtp_price_forecast = pd.read_hdf(
                rtp_input_data_path + [i for i in rtp_files if 'rtp_15min_2017' in i][0], key='df')
            # Insert rtp prices into simulated price forecast
            price_fcst['RTP'] = rtp_price_forecast['price'].loc[
                                t_start+pd.Timedelta('1826d'):t_end+pd.Timedelta('1826d')].values
        elif t_start.year == 2012 and t_end.year == 2013:
            rtp_price_forecast_2012 = pd.read_hdf(
                rtp_input_data_path + [i for i in rtp_files if 'rtp_15min_2017' in i][0], key='df')
            rtp_price_forecast_2013 = pd.read_hdf(
                rtp_input_data_path + [i for i in rtp_files if 'rtp_15min_2013' in i][0], key='df')
            # Insert rtp prices into simulated price forecast
            price_fcst['RTP'] = np.concatenate((rtp_price_forecast_2012['price'].loc[
                                                t_start+pd.Timedelta('1826d'):].values,
                                                rtp_price_forecast_2013['price'].loc[:t_end].values))
        else:
            rtp_price_forecast = pd.read_hdf(rtp_input_data_path + [
                i for i in rtp_files if 'rtp_15min_' + str(t_start.year) in i][0], key='df')
            # rtp_price_forecast = pd.read_pickle(
            #     rtp_input_data_path + [i for i in rtp_files if 'rtp_15min_' + str(t_start.year) in i][0], key='df')

            # Insert rtp prices into simulated price forecast
            price_fcst['RTP'] = rtp_price_forecast['price'].loc[t_start:t_end]

    return price_fcst


if __name__ == '__main__':
    test = simulate_elect_price_fcst(rtp_input_data_path='../analysis/input/RTP/',
                                     t_start=pd.Timestamp('2013-4-30 00:00'),
                                     t_end=pd.Timestamp('2013-5-30 23:00'),
                                     pr_constant=0.20, pricing={'ToU', 'Constant', 'Con_mi', 'ToU_mi', 'RTP'})

    test.plot()
    plt.show()






