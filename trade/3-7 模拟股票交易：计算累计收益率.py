# 3-4 模拟股票交易，买入，卖出信号
import pandas as pd
from jqdatasdk import get_security_info

# 创建交易策略，生成交易信号
import data.stock as st
import numpy as np
import matplotlib.pyplot as plt

def compose_signal(data):
    '''
    整合信号
    :param data:
    :return:
    '''
    # 开始纠偏，取消重复连续的买入卖出信号
    data['buy_signal'] = np.where((data['buy_signal'] == 1) & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1) & (data['sell_signal'].shift(1) == -1), 0,
                                   data['sell_signal'])
    print('纠偏之后，买入卖出信号，如下所示：')
    print(data[['close', 'weekday', 'buy_signal', 'sell_signal']])
    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data

def calculate_profit_pct(data):
    # 计算单次收益率：开仓，平仓（开仓的全部股数）
    data = data[data['signal'] != 0]
    data['profit_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    data = data[data['signal'] == -1]
    return data

def calculate_cum_profit(data):
    '''
    计算累计收益率
    :param data: dataframe
    :return:
    '''
    data['cum_profit'] = pd.DataFrame((1+data['profit_pct'])).cumprod() -1
    return data

def week_period_strategy(code, time_freq, start_date, end_date):
    '''
    :param code: 股票代码
    :param time_freq:
    :param start_date:
    :param end_date:
    :return:
    '''

    # 获取行情数据
    data = st.get_single_price(code, time_freq, start_date, end_date)
    # 新建周期字段
    data['weekday'] = data.index.weekday
    # 周四买入
    data['buy_signal'] = np.where((data['weekday'] == 3), 1, 0)
    # 周一卖出
    data['sell_signal']= np.where((data['weekday'] == 0), -1, 0)

    # 模拟错误的重复买入
    # 周四，周五连续买入
    data['buy_signal'] = np.where((data['weekday'] == 3) | (data['weekday'] == 4), 1, 0)
    # 周一，周二连续卖出
    data['sell_signal']= np.where((data['weekday'] == 0) | (data['weekday'] == 1), -1, 0)

    # 整合信号
    data = compose_signal(data)
    # 计算单次收益率
    data = calculate_profit_pct(data)
    data = calculate_cum_profit(data)

    return data

if __name__ == '__main__':
    df = week_period_strategy('000001.XSHE', 'daily', None, '2025-3-20')
    print(df[['close', 'weekday', 'signal', 'profit_pct', 'cum_profit']])
    print(df.describe())
    df['cum_profit'].plot()
    plt.show()