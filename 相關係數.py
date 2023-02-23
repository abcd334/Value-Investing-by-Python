import pandas as pd
import os

def Corr(data,corr_limit):

    df_returns = pd.DataFrame()

    for symbol in data['Code']:
        filename = str(symbol) + '.csv'

        df_stock = pd.read_csv(os.path.join(data_folder, filename), index_col='Date', parse_dates=True)
        df_returns[symbol] = df_stock['Close']
        print(symbol)

    # 計算相關係數
    corr = df_returns.corr()
    groups = []

    while len(corr) > 0:
        code = corr.index[0]
        group = corr[code][corr[code] < corr_limit].index
        groups.append(group)
        corr.drop(index=group, columns=group, inplace=True)

    # 输出分组
    for i, group in enumerate(groups):
        return(f"Group {i+1}: {list(group)}")

if __name__ == '__main__':
    data = pd.read_excel('Product Code.xlsx')
    data_folder = 'History Data'
    result = Corr(data,0.1)
    print(result)