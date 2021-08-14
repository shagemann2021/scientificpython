from pathlib import Path
import requests
from datetime import datetime
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import csv
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates


def detailed_graph(t="TCEHY", p1="2021-01-01", p2=datetime.today().strftime('%Y-%m-%d')):
    ticker = yf.Ticker(t) # getting the passed ticker via yfinance
    if (ticker.info['regularMarketPrice'] == None):
        raise NameError("You did not input a correct stock ticker! Try again.")

    df = ticker.history(start=p1, end=p2, interval='1d') # the dataframe including data from period1 to period2 (if no periods are passed, the beginning of 2017 until today will be used)
    df['Date'] = df.index # adding the 'Date' column, containing the dates of the index column for easier access
    current_price = ticker.info['regularMarketPrice'] # saving the current price of the ticker

    x_num = list(range(0, len(df))) # numerical list of every day in the periods
    x_time = df['Date'].tolist() # list of dates of every day in the periods
    y = df['Close'].tolist() # list of the historical prices of the ticker in the periods

    ohlc = df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
    ohlc['Date'] = pd.to_datetime(ohlc['Date'])
    ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
    ohlc = ohlc.astype(float)
    
    plt.style.use('dark_background')
    
    fig, ax = plt.subplots(figsize=(20,15))
    candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=1) #candlestick chart
    
    # Boillinger band calculations
    df['TP'] = (df['Close'] + df['Low'] + df['High'])/3
    df['std'] = df['TP'].rolling(20).std(ddof=0)
    df['MA-TP'] = df['TP'].rolling(20).mean()
    df['BOLU'] = df['MA-TP'] + 2*df['std']
    df['BOLD'] = df['MA-TP'] - 2*df['std']

    # Plotting it all together
    df[['Close', 'BOLU', 'BOLD']].plot(ax=ax, color=['azure', 'turquoise', 'cadetblue']).fill_between(df.index, df['BOLD'], df['BOLU'], facecolor='teal', alpha=0.3)

    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    
    plt.legend(loc='upper left') # legend
    plt.tight_layout() # for better visualization
    plt.savefig('graph.png') # saves the graph
    plt.show()
    