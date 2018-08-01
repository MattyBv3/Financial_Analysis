# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 20:52:10 2018

@author: Pr1d3sP4ran01a
"""

import datetime as dt
# matplotlib for data visualization / to graph things
import matplotlib.pyplot as plt
from matplotlib import style
# pandas for data analysis / to manipulate data
import pandas as pd
# pandas_data... = newest io library atm
import pandas_datareader.data as web

# set style for pretty graphs - sexy charts = proft
style.use('ggplot')
#set date range of stock prices to grab
start = dt.datetime(2015, 1, 1)
end = dt.datetime.now()

# MB test
ticker = input("Type a stock ticker: ")
# MB test

# make dataframe from stock history data (dataframe = spreadsheet or database table held in RAM)
# web.DataReader... = uses pandas_datareader pkg, looks for ticker "TSLA", gets info from morningstar, etc.
# !!! 'morningstar' had replaced 'yahoo' but now giving 404 error 7/31/2018 (worked 7/27/2018)
# !!! awaiting stackoverflow answer
df = web.DataReader(ticker, 'morningstar', start, end)
df.reset_index(inplace=True)
df.set_index("Date", inplace=True)
df = df.drop("Symbol", axis=1)

# save DataFrame to .csv file
df.to_csv('stock_ticker_output.csv')
# read data from .csv file rather than Yahoo api
df = pd.read_csv('stock_ticker_output.csv', parse_dates=True, index_col=0)
# graph it with
df.plot()
plt.show()
# so far just shows volume, now to graph what we're interested in
# plots 2nd graph showing highs & lows after volume
df[['High','Low']].plot()
plt.show()
# can't get 'Adj Close' to work https://pythonprogramming.net/handling-stock-data-graphing-python-programming-for-finance/?completed=/getting-stock-prices-python-programming-for-finance/
# solution, use 'Close' instead of 'Adj Close'
df['Close'].plot()
plt.show()

print("""
      Start part 3
      """)

# moving average
# creates (or re-writes if already exists) column df['100ma']
# stating that df['100ma'] column = 'Close" column w/ rolling method applied, with window of 100, and 
# this window will be an average (mean)

# df['100ma'] = df['Close'].rolling(window=100).mean() will result in "NaN" or not a number
# in 100ma column | requires 100 prev datapoints
# fix = change min. periods
df['100ma'] = df['Close'].rolling(window=100, min_periods=0).mean()
print(df.head())

# create 2 subplots | both 6 rows x 1 column | 1st starts at 0,0 | spans 5 rows | span 1 column
# sharex = ax2 always aligns its x axis w/ ax1's & vice versa
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

# plot close & 100ma on 1st axis | plot volume on 2nd
ax1.plot(df.index, df['Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])

plt.show()


# .head() is Pandas DataFrames feature / will output the first n rows, if no n chosen, default = 5
print(df.head())

print("""
      Start part 4
      """)
# OHLC = open high low close
# making candlesticks a.k.a. OHLC chart | not built into Panda
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates

#create dataframe based on Close, resample to 10 day window (only shows every 10 days) in OHLC format
# volume = could also do .mean() or .sum()
df_ohlc = df['Close'].resample('10D').ohlc()
# df of 10 days of volume, sum total
df_volume = df['Volume'].resample('10D').sum()
print(df_ohlc.head())

# make dates just regular column rather than index
df_ohlc = df_ohlc.reset_index()
# convert dates
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
# set up figure
fig = plt.figure()
# create 2 subplots | both 6 rows x 1 column | 1st starts at 0,0 | spans 5 rows | span 1 column
# sharex = ax2 always aligns its x axis w/ ax1's & vice versa
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
# converts axis from faw mdate numbers to dates
ax1.xaxis_date()
# graph candesticks
candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
# then do volume
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values,0)
# fill_between will graph x, y, then what to fill to or between...0 in this case
plt.show()



