# DeltaTrader

DeltaTrader是一个开源的量化交易接口，可以获取任意A股数据，并实现自动化交易

## 安装

可以通过clone该项目，实现引用

## 简单入门实例

有了DeltaTrader，如果你想要获取股票数据，只需要这样：

```python
import data.stock as st

data = st.get_single_price(code='000001.XSHE',
                           time_freq='daily',
                           start_date='2021-01-01',
                           end_date='2021-02-01')
```

## 数据导出

将数据导出为.csv格式：

```python
import data.stock as st

data = st.get_single_price(code='000001.XSHE')

st.export_data(data=data, filename='000001.XSHE', type='price')
```

## 功能模块

- 行情数据
- 策略模型
- 自动化交易