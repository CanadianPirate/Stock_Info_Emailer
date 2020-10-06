file = open("Tickers.txt", "r").readlines()
line_number = len(file)
Tickers = []
for i in range(line_number):
    line = file[i]

    Tickers.append(str.strip(line))

