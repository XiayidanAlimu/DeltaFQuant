import data.stock as st
import matplotlib.pyplot as plt
import strategy.base as base

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


if __name__ == '__main__':
    df = st.get_single_price('000001.XSHE', 'daily', '2024-3-20', '2025-3-20')
    df = base.calculate_max_drawdown(df)
    print(df[['daily-dd', 'max-dd']])
    df[['daily-dd', 'max-dd']].plot()
    plt.show()
