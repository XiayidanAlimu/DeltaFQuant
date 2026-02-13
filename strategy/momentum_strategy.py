'''
    动量策略
'''
from pandas.core.array_algos.transforms import shift

import data.stock as st
import pandas as pd
import strategy.base as base
import matplotlib.pyplot as plt

def get_data(start_date, end_date, type, use_cols, index_symbol='000300.XSHG'):
    """
    获取股票收盘价数据，并拼接为一个dataFramce
    :param start_date: str
    :param end_date: str
    :param type: str
    :param use_cols: list
    :param index_symbol: str 指数代码
    :return: dataFrame 拼接后的数据表
    """
    # 获取股票列表代码，沪深300持有个股，创业板，上证
    stocks = st.get_index_list(index_symbol)
    data_concat = pd.DataFrame()
    # 获取股票数据
    for code in stocks:
        data = st.get_csv_price(code, start_date, end_date, type, use_cols)
        data.columns = [code]
        data_concat = pd.concat([data_concat, data], axis=1)
    return data_concat

def momentum(data_concat, shift_n=1, top_n=2):
    """

    :param data_concat: dataFrame
    :param shift_n: 业绩统计周期，单元：月
    :param top_n: int 获取极值的个数
    :return:
    """
    # 转换时间频率：日->月
    data_concat.index = pd.to_datetime(data_concat.index)
    data_month = data_concat.resample('ME').last()

    # 计算过去n (shift_n) 个月的收益率
    print(data_month)
    # 收益率 = 期末值/期初值 - 1
    shift_return = data_month / data_month.shift(shift_n) - 1
    print(shift_return.head())
    # print(shift_return.shift(-1))

    # 生成交易信号：
    # 收益率排前n 》 赢家组合 》 买入信号：1
    # 收益率排后n 》 输家组合 》 卖出信号：-1
    buy_signals = get_top_stocks(shift_return, top_n)
    sell_signals = get_top_stocks(-1*shift_return, top_n)
    signals = buy_signals - sell_signals
    print(signals.head())

    # 计算投资组合收益率
    returns = base.calculate_porfolio_return(shift_return, signals, top_n * 2)
    print('==================计算(等权重)投资组合收益率====================')
    print(returns.head())

    # 评估策略效果：总收益率、年化收益率、最大回撤、夏普比
    returns = base.evaluate_strategy(returns)

    # 数据预览
    # print(data_month.head())
    return returns


def get_top_stocks(data, top_n):
    """
    找到前n位的极值，并转换为信号返回
    :param data:
    :param top_n: int 获取极值的个数
    :return: signals:df, 返回0,1,-1信号数据表
    """
    signals = pd.DataFrame(index=data.index, columns=data.columns)
    # 对data的每一行进行遍历，找到里面的最大值，并利用bool函数标注0或者1或者-1信号
    for index, row in data.iterrows():
        largest = row.nlargest(top_n)
        signals.loc[index] = row.isin(largest).astype(int)
    return signals



if __name__ == '__main__':
    data = get_data('2024-06-10', '2025-04-01', 'price', ['date', 'close'])
    returns = momentum(data)
    # returns.to_csv('')
    # 可视化每个月的收益率
    returns['cum_profit'].plot()
    plt.show()