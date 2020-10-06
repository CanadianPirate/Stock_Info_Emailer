# Base for grabbing stock data from yfinance

import time
import yfinance as yf
from datetime import date, timedelta
import calendar

today = date.today()
ticker = input("Please enter your ticker: ")
tickerData = yf.Ticker(ticker)

# In case of needing historical data
# tickerDf = tickerData.history(period='1d', start=yesterday, end=today)

price = tickerData.get_info()
print(price['previousClose'])
