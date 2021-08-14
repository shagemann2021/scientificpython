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

def simple(t="TCEHY", p1="2017-01-01", p2=datetime.today().strftime('%Y-%m-%d')):
    ticker = yf.Ticker(t) # getting the passed ticker via yfinance

    if (ticker.info['regularMarketPrice'] == None):
        raise NameError("You did not input a correct stock ticker! Try again.")

    df = ticker.history(start=p1, end=p2, interval='1d') # the dataframe including data from period1 to period2 (if no periods are passed, the beginning of 2017 until today will be used)
    df['Date'] = df.index # adding the 'Date' column, containing the dates of the index column for easier access
    current_price = ticker.info['regularMarketPrice'] # saving the current price of the ticker

    x_num = list(range(0, len(df))) # numerical list of every day in the periods
    x_time = df['Date'].tolist() # list of dates of every day in the periods (NOT USED YET!!!)
    y = df['Close'].tolist() # list of the historical prices of the ticker in the periods

    plt.figure(figsize=(10,5)) # defines the figure size
    plt.plot(x_num, y, color='salmon', linewidth=1.0, label=f'Data of {t}') # plot of the historical ticker data

    plt.legend(loc='upper left') # legend
    plt.tight_layout() # for better visualization
    plt.savefig('graph.png') # saves the graph
    plt.show()
    
def full_graph(t="TCEHY", p1="2021-01-01", p2=datetime.today().strftime('%Y-%m-%d')):
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
    df[['Close', 'BOLU', 'BOLD']].plot(ax=ax, color=['salmon', 'turquoise', 'cadetblue']).fill_between(df.index, df['BOLD'], df['BOLU'], facecolor='teal', alpha=0.3)

    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    
    plt.legend(loc='upper left') # legend
    plt.tight_layout() # for better visualization
    plt.savefig('graph.png') # saves the graph
    plt.show()

def regression(t='BTC-USD', p1="2017-01-01", p2=datetime.today().strftime('%Y-%m-%d')):
    ticker = yf.Ticker(t) # getting the passed ticker via yfinance
    df = ticker.history(start=p1, end=p2, interval='1d') # the dataframe including data from period1 to period2 (if no periods are passed, the beginning of 2017 until today will be used)
    df['Date'] = df.index # adding the 'Date' column, containing the dates of the index column for easier access
    current_price = ticker.info['regularMarketPrice'] # saving the current price of the ticker

    x = list(range(0, len(df))) # numerical list of every day in the periods
    x_date = df['Date'].tolist() # list of dates of every day in the periods (NOT USED YET!!!)
    y = df['Close'].tolist() # list of the historical prices of the ticker in the periods
    
    x_arr = np.array(x).reshape((-1,1)) # array of x values (reshape needed for correct format)
    y_arr = np.array(y) # array of y values
    model = LinearRegression() # performs the regression
    model.fit(x_arr, y_arr) # fits the model with our data
    correlation = model.coef_ # correlation coefficients
   
    plt.figure(figsize=(10,5)) # defines the figure size
    plt.plot(x,y, color='salmon', linewidth=1.0, label=f'Data of {t}') # plot of the historical ticker data
    plt.scatter(len(df), current_price, color='mediumblue', marker='o', label='Current price', zorder=2.5, s=25) # plot of the current ticker price
    
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


    plt.legend(loc='upper left') # legend
    plt.tight_layout() # for better visualization
    plt.savefig('graph.png') # saves the graph
    plt.show()
    
    
if __name__ == "__main__":
    regression()
    simple()
    full_graph()
    
def read():
    with open('test.txt') as f:
        lines = f.readlines()
        return lines[len(lines)-1]

global size
size = 0
global size2
size2 = Path("test.txt").stat().st_size

while(True):
    size = size2
    size2 = Path("test.txt").stat().st_size

    if size != size2:
        last_line = read()
        everything(t=last_line)