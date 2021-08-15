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
This script scrapes information from yahoo finance with the information received
from the scipy_webscraper and then creates plots which it saves in the folder in
which this program resides.
'''


def simple(t='BTC-USD', p1="2020-01-01", p2=datetime.today().strftime('%Y-%m-%d')):
    '''
    Creates a simple graph in which stock prices from the ticker "t" in the time
    period "p1" to "p2" are displayed.
    '''
    # Collecting the passed ticker via yfinance
    ticker = yf.Ticker(t)

    # Taking care of the case that an incorrect input is given
    if (ticker.info['regularMarketPrice'] == None):
        raise NameError("You did not input a correct stock ticker! Try again.")

    # The dataframe including data from period1 to period2 (if no periods are passed, the beginning of 2020 until today will be used)
    df = ticker.history(start=p1, end=p2, interval='1d') 
    # Adding the 'Date' column, containing the dates of the index column for easier access
    df['Date'] = df.index 
    # Saving the current price of the ticker
    current_price = ticker.info['regularMarketPrice'] 
 
    # List of dates of every day in the periods
    x_time = df['Date'].tolist() 
    # List of the historical prices of the ticker in the periods
    y = df['Close'].tolist() 
    
    # Sets background to dark style
    plt.style.use('dark_background')
    
    # Defines the figure size
    plt.figure(figsize=(10,5)) 
    # Plot of the historical ticker data
    plt.plot(x_time, y, color='salmon', linewidth=1.0, label=f'Data of {t}') 

    # Setting axis labels
    plt.xlabel('Date')
    plt.ylabel('Price')

    # Setting the title, legend. layout and saving the graph
    plt.title('Simple Graph of ' f'Data of {t}') 
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig('graph.png') 

def full_graph(t='BTC-USD', p1="2020-01-01", p2=datetime.today().strftime('%Y-%m-%d')):
    '''
    Creates a graph in which stock prices from the ticker "t" in the time period
    "p1" to "p2" are displayed. Also it has multiple layers of information
    showing trends using a Candlestick Chart, overlayed with Bollinger Bands.
    '''
    # Collecting the passed ticker via yfinance
    ticker = yf.Ticker(t) 

    # Error raised, in case of incorrect input
    if (ticker.info['regularMarketPrice'] == None):
        raise NameError("You did not input a correct stock ticker! Try again.")

    # The dataframe including data from period1 to period2 (if no periods are passed, the beginning of 2020 until today will be used)
    df = ticker.history(start=p1, end=p2, interval='1d') 
    # Adding the 'Date' column, containing the dates of the index column for easier access
    df['Date'] = df.index
    # Saving the current price of the ticker
    current_price = ticker.info['regularMarketPrice'] 
    # List of dates of every day in the periods
    x_time = df['Date'].tolist() 
    # List of the historical prices of the ticker in the periods
    y = df['Close'].tolist() 

    # Selecting for all the rows with these column labels
    ohlc = df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']] 
    # Converting the object into datetime and into matplotlib as a float - for the candlestick chart coming later
    ohlc['Date'] = pd.to_datetime(ohlc['Date'])  
    ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
    ohlc = ohlc.astype(float) 
    
    # Set background to dark style
    plt.style.use('dark_background') 

    # Candlestick plot
    fig, ax = plt.subplots(figsize=(15,10))
    candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=1)

    # Bollinger band calculations
    df['TP'] = (df['Close'] + df['Low'] + df['High'])/3
    df['std'] = df['TP'].rolling(20).std(ddof=0)
    df['MA-TP'] = df['TP'].rolling(20).mean()
    df['BOLU'] = df['MA-TP'] + 2*df['std']
    df['BOLD'] = df['MA-TP'] - 2*df['std']

    # Plotting bollinger bands
    df[['BOLU', 'BOLD']].plot(ax=ax, color=['turquoise', 'cadetblue']).fill_between(df.index, df['BOLD'], df['BOLU'], facecolor='teal', alpha=0.3)
    df['Close'].plot(ax=ax, color='salmon', label=f'Price at close of day of {t}')

    # Setting axis labels
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')

    # Setting title, legend, loyout and saving the graph
    plt.title('Detailed Graph showing Price Movements with Candlestick Charts and Bollinger Bands') # title
    plt.legend(loc='upper left', title= 'BOLU=Upper Bollinger Band, BOLD=Lower Bollinger Band') # legend
    plt.tight_layout() # for better visualization
    plt.savefig('graph.png') # saves the graph

def regression(t='BTC-USD', p1="2020-01-01", p2=datetime.today().strftime('%Y-%m-%d')):
    '''
    Creates a simple graph in which stock prices from the ticker "t" in the time
    period "p1" to "p2" are displayed. Additionally a regression line is generated.
    '''
    # Collecting thepassed ticker via yfinance
    ticker = yf.Ticker(t) 
    # The dataframe including data from period1 to period2 (if no periods are passed, the beginning of 2020 until today will be used)
    df = ticker.history(start=p1, end=p2, interval='1d') 
    # Adding the 'Date' column, containing the dates of the index column for easier access
    df['Date'] = df.index 
    # Saving the current price of the ticker
    current_price = ticker.info['regularMarketPrice'] 
    
    # List of dates of every day in the periods
    x_dates = df['Date'].tolist() 
    # Converting the object into datetime and into matplotlib dates for easier plotting
    x = pd.to_datetime(df['Date']).apply(mpl_dates.date2num)  
    # List of the historical prices of the ticker in the periods
    y = df['Close'].tolist() 
    
    # Array of x values (reshape needed for correct format)
    x_arr = np.array(x).reshape((-1,1))
    # Array of y values
    y_arr = np.array(y) 
    # Performs the regression
    model = LinearRegression() 
    # Fits the model with our data
    model.fit(x_arr, y_arr) 
    # Saves the correlation coefficients
    correlation = model.coef_ 
    
    # Set background to dark
    plt.style.use('dark_background') 

    # Defining the figure size
    plt.figure(figsize=(10,5))
    # Plot of the historical ticker data
    plt.plot(x_dates,y, color='salmon', linewidth=1.0, label=f'Data of {t}') 
    # Sets a marker of the current ticker price
    plt.scatter(x_dates[-1], current_price, color='mediumblue', marker='o', label='Current price', zorder=2.5, s=25) 

    # Array of x and y values
    x_plot = np.array(x)
    y_plot = np.array(y) 
    # Polyfit of the values (resulting in ascent and intercept)
    m,b = np.polyfit(x, y, 1)

    # Drawing the regression line in a color that depends on the coefficient we calculated above
    if correlation > 0: # positive correlation
        plt.plot(x_plot, m*x_plot + b, color='limegreen', label='Regression line')
    if correlation < 0: # negative correlation
        plt.plot(x_plot, m*x_plot + b, color='red', label='Regression line')
    if correlation == 0: # no correlation
        plt.plot(x_plot, m*x_plot + b, color='cadetblue', label='Regression line')

    # Setting axis labels
    plt.xlabel('Days since input date')
    plt.ylabel('Price')

    # Setting the title, lenegnd, layout and saving the graph
    plt.title('Regression Graph of ' f'Data of {t}')
    plt.legend(loc='upper left') 
    plt.tight_layout()
    plt.savefig('graph.png') 
