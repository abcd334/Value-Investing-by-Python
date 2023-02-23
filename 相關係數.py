import pandas as pd
import os

def Corr(data,corr_limit):

    df_returns = pd.DataFrame()

    for symbol in data['Code']:
        filename = str(symbol) + '.csv'

        df_stock = pd.read_csv(os.path.join(data_folder, filename), index_col='Date', parse_dates=True)
        df_returns[symbol] = df_stock['Close']


    # 計算相關係數
    corr = df_returns.corr()

    groups = pd.DataFrame()
    
    for symbol in data['Code']:
        symbol_corr=corr.loc[symbol]
        for code in symbol_corr.index:
            if symbol_corr.loc[code] < corr_limit:
                groups=groups.append({'symbol': symbol, 'code': code}, ignore_index=True)

    with pd.ExcelWriter('output.xlsx', mode='w') as writer:
        groups.to_excel(writer, sheet_name='sheet1', index=False, startrow=0, startcol=0, header=True)

    return groups

if __name__ == '__main__':
    data = pd.read_excel('Product Code.xlsx')
    data_folder = 'History Data'
    result = Corr(data,0.5)
    print(result)