from jqdatasdk import *
import pandas as pd
auth('13141244283','Xayida661108*')

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

def get_single_price(code, time_freq, start_date, end_date):
    '''
    获取单个股票行情数据
    :param code:
    :param time_freq:
    :param start_date:
    :param end_date:
    :return:
    '''
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