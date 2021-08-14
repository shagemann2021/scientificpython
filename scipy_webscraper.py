from pathlib import Path
import requests
from datetime import datetime
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import csv
import os
import os.path

print("Scanning text file...")

def everything(t="TCEHY", p1="2017-01-01", p2=datetime.today().strftime('%Y-%m-%d')):
    print(f'Ticker: {t}')
    ticker = yf.Ticker(t) # getting the passed ticker via yfinance

    if (ticker.info['regularMarketPrice'] == None):
        print("Baby this wont work")
        if os.path.exists("graph.png"):
            os.remove("graph.png")
        #raise NameError("You did not input a correct stock ticker! Try again.")

    else:
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
        #plt.show()



global size
size = 0
global size2
size2 = Path("tester.txt").stat().st_size

while(True):
    size = size2
    size2 = Path("tester.txt").stat().st_size

    if size != size2:
        lis = list(csv.reader(open('tester.txt')))

        if len(lis) == 1:
            last_line = lis[0]
            last_line = str(last_line[0])
            last_line_list = last_line.split()
        else:
            last_line = lis[len(lis)-1]
            last_line = str(last_line[0])
            last_line_list = last_line.split()

        if len(last_line_list) == 1:
            everything(t=last_line_list[0])
        if len(last_line_list) == 2:
            everything(t=last_line_list[0], p1=last_line_list[1])
        if len(last_line_list) == 3:
            everything(t=last_line_list[0], p1=last_line_list[1], p2=last_line_list[2])
