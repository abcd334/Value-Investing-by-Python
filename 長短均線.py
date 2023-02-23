import numpy as np

# 定义回测策略
def moving_average_crossover(data, short_window, long_window):
    # 计算短期均线和长期均线
    data['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    data['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

    # 判断买卖信号
    data['signal'] = np.where(data['short_mavg'] > data['long_mavg'], 1.0, 0.0)
    data['position'] = data['signal'].diff()

    pre_data_return = 0
    pre_position=0
    strategy = []
    for data_return, position in zip(data['Close'], data['position']):
        if position != 0 and pre_data_return == 0:
            strategy.append(0)
            pre_data_return = data_return
            pre_position=position
        elif position != 0:
            strategy.append((data_return - pre_data_return)*pre_position)
            pre_data_return = data_return
            pre_position = position
        else:
            strategy.append(np.nan)

    data['strategy'] = strategy

    data.dropna(inplace=True)

    return data