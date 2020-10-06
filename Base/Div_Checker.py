# This program is designed to get dividend yields from yfinance and check against a users preference of a good div yield.
# Made to be run once a day in background to make sure a user doesn't keep holding shares with bad yield.
# Windows task scheduler or cron will handle task scheduling.

import yfinance as yf
import tkinter.messagebox

# Tickers to check
tickers = ["ENB.TO", "PPL.TO", "EIF.TO"]

# Adding each tickers div Yield to the dict
div_yields = []
for i in tickers:
    ticker = i
    ticker_object = yf.Ticker(ticker)
    ticker_info = ticker_object.get_info()
    div_yields.append(ticker_info['dividendYield'])

# Checking each div yield
bad_yields = []
for i in div_yields:
    if i < 0.06: # Enter bad yield here
        bad_yields.append(i)
    else:
        pass


# Checking if there is any bad yields in the dict
message = ""
if bool(bad_yields):
    for i in range(0, len(bad_yields)):
        message += (tickers[i] + " has a bad yield.\n")
    tkinter.messagebox.showinfo("Yields", message)
else:
    pass
