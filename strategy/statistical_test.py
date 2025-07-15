
import data.stock as st
import strategy.ma_strategy as ma
import matplotlib.pyplot as plt
from scipy import stats

def ttest(data_return):
    """
    对策略收益进行t检验
    :param data_return: dataframe,单次收益率
    :return: float,t值和p值
    """
    # 调用假设检验 ttest 函数：scipy
    t, p = stats.ttest_1samp(data_return, 0, nan_policy='omit')

    # 判断是否与理论均值有显著性差异:α=0.05
    p_value = p / 2  # 获取单边p值

    # 打印
    print("t-value:", t)
    print("p-value:", p_value)
    print("是否可以拒绝[H0]收益均值=0：", p_value < 0.05)

    return t, p_value

if __name__ == '__main__':
    code = '000001.XSHE'
    df = st.get_single_price(code, 'daily', '2024-06-15', '2025-01-01')
    # 调用双均线策略
    df = ma.ma_strategy(df)

    # 策略的单次收益率
    returns = df['profit_pct']
    # print(returns)

    # 绘制一下分布图用于观察
    # plt.hist(returns, bins=30)
    # plt.show()

    # 对多个股票进行计算、测试
    ttest(returns)