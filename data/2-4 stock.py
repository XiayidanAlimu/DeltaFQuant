# 2-4 使用JQData获取行情数据

from jqdatasdk import *
import pandas as pd

auth('13141244283','Xayida661108*')

# 上海证券交易所	.XSHG	600519.XSHG	贵州茅台
# 深圳证券交易所	.XSHE	000001.XSHE	平安银行

# 如何获取股票行情数据
df = get_price('000001.XSHE', count=100, end_date='2024-03-18', frequency='daily')

# 打印data frame
print(df)

# 打印data frame的长度
print(len(df))

# 获取所有A股的行情数据
stocks = list(get_all_securities(['stock']).index)
print(stocks)

for stock_code in stocks[:5]:
    print('正在获取股票代码 code = ', stock_code, ' 的行情数据...')
    df = get_price(stock_code, count=10, end_date='2024-03-18', frequency='daily', panel=False)
    print(df)
    time.sleep(3)