# 3-4 模拟股票交易，买入，卖出信号

# 创建交易策略，生成交易信号
import data.stock as st
import numpy as np
import strategy.base as base

def week_period_strategy(code, time_freq, start_date, end_date):
    data = st.get_single_price(code, time_freq, start_date, end_date)
    print(data)
    # 新建周期字段
    data['weekday'] = data.index.weekday

    # 周四买入
    data['buy_signal'] = np.where((data['weekday'] == 3), 1, 0)
    # 周一卖出
    data['sell_signal']= np.where((data['weekday'] == 0), -1, 0)


    # 整合信号
    data = base.compose_signal(data)

    return data

if __name__ == '__main__':
    data = week_period_strategy('000001.XSHE', 'daily', '2024-3-20', '2024-5-20')
    print(data[['close', 'weekday', 'buy_signal', 'sell_signal', 'signal']])