import pandas as pd
import data.stock as st
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def compose_signal(data):
    # 整合信号
    data['buy_signal'] = np.where((data['buy_signal'] == 1) & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1) & (data['sell_signal'].shift(1) == -1), 0, data['sell_signal'])
    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data

def calculate_profit_pct(data):
    # 计算单次收益率：开仓，平仓（开仓的全部股数）
    data.loc[data['signal'] != 0, 'profit_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    data = data[data['signal'] == -1]
    return data

def calculate_cum_profit(data):
    # 计算累计收益率
    data['cum_profit'] = pd.DataFrame((1+data['profit_pct'])).cumprod() -1
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

    # 整合信号
    data = compose_signal(data)

    # 计算单次收益率
    data = calculate_profit_pct(data)
    data = calculate_cum_profit(data)

    return data

if __name__ == '__main__':
    stock_list = [{'name': '贵州茅台', 'code': '600519.XSHG'},
        {'name': '平安银行', 'code': '000001.XSHE'},
        {'name': '万科A', 'code': '000002.XSHE'}]
    df_cum_profit = pd.DataFrame()
    for stock in stock_list:
        df = week_period_strategy(stock['code'], 'daily', None, '2025-3-20')
        print(stock['name'])
        print(df[['close', 'signal', 'profit_pct', 'cum_profit']].describe())
        df_cum_profit[stock['name']] = df['cum_profit']

    print(df_cum_profit.describe())
    df_cum_profit.plot()
    plt.show()
