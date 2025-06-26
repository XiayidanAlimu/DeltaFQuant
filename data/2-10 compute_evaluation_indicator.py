from jqdatasdk import *
auth('13141244283','Xayida661108*')

# 如何获取股票行情数据
df = get_price('600519.XSHG', count=1, end_date='2025-03-18', frequency='daily')
price = df['close'].iloc[0]
print('当天股票收盘价', price)

qv = query(valuation).filter(valuation.code == '600519.XSHG')
df_valuation = get_fundamentals(qv, date='2025-03-18')
capitalization = df_valuation['capitalization'].iloc[0]
print('发行总股数', capitalization)
print('当天市值 = 当天股票收盘价 × 发行总股数 = ', price * capitalization)

qv_indicator = query(indicator).filter(indicator.code == '600519.XSHG')
df_indicator = get_fundamentals(qv_indicator, date='2025-03-18')
eps = df_indicator['eps'].iloc[0]

# 每股股价 price
# 每股收益 eps indicator
result = price/eps
print('每股股价', price)
print('每股收益', eps)
print('#市盈率（静态） = 每股股价 / 每股收益（或者：市值 / 母公司净利润）= ', result)