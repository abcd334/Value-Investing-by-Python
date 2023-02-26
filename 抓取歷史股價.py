import yfinance as yf
import os
import pandas as pd

data=pd.read_excel('Product Code.xlsx')

for symbol in data['Code']:
    filename = str(symbol) + '.csv'
    df = yf.Ticker(str(symbol)).history(period="max")
    data_folder = 'History Data'
    df.index = pd.to_datetime(df.index.strftime('%Y-%m-%d'))

    if os.path.exists(os.path.join(data_folder, filename)):
        os.remove(os.path.join(data_folder, filename))

    with open(os.path.join(data_folder, filename), mode='a',newline='') as file:
        df.to_csv(file, index=True, header=not file.tell())
