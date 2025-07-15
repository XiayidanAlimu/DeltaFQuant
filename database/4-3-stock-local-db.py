import data.stock as st

# 从本地读取数据
data = st.get_csv_price('000001.XSHE', '2024-06-25', '2024-06-28')
print(data)
exit()