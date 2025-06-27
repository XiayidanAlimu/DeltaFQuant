'''
用于调用股票行情数据的脚本
'''

import data.stock as st

code = '000001.XSHE'
data = st.get_single_price(code=code, time_freq='daily', start_date='2024-3-20', end_date='2025-3-15')
st.export_data(data, code, 'price')
# 从csv中获取数据
data = st.get_csv_data(code, 'price')
print(data)

# 实时更新数据 ??? TBD

