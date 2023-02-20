import yfinance as yf
import pandas as pd
import openpyxl

df = yf.Ticker("^TWII").history(period="max")
data = pd.ExcelWriter('TSEA.xlsx',engine='openpyxl',mode='a')
data.to_excel(writer, sheet_name='工作表1', index=False)

writer.save()
