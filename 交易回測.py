import pandas as pd
from 長短均線 import moving_average_crossover

symbol = '^TWII'
data = pd.read_csv(symbol+'.csv')

'''
# 将数据转换为mplfinance库所需的格式
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
df.index.name = 'Date'

# 绘制K线图
mpf.plot(df, type='candle', mav=(5, 10, 20), volume=True, show_nontrading=True)
'''
result=pd.DataFrame()
for i in range(10,100,10):
    for j in range(20,300,10):
        data = pd.read_csv(symbol + '.csv')
        # 执行回测策略
        backtest_data = moving_average_crossover(data,i,j)
        summary=backtest_data['strategy'].sum()
        result=result.append({'I':i,'J':j,'result':summary}, ignore_index=True)

print(result)

# 打开一个已经存在的 Excel 文件
with pd.ExcelWriter('output.xlsx', mode='w') as writer:
    # 将 DataFrame 写入到名为 sheet1 的工作表中，并清除工作表中原有的内容
    result.to_excel(writer, sheet_name='sheet1', index=False, startrow=0, startcol=0, header=True)
    #backtest_data.to_excel(writer, sheet_name='sheet2', index=False, startrow=0, startcol=0, header=True)
'''
# 分析回测结果
total_returns = backtest_data['strategy'].cumsum()
annualized_returns = (np.exp(total_returns / len(backtest_data)) - 1) * 252
sharpe_ratio = annualized_returns / backtest_data['strategy'].std() * np.sqrt(252)
max_drawdown = (backtest_data['strategy'].cumsum().expanding().max() - backtest_data['strategy'].cumsum()).max()

print(f"Total returns: {total_returns}")
print(f"Annualized returns: {annualized_returns}")
print(f"Sharpe ratio: {sharpe_ratio}")
print(f"Max drawdown: {max_drawdown}")
'''