import requests
from datetime import datetime
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
#import telegram_bot as bot


# The scrape function scrapes all the information that we need to use for our plot, our regression and for the Telegram bot
def scrape(t='BTC-USD', p1="2017-01-01", p2=datetime.today().strftime('%Y-%m-%d')):
    ticker = yf.Ticker(t) # getting the passed ticker via yfinance

    if (ticker.info['regularMarketPrice'] == None):
        bot_placeholder_fun()
        raise NameError("You did not input a correct stock ticker! Try again.")



    df = ticker.history(start=p1, end=p2, interval='1d') # the dataframe including data from period1 to period2 (if no periods are passed, the beginning of 2017 until today will be used)
    df['Date'] = df.index # adding the 'Date' column, containing the dates of the index column for easier access
    current_price = ticker.info['regularMarketPrice'] # saving the current price of the ticker

    return [df, current_price, t] # returning a list that contains the dataframe, the current price of the ticker and the name of the ticker

# The values function creates lists that contain the x and y values for our calculations and the plot
def values(df):
    x_num = list(range(0, len(df))) # numerical list of every day in the periods
    x_time = df['Date'].tolist() # list of dates of every day in the periods (NOT USED YET!!!)
    y = df['Close'].tolist() # list of the historical prices of the ticker in the periods

    return [x_num, y] # returning a list of the x and y values

# The regression function performs linear regression and returns the desired correlation coefficient
def regression(x, y):
    x_arr = np.array(x).reshape((-1,1)) # array of x values (reshape needed for correct format)
    y_arr = np.array(y) # array of y values
    model = LinearRegression() # performs the regression
    model.fit(x_arr, y_arr) # fits the model with our data
    correlation = model.coef_ # correlation coefficients

    return correlation[0] # returning the desired correlation coefficient

# The regression_plot function returns values needed to plot the regression line
def regression_plot(x, y):
    x_plot = np.array(x) # array of x values
    y_plot = np.array(y) # array of y values
    m,b = np.polyfit(x, y, 1) # polyfit of the values (resulting in ascent and intercept)

    return [x_plot, y_plot, m, b] # returning a list of values needed to plot the regression line

# The plot function plots everything in a nice format
def plot(t, x, y, df, current_price, correlation, x_plot, y_plot, m, b):
    plt.figure(figsize=(10,5)) # defines the figure size
    plt.plot(x,y, color='salmon', linewidth=1.0, label=f'Data of {t}') # plot of the historical ticker data
    plt.scatter(len(df), current_price, color='mediumblue', marker='o', label='Current price', zorder=2.5, s=25) # plot of the current ticker price

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
    #plt.show()




# def starter(user_input):
#     # #function_from_bot sends list of strings
#     # for stock in user_input:
#     #     try:
#     #         print(stock)
#     #         list = scrape(stock)
#     #         #bot.decider(1)
#     #         main(list)
#     #
#     #     except:
#     #         #bot.decider(2)
#     #         print("Input has no data to scrape")
#
#     list = scrape(stock)
#     if (ticker.info['regularMarketPrice'] == None):
#         raise NameError("You did not input a correct stock ticker! Try again.")
#



# The main function puts together all data
def returner(user_input):

    list = scrape(user_input)
    data = list[0] # the dataframe
    current = list[1] # the current price
    name = list[2] # the name of the ticker

    xyvalues = values(data)
    x = xyvalues[0] # x values for regression
    y = xyvalues[1] # y values for regression
    correlation = regression(x,y) # correlation coefficient

    xyplotvalues = regression_plot(x,y)
    x_plot = xyplotvalues[0] # x values for regression line plot
    y_plot = xyplotvalues[1] # y values for regression line plot
    m = xyplotvalues[2] # ascent of regression line
    b = xyplotvalues[3] # intercept of regression line

    return([name, x, y, data, current, correlation, x_plot, y_plot, m, b]) # plot and save the data

if __name__ == "__main__":
    main()
