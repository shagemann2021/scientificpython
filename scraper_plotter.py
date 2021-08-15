from pathlib import Path
import requests
from datetime import datetime
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import csv


'''
This skript scrapes information from yahoo finance with the information received
from the scipy_webscraper and then creates plots which it saves in the folder in
which this program resides.
'''


def simple(t='BTC-USD', p1="2020-01-01", p2=datetime.today().strftime('%Y-%m-%d')):
    '''
    Creates a simple graph in which stock prices from the ticker "t" in the time
    period "p1" to "p2" are displayed.
    '''
    ticker = yf.Ticker(t) # getting the passed ticker via yfinance

    if (ticker.info['regularMarketPrice'] == None):
        raise NameError("You did not input a correct stock ticker! Try again.")

    df = ticker.history(start=p1, end=p2, interval='1d') # the dataframe including data from period1 to period2 (if no periods are passed, the beginning of 2020 until today will be used)
    df['Date'] = df.index # adding the 'Date' column, containing the dates of the index column for easier access
    current_price = ticker.info['regularMarketPrice'] # saving the current price of the ticker

    x_num = list(range(0, len(df))) # numerical list of every day in the periods
    x_time = df['Date'].tolist() # list of dates of every day in the periods (NOT USED YET!!!)
    y = df['Close'].tolist() # list of the historical prices of the ticker in the periods

    plt.style.use('dark_background') # sets background to dark style

    plt.figure(figsize=(10,5)) # defines the figure size
    plt.plot(x_time, y, color='salmon', linewidth=1.0, label=f'Data of {t}') # plot of the historical ticker data

    # setting axis labels
    plt.xlabel('Date')
    plt.ylabel('Price')

    plt.title('Simple Graph of ' f'Data of {t}') # title
    plt.legend(loc='upper left') # legend
    plt.tight_layout() # for better visualization
    plt.savefig('graph.png') # saves the graph




def full_graph(t='BTC-USD', p1="2020-01-01", p2=datetime.today().strftime('%Y-%m-%d')):
    '''
    Creates a graph in which stock prices from the ticker "t" in the time period
    "p1" to "p2" are displayed. Also it has multiple layers of information
    showing trends using a Candlestick Chart, overlayed with Bollinger Bands.
    '''
    ticker = yf.Ticker(t) # getting the passed ticker via yfinance

    if (ticker.info['regularMarketPrice'] == None):
        raise NameError("You did not input a correct stock ticker! Try again.")

    df = ticker.history(start=p1, end=p2, interval='1d') # the dataframe including data from period1 to period2 (if no periods are passed, the beginning of 2020 until today will be used)
    df['Date'] = df.index # adding the 'Date' column, containing the dates of the index column for easier access
    current_price = ticker.info['regularMarketPrice'] # saving the current price of the ticker

    x_num = list(range(0, len(df))) # numerical list of every day in the periods
    x_time = df['Date'].tolist() # list of dates of every day in the periods
    y = df['Close'].tolist() # list of the historical prices of the ticker in the periods


    ohlc = df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']] # selecting all rows with these column labels
    ohlc['Date'] = pd.to_datetime(ohlc['Date']) # convert object into datetime.
    ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num) # converting it into matplotlib
    ohlc = ohlc.astype(float) # casting it as a float

    plt.style.use('dark_background') # background set to dark style

    #candlestick chart plotting
    fig, ax = plt.subplots(figsize=(15,10))
    candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=1) #candlestick chart

    # Bollinger band calculations
    df['TP'] = (df['Close'] + df['Low'] + df['High'])/3
    df['std'] = df['TP'].rolling(20).std(ddof=0)
    df['MA-TP'] = df['TP'].rolling(20).mean()
    df['BOLU'] = df['MA-TP'] + 2*df['std']
    df['BOLD'] = df['MA-TP'] - 2*df['std']

    # Plotting bollinger bands
    df[['BOLU', 'BOLD']].plot(ax=ax, color=['turquoise', 'cadetblue']).fill_between(df.index, df['BOLD'], df['BOLU'], facecolor='teal', alpha=0.3)
    df['Close'].plot(ax=ax, color='salmon', label=f'Price at close of day of {t}')

   # setting axis labels
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')

    plt.title('Detailed Graph showing Price Movements with Candlestick Charts and Bollinger Bands') # title
    #plt.suptitle('BOLU=Upper Bollinger Band, BOLD=Lower Bollinger Band') #subtitle
    plt.legend(loc='upper left', title= 'BOLU=Upper Bollinger Band, BOLD=Lower Bollinger Band') # legend
    plt.tight_layout() # for better visualization
    plt.savefig('graph.png') # saves the graph




def regression(t='BTC-USD', p1="2020-01-01", p2=datetime.today().strftime('%Y-%m-%d')):
    '''
    Creates a simple graph in which stock prices from the ticker "t" in the time
    period "p1" to "p2" are displayed. Additionally a regression line is generated.
    '''

    ticker = yf.Ticker(t) # getting the passed ticker via yfinance
    df = ticker.history(start=p1, end=p2, interval='1d') # the dataframe including data from period1 to period2 (if no periods are passed, the beginning of 2020 until today will be used)
    df['Date'] = df.index # adding the 'Date' column, containing the dates of the index column for easier access
    current_price = ticker.info['regularMarketPrice'] # saving the current price of the ticker

    x_dates = df['Date'].tolist() # list of dates of every day in the periods (NOT USED YET!!!)
    x = pd.to_datetime(df['Date']).apply(mpl_dates.date2num)  # convert object into datetime.
    y = df['Close'].tolist() # list of the historical prices of the ticker in the periods

    x_arr = np.array(x).reshape((-1,1)) # array of x values (reshape needed for correct format)
    y_arr = np.array(y) # array of y values
    model = LinearRegression() # performs the regression
    model.fit(x_arr, y_arr) # fits the model with our data
    correlation = model.coef_ # correlation coefficients

    plt.style.use('dark_background') # set background to dark

    plt.figure(figsize=(10,5)) # defines the figure size
    plt.plot(x_dates,y, color='salmon', linewidth=1.0, label=f'Data of {t}') # plot of the historical ticker data
    plt.scatter(x_dates[-1], current_price, color='mediumblue', marker='o', label='Current price', zorder=2.5, s=25) # plot of the current ticker price

    x_plot = np.array(x) # array of x values
    y_plot = np.array(y) # array of y values
    m,b = np.polyfit(x, y, 1) # polyfit of the values (resulting in ascent and intercept)

    # drawing the regression line in a color that depends on the coefficient we calculated above
    if correlation > 0: # positive correlation
        plt.plot(x_plot, m*x_plot + b, color='limegreen', label='Regression line')
    if correlation < 0: # negative correlation
        plt.plot(x_plot, m*x_plot + b, color='red', label='Regression line')
    if correlation == 0: # no correlation
        plt.plot(x_plot, m*x_plot + b, color='cadetblue', label='Regression line')

    # setting axis labels
    plt.xlabel('Days since input date')
    plt.ylabel('Price')

    plt.title('Regression Graph of ' f'Data of {t}') # title
    plt.legend(loc='upper left') # legend
    plt.tight_layout() # for better visualization
    plt.savefig('graph.png') # saves the graph
