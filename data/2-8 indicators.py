from jqdatasdk import *
import pandas as pd
auth('13141244283','Xayida661108*')

pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 1000)

df = get_fundamentals(query(indicator), statDate='2024')
df.to_csv('/Users/xiayidan.alimu/DeltaFQuant/2-data/finance/2-8-indicators.csv')

# 基于盈利指标筛选股票
# eps
# operating_profit
# roe
# inc_net_profit_year_on_year

df = df[(df['eps'] > 0) & (df['operating_profit'] > 3620643858) & (df['roe'] > 8.5) & (df['inc_net_profit_year_on_year'] > 10)]
print(df)
print(len(df))

# operating profit 列求平均值 average = 3620643858
# roe 列求平均值 average = 8.450188923
