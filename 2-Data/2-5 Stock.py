from jqdatasdk import *
import pandas as pd
auth('13141244283','Xayida661108*')

# 转换周期：日k转换为周k
print('转换周期：日k转换为周k')
df = get_price('000001.XSHE', count=10, end_date='2024-03-18', frequency='daily', panel=False)
df['weekday'] = df.index.weekday
print(df)

df_week = pd.DataFrame()
df_week['open'] = df['open'].resample('W').first()
df_week['close'] = df['close'].resample('W').last()
df_week['high'] = df['high'].resample('W').max()
df_week['low'] = df['low'].resample('W').min()
print(df_week)

# 转换周期：月k转换为年k
print('转换周期：月k转换为年k')

df_month = get_price('000001.XSHE', start_date='2024-01-01', end_date='2024-12-31', frequency='daily', panel=False)
print(df_month)

df_year = pd.DataFrame()
df_year['open'] = df_month['open'].resample('ME').first()
df_year['close'] = df_month['close'].resample('ME').last()
df_year['high'] = df_month['high'].resample('ME').max()
df_year['low'] = df_month['low'].resample('ME').min()
print(df_year)

# 汇总统计：统计月成交量，成交额(sum)
print('汇总统计：统计月成交量，成交额(sum)')
df_week['volume (sum)'] = df['volume'].resample('W').sum()
df_week['money (sum)'] = df['money'].resample('W').sum()
print(df_week)
