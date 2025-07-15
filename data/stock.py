from datetime import datetime, timedelta
import os.path

from jqdatasdk import *
auth('18997994905','Alimu620117')

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
        end_date = datetime.today()
    df = get_price(code, start_date=start_date, end_date=end_date, frequency=time_freq, panel=False)
    return df

def export_data(data, filename, type, mode=None):
    """
    导出股票相关数据
    :param data:
    :param filename:
    :param type: 股票数据类型，可以是：price、finance
    :param mode: a代表追加，none代表默认w写入
    :return:
    """
    file_root = root + type + '/' + filename + '.csv'
    data.index.names = ['date']
    if mode == 'a':
        data.to_csv(file_root, mode=mode, header=False)
        # 删除重复值
        data = pd.read_csv(file_root)  # 读取数据
        data = data.drop_duplicates(subset=['date'])  # 以日期列为准
        data.to_csv(file_root, index=False)  # 重新写入
    else:
        data.to_csv(file_root)  # 判断一下file是否存在 > 存在：追加 / 不存在：保持

    print('已成功存储至：', file_root)

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

def get_csv_price(code, start_date, end_date, type='price', columns=None):
    """
        获取本地数据，且顺便完成数据更新工作
        :param code: str,股票代码
        :param start_date: str,起始日期
        :param end_date: str,起始日期
        :param columns: list,选取的字段
        :return: dataframe
        """
    update_daily_price(code, type)
    # 讀取數據
    file_root = root + type + '/' + code + '.csv'
    if columns is None:
        data = pd.read_csv(file_root, index_col='date')
    else:
        data = pd.read_csv(file_root, usecols=columns, index_col='date')
    # 根据日期筛选股票数据
    return data[(data.index >= start_date) & (data.index <= end_date)]

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

def update_daily_price(stock_code, type='price'):
    # 3.1 是否存在文件：不存在则重新获取；存在则跳转步骤-> 3.2
    file_root = root + type + '/' + stock_code + '.csv'
    if os.path.exists(file_root):
        # 如果存在对应文件，执行3.2
        startDate = pd.read_csv(file_root, usecols=['date']).iloc[-1].item()
        # 3.2 获取增量数据(code, start_date=对应股票csv中最新日期, end_date=今天)
        today = datetime.strptime(startDate, "%Y-%m-%d").date()
        one_day = timedelta(days=1)
        next_day = today + one_day
        df = get_single_price(stock_code, 'daily', startDate, next_day.strftime("%Y-%m-%d"))
        # 3.4 追加到已有文件中
        export_data(df, stock_code, type, 'a')
    else:
        # 重新获取该股票行情数据
        df = get_single_price(stock_code, 'daily', '2024-6-10', '2025-4-10')
        export_data(df, stock_code, type)
    print('股票數據已經更新成功', stock_code, type)

def init_db():
    # 初始化股票数据库
    stocks = get_stock_list()
    for code in stocks:
        update_daily_price(code, 'price')


