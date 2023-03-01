import pandas as pd
from 長短均線 import moving_average_crossover
import os
import mplfinance as mpf
from 交易策略 import XAverage_Range

symbol = '^TWII'
data = pd.read_csv(os.path.join('History Data', symbol+'.csv'), index_col='Date')
data.index = pd.to_datetime(data.index)

'''
def XAverage(True_Range_line,days):
    var1=(2/(days+1))
    XAverage_line = pd.DataFrame()
    for True_Range in True_Range_line['True Range']:
        if True_Range==0:
            XAverage_line=XAverage_line.append({'XAverage':0}, ignore_index=True)
        else:
            XAverage_line=XAverage_line.append({'XAverage': XAverage_line[-1]+var1*(True_Range-XAverage_line[-1])}, ignore_index=True)

    return XAverage_line
'''




if __name__ == '__main__':
    days=10
    ave_days=120
    Fc_u=2
    Fc_d=2
    #True_Range_line = TrueRange(data,days)
    result=XAverage_Range(data,days,ave_days,Fc_u,Fc_d)
    #with pd.ExcelWriter('output.xlsx', mode='w') as writer:
    #    True_Range_line.to_excel(writer, sheet_name='sheet1', index=False, startrow=0, startcol=0, header=True)


    #print(True_Range_line,XAverage_line)



# 繪製K線圖
#mpf.plot(data, type='candle', mav=(50,100,120), volume=True, show_nontrading=True)

'''
result=pd.DataFrame()
for i in range(10,100,10):
    for j in range(20,300,10):
        data = pd.read_csv(os.path.join('History Data', symbol+'.csv'))
        # 執行策略
        backtest_data = moving_average_crossover(data,i,j)
        summary=backtest_data['strategy'].sum()
        result=result.append({'I':i,'J':j,'result':summary}, ignore_index=True)

print(result)


with pd.ExcelWriter('output.xlsx', mode='w') as writer:
    result.to_excel(writer, sheet_name='sheet1', index=False, startrow=0, startcol=0, header=True)
'''
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