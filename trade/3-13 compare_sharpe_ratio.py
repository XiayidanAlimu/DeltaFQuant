import pandas as pd
import data.stock as st
import  strategy.base as base
import matplotlib.pyplot as plt

codes = ['002594.XSHE', '300750.XSHE', '601012.XSHG']
sharpes = []
for code in codes:
    df = st.get_single_price(code, 'daily', '2024-3-20', '2025-3-20')
    print(df)
    daily_sharpe, annual_sharpe = base.calculate_sharpe(df)
    sharpes.append([code, annual_sharpe])

sharpes = pd.DataFrame(sharpes, columns=['code', 'sharpe']).set_index('code')
print(sharpes)
sharpes.plot.bar()
plt.show()
