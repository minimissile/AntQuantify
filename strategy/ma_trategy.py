"""
简单的均线策略
"""

import pandas as pd
import numpy as np
import helpers.stock as hs
import helpers.trade as ht
import helpers.calculate as hc


def ma_strategy(data, short_window=5, long_window=20):
    """
    双均线策略
    长短均线金叉买入， 死叉卖出
    :param data: dataframe 投资标的行情数据(必须包含收盘价)
    :param short_window: 短期移动平均线
    :param long_window: 长期移动平均线
    :return:
    """

    print('当前周期参数对：', short_window, long_window)

    # 1. 计算指标： ma短期，ma长期
    data = pd.DataFrame(data)
    data['short_ma'] = data['close'].rolling(window=short_window).mean()
    data['long_ma'] = data['close'].rolling(window=long_window).mean()

    # 2. 生成信号，金叉买入，死叉卖出
    data['buy_signal'] = np.where(data['short_ma'] > data['long_ma'], 1, 0)
    data['sell_signal'] = np.where(data['short_ma'] < data['long_ma'], -1, 0)

    # 3. 过滤交易信号
    data = ht.compose_signal(data)
    print(data)

    # 计算单次收益
    data = hc.calculate_prof_pct(data)

    # 计算累计收益
    data = hc.calculate_cum_pct(data)

    # 4. 删除多余的columns
    # axis: 0: 删除行 1：删除列
    data = data.drop(labels=['buy_signal', 'sell_signal'], axis=1)
    return data


if __name__ == '__main__':
    test_code = '000099.XSHE'
    test_df = hs.get_csv_data(test_code)
    test_df = ma_strategy(test_df)
    df = test_df[test_df['signal'] != 0]
    print(df)
