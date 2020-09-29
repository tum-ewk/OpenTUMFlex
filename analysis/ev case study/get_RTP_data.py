"""
The get_RTP_data module requests real time prices ComED, an energy supplier from Illinois and
resamples them to a 15 minute resolution.
"""

__author__ = "Michel Zadé"
__copyright__ = "2020 TUM-EWK"
__credits__ = []
__license__ = "GPL v3.0"
__version__ = "1.0"
__maintainer__ = "Michel Zadé"
__email__ = "michel.zade@tum.de"
__status__ = "Development"

import requests
import json
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Define start and end date
t_start = '201701010000'
t_end = '201801010000'
avg_price_california = 0.19
# gets all data from website
price_data = requests.get('https://hourlypricing.comed.com/api?type=5minutefeed&datestart=' + t_start +
                          '&dateend=' + t_end)
# parses data to dictionary
parsed = json.loads(price_data.content)

rtp_df = pd.DataFrame(parsed)
timesteps = list()

# convert millisUTC to timestamp
for i in range(len(rtp_df)):
    timesteps.append(datetime.datetime.fromtimestamp(int(rtp_df['millisUTC'][i])/1000) - pd.Timedelta('7 h'))

# Insert timesteps into
rtp_df.insert(column='timesteps', value=timesteps, loc=0)
# Since data is from 2013-2014 a date offset of one year and six hours is subtracted
# rtp_df['NEW_DATE'] = rtp_df['timesteps'].apply(lambda x: x - pd.DateOffset(years=6, hours=6))
rtp_df['price_str'] = rtp_df['price']
# divide by 100 to make them to dollar per kWh
rtp_df['price'] = rtp_df['price'].astype(float) / 100
# rtp_df.index = rtp_df['NEW_DATE']
rtp_df.index = rtp_df['timesteps']

# Resample data to 15 minutes
rtp_15min = rtp_df.resample('15min').mean()

# Set all NaN values to average
rtp_15min['price'][rtp_15min['price'].isna()] = rtp_15min['price'].mean()

# Add constant value for taxes, fees, delivery services etc. (constant price of California in 2019 - average rtp)
rtp_15min['price'] += avg_price_california - rtp_15min['price'].mean()

# Create test plot for analysis
fig1, axs = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True)
axs[0].plot(rtp_df['price'].index, rtp_df['price'])
axs[0].grid()
axs[1].plot(rtp_15min['price'].index, rtp_15min['price'])
axs[1].grid()

# Add daytime id in order to use groupby()
rtp_15min['Daytime_ID'] = rtp_15min.index.weekday_name.array + ', ' + rtp_15min.index.strftime('%H:%M').array

rtp_per_daytime = pd.DataFrame()
rtp_15min_temp = rtp_15min.groupby(by='Daytime_ID').mean()
rtp_per_daytime = rtp_per_daytime.append(rtp_15min_temp.iloc[96:192, :])
rtp_per_daytime = rtp_per_daytime.append(rtp_15min_temp.iloc[480:, :])
rtp_per_daytime = rtp_per_daytime.append(rtp_15min_temp.iloc[384:480, :])
rtp_per_daytime = rtp_per_daytime.append(rtp_15min_temp.iloc[0:96, :])
rtp_per_daytime = rtp_per_daytime.append(rtp_15min_temp.iloc[192:384, :])

# Plot average daytime price data
plt.figure()
rtp_per_daytime['price'].plot()
plt.grid()

# Save price df in hdf files
rtp_15min.to_hdf('C:/Users/ga47num/PycharmProjects/GER MP - OpenTUMFlex - EV/Input/RTP/rtp_15min_' +
                 t_start + '-' + t_end + '.h5', mode='w', key='df')
rtp_per_daytime.to_hdf('C:/Users/ga47num/PycharmProjects/GER MP - OpenTUMFlex - EV/Input/RTP/rtp_per_daytime_' +
                       t_start + '-' + t_end + '.h5', mode='w', key='df')
