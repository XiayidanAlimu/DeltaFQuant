import pandas as pd
import data.stock as st
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

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

if __name__ == '__main__':
    df = st.get_single_price('000001.XSHE', 'daily', '2024-3-20', '2025-3-20')
    df = calculate_max_drawdown(df)
    print(df[['daily-dd', 'max-dd']])
    df[['daily-dd', 'max-dd']].plot()
    plt.show()
