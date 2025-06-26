
from jqdatasdk import *
import pandas as pd
auth('13141244283','Xayida661108*')

pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 1000)

df = get_fundamentals(query(indicator), statDate='2024')

print('基于盈利指标筛选股票')
df = df[(df['eps'] > 0) & (df['operating_profit'] > 3620643858) & (df['roe'] > 8.5) & (df['inc_net_profit_year_on_year'] > 10)]
print(df)

# 获取股票估值指标
print('获取股票估值指标')
df_valuation = get_fundamentals(query(valuation), statDate='2024')
print(df_valuation.head())

# 用code作为匹配的标准
print('用code作为匹配的标准')
df['index'] = df['code']
df_valuation['index'] = df_valuation['code']
df['pe_ratio'] = df_valuation['pe_ratio']
print(df)

# 筛选pe_ratio>0的
print('筛选pe_ratio>0的')
df = df[df['pe_ratio'] > 0]
print(df)

