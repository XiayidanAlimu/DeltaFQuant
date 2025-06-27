import pandas as pd
import data.stock as st
import numpy as np

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

def calculate_sharpe(data):
    # sharpe = (回报率的均值 - 无风险利率)/回报率的标准差
    daily_return = data['close'].pct_change()
    avg_return = daily_return.mean()
    sd_return = daily_return.std()
    sharpe = avg_return / sd_return
    sharpe_year = sharpe * np.sqrt(252)
    return sharpe, sharpe_year

def calculate_max_drawdown(data):
    # 选取时间周期(时间窗口)
    window = 252
    # 选取时间周期中的最大净值
    data['roll_max'] = data['close'].rolling(window=252, min_periods=1).max()
    # 计算当天的回撤比 (谷值-峰值)/峰值 = 谷值/峰值 - 1
    data['daily-dd'] = data['close']/data['roll_max'] - 1
    # 选取时间周期内最大回撤
    data['max-dd'] = data['daily-dd'].rolling(window, min_periods=1).min()
    return data

