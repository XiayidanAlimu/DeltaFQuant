import pandas as pd
from xarray.core.utils import result_name

import data.stock as st
import numpy as np

def compose_signal(data):
    # 整合信号
    data['buy_signal'] = np.where((data['buy_signal'] == 1) & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1) & (data['sell_signal'].shift(1) == -1), 0, data['sell_signal'])
    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data

def calculate_prof_pct(data):
    """
    计算单次收益率：开仓、平仓（开仓的全部股数）
    :param data:
    :return:
    """
    # 筛选信号不为0的，并且计算涨跌幅
    data.loc[data['signal'] != 0, 'profit_pct'] = data['close'].pct_change()
    data = data[data['signal'] == -1]  # 筛选平仓后的数据：单次收益
    return data

def calculate_cum_prof(data):
    """
    计算累计收益率（个股收益率）
    :param data: dataframe
    :return:
    """
    # 累计收益
    data['cum_profit'] = pd.DataFrame(1 + data['profit_pct']).cumprod() - 1
    return data

def calculate_sharpe(data):
    # sharpe = (回报率的均值 - 无风险利率)/回报率的标准差
    # daily_return = data['close'].pct_change() # a. 演示部分
    daily_return = data['profit_pct'] # b. 策略应用后
    avg_return = daily_return.mean()
    sd_return = daily_return.std()
    sharpe = avg_return / sd_return
    sharpe_year = sharpe * np.sqrt(252)
    return sharpe, sharpe_year

def calculate_max_drawdown(data, window=252):
    """
    计算最大回撤比
    :param data:
    :param window: int 窗口值，默认为252（日k）
    :return:
    """
    # 模拟持仓金额：投入的总金额 *（1+收益率）
    data['close'] = 10000 * (1 + data['cum_profit'])
    # 选取时间周期中的最大净值
    data['roll_max'] = data['close'].rolling(window=window, min_periods=1).max()
    # 计算当天的回撤比 (谷值-峰值)/峰值 = 谷值/峰值 - 1
    data['daily_dd'] = data['close'] / data['roll_max'] - 1
    # 选取时间周期内最大回撤
    data['max_dd'] = data['daily_dd'].rolling(window, min_periods=1).min()

    return data

def calculate_porfolio_return(data, signal, n):
    """
    计算组合收益率 （等权重） = 收益率之和/股票个数
    :param data: dataframe
    :param signal: dataframe
    :param n: int
    :return returns: dataframe
    """
    returns = data.copy()
    # shift(-1) 因为当前月份的信号*下个月份的收益率，才是当前月份的收益情况
    returns['profit_pct'] = (signal * returns.shift(-1)).T.sum() / n
    returns = calculate_cum_prof(returns)
    # shift(1) 来匹配对应的交易月份
    return returns.shift(1)

def evaluate_strategy(data):
    """
    评估策略收益表现
    :param data: dataframe 包含单次收益率数据
    :return: results : dist 评估指标数据
    """
    # 评估策略效果：总收益率、年化收益率、最大回撤、夏普比
    data = calculate_cum_prof(data)

    # 获取总收益率
    total_return = data['cum_profit'].iloc[-1]

    # 计算年化收益率（每月开仓）
    annualized_return = data['profit_pct'].mean() * 12

    # 计算近一年最大回撤
    data = calculate_max_drawdown(data, window=12)

    # 获取近一年最大回撤
    max_drawdown = data['max_dd'].iloc[-1]

    # 计算夏普比率
    sharpe, annualized_sharpe = calculate_sharpe(data)

    # 放到dict中
    results = {
        '总收益率': total_return,
        '年化收益率': annualized_return,
        '最大回撤': max_drawdown,
        '夏普比率': sharpe
    }

    # 打印评估指标
    for key, value in results.items():
        print(key, value)

    return data

