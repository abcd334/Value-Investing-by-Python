import pandas as pd
import os

def Corr(data_folder,data,corr_limit):

    df_returns = pd.DataFrame()

    for symbol in data:
        #print(str(symbol))
        filename = str(symbol) + '.csv'
        df_stock = pd.read_csv(os.path.join(data_folder, filename), index_col='Date', parse_dates=True)
        df_returns[symbol] = df_stock['Close']

    # 計算相關係數
    corr = df_returns.corr()
    #print(corr)
    groups = pd.DataFrame()
    #check=0
    for symbol in data:
        symbol_corr = corr.loc[symbol]
        check = 0
        for code in symbol_corr.index:
            if check == 1:
                if symbol_corr.loc[code] < corr_limit:
                    groups = groups.append({'symbol': symbol, 'code': code}, ignore_index=True)
            if symbol==code:
                check = 1

        '''
        symbol_corr=corr.loc[symbol]

        for code in symbol_corr.index:
            if symbol_corr.loc[code] < corr_limit:
                groups=groups.append({'symbol': symbol, 'code': code}, ignore_index=True)
        '''
    with pd.ExcelWriter('output.xlsx', mode='w') as writer:
        groups.to_excel(writer, sheet_name='sheet1', index=True, startrow=0, startcol=0, header=True)

    return groups

if __name__ == '__main__':
    STK_code = pd.read_excel('Product Code.xlsx')
    #Fund_code = pd.read_excel('Fund Code.xlsx')
    data = pd.concat([STK_code['Code']], ignore_index=True)
    #data= pd.read_excel('Product Code.xlsx')
    data_folder = 'History Data'
    result = Corr(data_folder,data,0.5)
    #print(result)