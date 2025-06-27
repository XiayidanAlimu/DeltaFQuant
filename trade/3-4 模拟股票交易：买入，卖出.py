# 3-4 模拟股票交易，买入，卖出信号


import data.stock as st
import numpy as np

# 创建交易策略，生成交易信号
def week_period_strategy(code, time_freq, start_date, end_date):
    data = st.get_single_price(code, time_freq, start_date, end_date)
    print(data)
    # 新建周期字段
    data['weekday'] = data.index.weekday
    # 周四买入
    data['buy_signal'] = np.where((data['weekday'] == 3), 1, 0)
    # 周一卖出
    data['sell_signal']= np.where((data['weekday'] == 0), -1, 0)
    print('正确情况，没有重复连续的买入卖出信号，如下所示：')
    print(data[['close', 'weekday', 'buy_signal', 'sell_signal']])

    # 模拟错误的重复买入
    # 周四，周五连续买入
    data['buy_signal'] = np.where((data['weekday'] == 3) | (data['weekday'] == 4), 1, 0)
    # 周一，周二连续卖出
    data['sell_signal']= np.where((data['weekday'] == 0) | (data['weekday'] == 1), -1, 0)
    print('错误发生时，会出现重复的买入卖出信号，如下所示：')
    print(data[['close', 'weekday', 'buy_signal', 'sell_signal']])
    # 开始纠偏，取消重复连续的买入卖出信号
    data['buy_signal'] = np.where((data['buy_signal'] == 1) & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1) & (data['sell_signal'].shift(1) == -1), 0, data['sell_signal'])
    print('纠偏之后，买入卖出信号，如下所示：')
    print(data[['close', 'weekday', 'buy_signal', 'sell_signal']])
    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data

if __name__ == '__main__':
    data = week_period_strategy('000001.XSHE', 'daily', '2024-3-20', '2024-5-20')
    print(data[['close', 'weekday', 'buy_signal', 'sell_signal', 'signal']])