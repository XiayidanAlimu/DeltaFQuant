import os

from jqdatasdk import *
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

auth(os.environ['USERNAME'], os.environ['PASSWORD'])

# 1. 使用 resample 函数计算平安银行（000001.XSHE）2025 年 1 月的月 K，并回答该月 K 的开盘价、收盘价、最高价、最低价分别是多少？

print('平安银行（000001.XSHE）2025 年 1 月的月 K')
df = get_price('000001.XSHE', start_date='2025-01-01', end_date='2025-01-31', frequency='daily', panel=False)
print(df)

print('平安银行（000001.XSHE） 1月 K 的开盘价、收盘价、最高价、最低价')
df_month = pd.DataFrame()
df_month['open'] = df['open'].resample('ME').first()
df_month['close'] = df['close'].resample('ME').last()
df_month['high'] = df['high'].resample('ME').max()
df_month['low'] = df['low'].resample('ME').min()
print(df_month)

# 2. 使用 resample 函数计算平安银行（000001.XSHE）2024-3-25至2025-3-25期间每个月的总交易量、交易额

print('平安银行（000001.XSHE）2024-3-25至2025-3-25期间每个月的总交易量、交易额')
df2 = get_price('000001.XSHE', start_date='2024-03-25', end_date='2025-03-25', frequency='daily', panel=False)
df2_month = pd.DataFrame()
df2_month['volume (sum)'] = df2['volume'].resample('ME').sum()
df2_month['money (sum)'] = df2['money'].resample('ME').sum()
print(df2_month)

