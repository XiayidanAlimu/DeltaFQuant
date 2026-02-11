'''
 @desc： 4-11 双均线策略：寻找最优参数
'''
import pandas as pd
import numpy as np
from sympy import false

# 参数一：股票池

# 参数二：周期参数 [5,10,20,60,120,250] 一周，两周，一个月，一个季度，半年，一年

# 匹配，并计算不同的周期参数对：5-10,5-20,...120-250

#

import strategy.ma_strategy as ma
import data.stock as st

# stocks = ['000001.XSHE']
params = [5,10,20,60,120,250]
data = st.get_csv_price('000001.XSHE', '2016-01-01', '2021-01-01')

# 存放参数与收益
res = []

# short 表示短周期
# long表示长周期
for short in params:
    for long in params:
        if long > short:
            data_res = ma.ma_strategy(data=data, short_window=short,long_window=long)

            # 获取周期参数，及其对应的累计收益率
            # 确保有数据可访问
            if len(data_res['cum_profit']) > 0:
                cum_profit = data_res['cum_profit'].iloc[-1]
                res.append([short, long, cum_profit])
            else:
                res.append([short, long, np.nan])

# 将结果列表转换为df,并找到最优参数
res = pd.DataFrame(res, columns=['short_win', 'long_win', 'cum_profit'])
# 排序
res = res.sort_values(by='cum_profit', ascending=False) # 按收益倒叙排序

print(res)

