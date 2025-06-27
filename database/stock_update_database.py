'''
用于调用股票行情数据的脚本
'''

import data.stock as st

code = '000001.XSHE'
data = st.get_single_price(code=code, time_freq='daily', start_date='2024-3-20', end_date='2025-3-15')
st.export_data(data, code, 'price')
data = st.get_csv_data(code, 'price')
print(data)

# 实时更新数据 ??? TBD

# 1. 获取所有股票代码
# 2. 存储到csv文件中
# 3. 每日更新数据
# 3.1 获取增量数据(code, start_date=对应股票csv中最新日期, end_date=今天)
# 3.2 追加到已有文件中（是否存在文件：创建新的csv或追加数据）