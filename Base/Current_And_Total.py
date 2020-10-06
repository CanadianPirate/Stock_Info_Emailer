from yahoo_fin import stock_info as si

shares = {"ENB.TO": 100, "BCE.TO": 25}

def read_tickers():
    file = open("Tickers.txt", "r").readlines()
    line_number = len(file)
    ticker_list = []
    for i in range(line_number):
        line = file[i]
        ticker_list.append(str.strip(line))

    return ticker_list

def get_prices(ticker_dict):
    current_prices = []
    for i in ticker_dict:
        current_prices.append(round(si.get_live_price(i), 2))

    return current_prices

def get_total_value(current_prices, shares):
    share_amounts = list(shares.values())
    totals = []
    total = 0
    for i in range(len(share_amounts)):
        totals.append(share_amounts[i] * current_prices[i])

    for i in totals:
        total += i
    return total

tickers = read_tickers()
prices = get_prices(tickers)
total_prices = get_total_value(prices, shares)
print(total_prices)
