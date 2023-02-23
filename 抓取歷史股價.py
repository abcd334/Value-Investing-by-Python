import yfinance as yf
import os

ticker_code='^TWII'
df = yf.Ticker(ticker_code).history(period="max")

if os.path.exists(ticker_code+'.csv'):
    os.remove(ticker_code+'.csv')

with open(ticker_code+'.csv', mode='a',newline='') as file:
    df.to_csv(file, index=True, header=not file.tell())
