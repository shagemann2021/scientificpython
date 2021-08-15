# scientificpython
As our final Scientific Python project, we decided to implement a stock exchange webscraper combined with a Telegram Bot to have access to this information straight to your phone real-time. We used the Yahoo! Finance market data downloader to continuously scrape the historical to current stock price from the web, visualise this information using three different plots - with varying levels of complexity depending as to how much information you want to know - and then have these graphs accessible to a Telegram bot chat. 

Please make sure to check you have installed all the packages listed in requirements.txt (e.g. with pip install -r requirements.txt) to ensure functioning code. 

The three graphs that are available to be used are: 
- simple: just a basic stock price graph
- regression: this has the addition of a regression line giving an indication of stock trends 
- full_graph: has mutiple layers of information showing trends using a Candlestick Chart, overlayed with Bollinger Bands. More information below as to how to interpret these graphs. 

In the Candlestick Chart, the green and red boxes are a classic method used by traders to determine possible price movement based on past patterns. Each candlestick represents four pieces of information for that day: open and close in the thick body; high and low in the longer “candle wicks” above and below the body. Trading is often dictated by emotion, which can be read in candlestick charts by visually representing the size of price moves with different colors. Traders use the candlesticks to make trading decisions based on regularly occurring patterns that help forecast the short-term direction of the price.


Bollinger Bands are a technical analysis tool defined by a set of trendlines plotted two standard deviations (positively and negatively) away from a simple moving average (SMA) of a security's price, but which can be adjusted to user preferences. Bollinger Bands were developed and copyrighted by famous technical trader John Bollinger, designed to discover opportunities that give investors a higher probability of properly identifying when an asset is oversold or overbought.Many traders believe the closer the prices move to the upper band, the more overbought the market, and the closer the prices move to the lower band, the more oversold the market. John Bollinger has a set of 22 rules to follow when using the bands as a trading system. [https://www.investopedia.com/articles/technical/102201.asp]

How to use the Telegram Bot:
- type your requests in the following order 'type_of_graph Ticker_symbol start_date end_date'
- example commands for the Telegram Bot could be: 
'full_graph'
'simple BTC-USD'
'regression TCEHY 01.01.2020'
'full_graph TSLA 01.01.2017 01.01.2019'

An option would be to give simply the name of any graph and the standard response would be bitcoin stocks 'BTC-USD' for the year 2020 to the current date.
