# 获取价格并且计算涨跌幅

import data.stock as st

# 获取平安银行的行情数据（日k）
data = st.get_single_price('000001.XSHE', 'daily', '2024-3-18', end_date='2024-04-18')
print(data)
# 计算涨跌幅
data = st.calculate_change_pct(data)
print(data) # 多了一列 close_pct
# 验证准确性

# 获取周k
data_week = st.transfer_price_freq(data, 'W')
print(data_week)
# 计算涨跌幅
data_week = st.calculate_change_pct(data_week)
print(data_week) # 多了一列 close_pct
# 验证准确性