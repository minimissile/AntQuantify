import numpy as np


def compose_signal(data):
    """
    整合交易信号
    :param data: dataframe
    :return:
    """
    data['buy_signal'] = np.where((data['buy_signal'] == 1) & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where(
        (data['sell_signal'] == -1) & (data['sell_signal'].shift(1) == -1), 0, data['sell_signal'])
    # 合并交易信号
    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data
