import pandas as pd
import data.stock as st
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def calculate_sharpe(data):
    # sharpe = (回报率的均值 - 无风险利率)/回报率的标准差
    daily_return = data['close'].pct_change()
    avg_return = daily_return.mean()
    sd_return = daily_return.std()
    sharpe = avg_return / sd_return
    sharpe_year = sharpe * np.sqrt(252)
    return sharpe, sharpe_year

if __name__ == '__main__':
    df = st.get_single_price('000001.XSHE', 'daily', '2024-3-20', '2025-3-20')
    sharpe = calculate_sharpe(df)
    print(sharpe)
