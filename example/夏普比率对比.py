import helpers.stock as hs
import helpers.calculate as hc
import pandas as pd
import matplotlib.pyplot as plt

# 获取3只股票的数据
codes = ['689009.XSHG', '000055.XSHE', '000338.XSHE']

# 容器：存放夏普值
sharpes = []

for code in codes:
    data = hs.get_csv_price(code, '2022-10-01', '2022-12-01')

    # 计算每只股票的夏普比率
    daily_sharpe, annual_sharpe = hc.calculate_sharpe(data)
    sharpes.append([code, annual_sharpe])
    print(sharpes)

# 可视化3只股票并比较
sharpes = pd.DataFrame(sharpes, columns=['code', 'sharpe']).set_index('code')

# 绘制bar图
sharpes.plot.bar(title='Compare Annual Sharpe Ratio')
plt.xticks(rotation=30)
plt.show()
