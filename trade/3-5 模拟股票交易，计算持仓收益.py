import data.stock as st
import numpy as np
import matplotlib.pyplot as plt

#整合信号
def compose_signal(data):
    data['buy_signal'] = np.where((data['buy_signal'] == 1) & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1) & (data['sell_signal'].shift(1) == -1), 0, data['sell_signal'])
    print('纠偏之后，买入卖出信号，如下所示：')
    print(data[['close', 'weekday', 'buy_signal', 'sell_signal']])
    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data

# 计算单次收益率：开仓，平仓（开仓的全部股数）
def calculate_profit_pct(data):
    data = data[data['signal'] != 0]
    data['profit_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    data = data[data['signal'] == -1]
    return data

def week_period_strategy(code, time_freq, start_date, end_date):

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

    return data

if __name__ == '__main__':
    df = week_period_strategy('000001.XSHE', 'daily', None, '2024-5-20')
    print(df[['close', 'weekday', 'signal', 'profit_pct']])
    print(df.describe())
    df['profit_pct'].plot()
    plt.show()