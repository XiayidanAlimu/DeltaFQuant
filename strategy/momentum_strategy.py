'''
    动量策略
'''
from pandas.core.array_algos.transforms import shift

import data.stock as st
import pandas as pd

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
    for code in stocks[0:9]:
        data = st.get_csv_price(code, start_date, end_date, type, use_cols)
        data.columns = [code]
        data_concat = pd.concat([data_concat, data], axis=1)
    return data_concat

def momentum(data_concat, shift_n=1):
    """

    :param data_concat: dataFrame
    :param shift_n: 业绩统计周期，单元：月
    :return:
    """
    data_concat.index = pd.to_datetime(data_concat.index)
    data_month = data_concat.resample('ME').last()
    # 计算过去n (shift_n) 个月的收益率
    print(data_month)
    shift_return = data_month / data_month.shift(shift_n) - 1
    print(shift_return)

if __name__ == '__main__':
    data = get_data('2024-06-10', '2025-04-01', 'price', ['date', 'close'])
    momentum(data, shift_n=2)
