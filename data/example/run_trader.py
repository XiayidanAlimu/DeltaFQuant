'''
以双均线策略为例，进行模拟实盘交易
'''
import time

import pandas as pd
from sympy.physics.units import amount

import data.stock as st
import strategy.ma_strategy as ma
import easytrader

# 交易初始化
user = easytrader.user('ths')
user.connect()
user.enable_type_keys_for_editor()

start_date = '2016-01-01'
end_date='2021-05-21'

# 步骤一：确定股票池，大盘股，沪深300
stocks = st.get_index_list()
print(stocks)

# 步骤二：找到有交易信号的股票，为之后交易进行准备

for stock in stocks:
    data = st.get_csv_price(stock, start_date=start_date, end_date=end_date)
    print(stock)
    print(data.tail())

    # 跑策略：双均线
    data = ma.ma_strategy(data)
    print(data.tail())

    signal = data['signal'].iloc[-1]
    print(signal)

    # 交易参数设置
    code = stock.split('.')[0] # 删除交易所后缀，例如 000001.XSHE => 000001
    price = data['close'].iloc[-1] # 获取当期收盘价
    amount = 100

    # 获取持仓信息
    position = pd.DataFrame(user.position)
    stock_pos = position[position['证券代码'==code]]['股份可用'].iloc[0]
    print('当前持仓：', position)

    # 进行，买入，卖出操作
    if signal == 1: # 买入
        entrust = user.buy(code, price, amount)
        print('=======买入id:', entrust)
    elif signal == -1 and stock_pos is not None:
        entrust = user.sell(code, price, stock_pos)
        print('=======卖出id:', entrust)
    else:
        print('无交易')
    time.sleep(3)

# 步骤三：判断交易信号：买入&卖出


# 步骤四：容错处理，提示信息

# 步骤五：