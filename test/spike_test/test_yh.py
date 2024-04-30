import yfinance as yf

name = "005930.KS"
ticker = yf.Ticker(name)
df = ticker.history(interval="1m", period="2mo", auto_adjust=False)
print(df)
