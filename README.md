# scientificpython
As our final Scientific Python project, we decided to implement a stock exchange webscraper combined with a Telegram Bot to have access to this information straight to your phone real-time. We used the Yahoo! Finance market data downloader to continuously scrape the historical to current stock price from the web, visualise this information using three different plots - with varying levels of complexity depending as to how much information you want to know - and then have these graphs accessible to a Telegram bot chat.

Please make sure to check you have installed all the packages listed in requirements.txt (e.g. with pip install -r requirements.txt) to ensure functioning code.

How to use the Telegram Bot:
- type your requests in the following order 'type_of_graph Ticker_symbol start_date end_date'
- example commands for the Telegram Bot could be:
'simple BTC-USD'
'regression TCEHY 01.01.2020'
'full_graph TSLA 01.01.2017 01.01.2019'


