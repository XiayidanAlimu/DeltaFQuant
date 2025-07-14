import datetime
import os.path

from jqdatasdk import *
auth('13141244283','Xayida661108*')

import pandas as pd
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 1000)

# 全局变量

root = "/Users/xiayidan.alimu/DeltaTrader/data/"

def get_stock_list():
    '''
    获取所有A股股票列表
    :return:
    '''
    stock_list = list(get_all_securities(['stock']).index)
    return stock_list

def get_single_finance(code, statDate):
    df = get_fundamentals(query(indicator).filter(indicator.code == code), statDate=statDate)
    return df

def get_single_price(code, time_freq, start_date=None, end_date=None):
    '''
    获取单个股票行情数据
    :param code:
    :param time_freq:
    :param start_date:
    :param end_date:
    :return:
    '''
    if start_date is None:
        start_date = get_security_info(code).start_date
    if end_date is None:
        end_date = datetime.datetime.today()
    df = get_price(code, start_date=start_date, end_date=end_date, frequency=time_freq, panel=False)
    return df

# 导出股票相关数据
def export_data(df, filename, type):
    """

    :param df:
    :param filename:
    :param type: 股票数据类型，可以是price,finance
    :return:
    """
    file_root = root + type + '/' + filename + '.csv'
    df.index.names=['date']
    df.to_csv(file_root)

def transfer_price_freq(df, time_freq):
    '''
    将数据转换为指定周期：开盘价（周期第一天），收盘价（周期最后一天），最高价（周期内），最低价（周期内）
    :param df:
    :param time_freq:
    :return:
    '''
    df_transferred = pd.DataFrame()
    df_transferred['open'] = df['open'].resample(time_freq).first()
    df_transferred['close'] = df['close'].resample(time_freq).last()
    df_transferred['high'] = df['high'].resample(time_freq).max()
    df_transferred['low'] = df['low'].resample(time_freq).min()
    return df_transferred


# query(valuation) 市值数据
# query(indicator) 指标数据
# query(income) 盈利数据
def get_single_indicator(code, date, statDate):
    '''
    获取单个股票的财务指标
    :param code:
    :param date:
    :param statDate:
    :return:
    '''
    df = get_fundamentals(query(indicator).filter(indicator.code == code), date=date, statDate='2024')
    return df

def get_single_valuation(code, date, statDate):
    '''
    获取单个股票的估值指标
    :param code:
    :param data:
    :param statDate:
    :return:
    '''
    df = get_fundamentals(query(valuation).filter(valuation.code == code), date=datetime)
    return df

def get_csv_data(code, type):
    file_root = root + type + '/' + code + '.csv'
    pd.read_csv(file_root)

# 计算涨跌幅
def calculate_change_pct(data):
    '''
    涨跌幅 = （当期收盘价 - 前期收盘价） / 前期收盘价
    当天，当分钟，当秒钟，当月，当周，当年
    :param data:
    :return: dataframe 带有涨跌幅
    '''
    data['close_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    return data

def update_daily_price(stock_code, type):
    # 3.1 是否存在文件：不存在则重新获取；存在则跳转步骤-> 3.2
    file_root = root + type + '/' + stock_code + '.csv'
    if os.path.exists(file_root):
        # 如果存在对应文件，执行3.2
        startDate = pd.read_csv(file_root, usecols=['date']).iloc[-1]
        # 3.2 获取增量数据(code, start_date=对应股票csv中最新日期, end_date=今天)
        df = get_single_price(stock_code, 'daily', startDate, datetime.datetime.today())
        # 3.3 删除重复值
        df.index.names = ['date']
        df = df.drop_duplicates('date', 'last')
        # 3.4 追加到已有文件中
        df.to_csv(file_root, mode='a', header=False)
    else:
        # 重新获取该股票行情数据
        df = get_single_price(stock_code, 'daily')
        export_data(df, stock_code, type)

def init_db():
    # 初始化股票数据库
    stocks = get_stock_list()
    for code in stocks:
        update_daily_price(code, 'price')


