from pathlib import Path
import requests
from datetime import datetime
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import csv

def everything(t="TCEHY", p1="2017-01-01", p2=datetime.today().strftime('%Y-%m-%d')):
    print(t)
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
