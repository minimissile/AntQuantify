"""
各种值的计算
"""

import numpy as np
import pandas as pd


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


def calculate_change_pct(data):
    """
    计算每个日期单位当前涨跌幅
    涨跌幅计算公式：(当天收盘价 - 前期收盘价) / 前期收盘价
    :param data: dataframe, 带有收盘价
    :return: dataframe, 带有涨跌幅
    """
    data['close_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    return data


def calculate_sharpe(data):
    """
    计算夏普比率
    :param data: dataframe stock
    :return: float 年华的夏普比率
    """
    # 公式 sharpe = （回报率的均值 - 无风险利率） / 回报率的标准差
    # 依照公式计算每一个因子项
    # 回报率的均值 = 日涨跌幅.mean()
    # pct_change: 计算每日增长率
    daily_return = data['close'].pct_change()
    evg_return = daily_return.mean()
    # 回报率的标准差= 日涨跌幅.stddeviation()
    sd_return = daily_return.std()
    # 计算夏普比率
    sharpe = evg_return / sd_return
    sharpe_year = sharpe * np.sqrt(252)
    return sharpe, sharpe_year


def calculate_cum_pct(data):
    """
    计算累计收益率
    :param data:
    :return:
    """
    data['cum_profit'] = pd.DataFrame(1 + data['profit_pct']).cumprod() - 1
    return data


def calculate_prof_pct(data):
    """
    计算单次收益率
    :param data:
    :return:
    """
    # 过滤掉没有交易信号的日期
    # data = data[data['signal'] != 0]
    # 收益
    # data['profit_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    # pct_change 的计算结果等价于上面一行
    # data['profit_pct'] = data['close'].pct_change()

    # 筛选信号不为0的, 并且计算涨跌幅
    # loc使用说明： data.loc[赛选条件, 添加新列] = 新列赋值
    data.loc[data['signal'] != 0, 'profit_pct'] = data['close'].pct_change()
    data = data[data['signal'] == -1]
    return data


def calculate_prof_pct2(data):
    """
    计算单次收益率
    :param data:
    :return:
    """

    data.loc[data['signal'] != 0, 'profit_pct'] = data['close'].pct_change()
    # 过滤掉没有交易信号的日期
    # data = data[data['signal'] != 0]
    # 收益
    # data['profit_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    # pct_change 的计算结果等价于上面一行
    # data['profit_pct'] = data['close'].pct_change()

    # 筛选平仓后的数据
    data = data[data['signal'] == -1]
    return data


def calculate_max_drawdown(data, window=252):
    """
    计算最大回撤比
    :param data:
    :param window: int, 时间窗口设置，默认为252（日k）
    :return:
    """
    # 模拟持仓金额：投入的总金额 *（1+收益率）
    data['close'] = 10000 * (1 + data['cum_profit'])
    # 选取时间周期中的最大净值
    data['roll_max'] = data['close'].rolling(window=window, min_periods=1).max()
    # 计算当天的回撤比 = (谷值 — 峰值)/峰值 = 谷值/峰值 - 1
    data['daily_dd'] = data['close'] / data['roll_max'] - 1
    # 选取时间周期内最大的回撤比，即最大回撤
    data['max_dd'] = data['daily_dd'].rolling(window, min_periods=1).min()

    return data


def calculate_cum_pct(data):
    """
    计算累计收益率
    :param data:
    :return:
    """
    data['cum_profit'] = pd.DataFrame(1 + data['profit_pct']).cumprod() - 1
    return data


def calculate_cum_prof(data):
    """
    计算累计收益率（个股收益率）
    :param data: dataframe
    :return:
    """
    # 累计收益
    data['cum_profit'] = pd.DataFrame(1 + data['profit_pct']).cumprod() - 1
    return data
