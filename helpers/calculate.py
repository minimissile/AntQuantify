"""
各种值的计算
"""


def calculate_max_drawdown(data):
    """
    计算最大回测比
    :param data:
    :return:
    """
    # 1. 选取时间周期(时间窗口： 过去多少根交易K线)
    window = 252
    # 2. 选取时间周期内的最大值
    data['rolling_max'] = data['close'].rolling(window=window, min_periods=1).max()  # min_periods: 最少要的观测值
    # 3. 计算当天的回测比 = (谷值 - 峰值) / 峰值 = 谷值/峰值 - 1
    data['daily_dd'] = data['close'] / data['rolling_max'] - 1
    # 4. 选取时间周期内的最大回测比，即最大回测
    data['max_dd'] = data['daily_dd'].rolling(window=window, min_periods=1).min()
    return data
