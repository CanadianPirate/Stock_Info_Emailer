# This program was written by Chandler Dionne
import yfinance as yf
import smtplib
import ssl
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from yahoo_fin import stock_info as si

port = 465  # For SSl


bad_yield = 5  # Whole number from 0-100
senders_email = "youremail@gmail.com"  # Users email
user_pass = "password"
receivers_email = "receiver@example.com"  # Person To send to
off_port_earnings = 0 # Enter profits that arent reflected in your current holdings
holdings = {"ENB": 42.58, "BNS.TO": 55.15} # Add holdings and buy prices here
shares = {"ENB": 100, "BNS.TO": 100} # Add share amounts here


# Opens a text file and reads each ticker from it **was added for packaged version to be easily customizable**
def read_tickers():
    file = open("Tickers.txt", "r").readlines()
    line_number = len(file)
    ticker_list = []
    for i in range(line_number):
        line = file[i]
        ticker_list.append(str.strip(line))

    return ticker_list


# Gets current prices
def get_current_prices(ticker_dict):
    current_prices = []
    for i in ticker_dict:
        current_prices.append(round(si.get_live_price(i), 2))

    return current_prices

# Gets the total value of the current holdings
def get_total_value(current_prices, shares):
    share_amounts = list(shares.values())
    totals = []
    total = 0
    for i in range(len(share_amounts)):
        totals.append(share_amounts[i] * current_prices[i])

    for i in totals:
        total += i

    return round(total, 2)

# Gets dividend yield percentages as an integer
def get_div_yield(ticker_dict):
    div_yields = []
    for i in ticker_dict:
        ticker_object = yf.Ticker(i)
        ticker_info = ticker_object.get_info()
        div_yields.append(round(100 * ticker_info['dividendYield'], 2))
    return div_yields

# Gets the most recent ex dividend dates for the current holdings
def get_div_ex(ticker_dict):
    div_ex_list = []
    for i in ticker_dict:
        ticker_object = yf.Ticker(i)
        ticker_info = ticker_object.get_info()
        date = datetime.fromtimestamp(ticker_info['exDividendDate'])
        date = datetime.date(date)
        date = date.strftime('%b %d, %Y')
        div_ex_list.append(date)

    return div_ex_list

# Checks if the yields are under the users prefrence
def check_yield(yields_dict):
    for i in yields_dict:
        if i < bad_yield:
            return True
        else:
            pass

    return False

# Sends the email after its been packaged by mime
def email_user(sender, receiver, message, password):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())


if __name__ == "__main__":

    # Getting data
    tickers = read_tickers()
    yields = get_div_yield(tickers)
    current_prices = get_current_prices(holdings)
    total_current_value = get_total_value(current_prices, shares)
    div_ex = get_div_ex(tickers)

    # Checking yields
    if check_yield(yields):
        bad_check = "One or more of your stocks has a yield under 6%! Consider looking for better yields to replace it."
    else:
        bad_check = ""


    # Parsing text for email packing
    add_text = ""
    for i in range(len(tickers)):
        add_text += (tickers[i] + " has a yield of " + str(yields[i]) + "% today. The most recent EX Div date is " + str(div_ex[i]) + "<br>")

    add_text += "<br> Your total portfolio value is now $" + str(total_current_value)


    # Using mime to make future html additions easier
    email_message = MIMEMultipart('alternative')
    email_message['Subject'] = "Your Daily Stock Info!"
    email_message['From'] = senders_email
    email_message['To'] = receivers_email
    plain = "hi"
    html = """\
    <html>
      <body>
        <p style="color:red;font-size:16px">
        """ + bad_check + """
        </p>
        <p style="font-size:16px"><b>Here is your stock data from today.</b></p>
        <p style="font-size:12px">
           """+str(add_text)+"""
        </p>
      </body>
    </html>
    """

    # Making and attaching each part.
    part1 = MIMEText(plain, 'plain')
    part2 = MIMEText(html, 'html')
    email_message.attach(part1)
    email_message.attach(part2)

    # Sending final email
    email_user(senders_email, receivers_email, email_message, user_pass)
