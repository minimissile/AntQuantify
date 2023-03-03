import helpers.calculate as calculate


def evaluate_strategy(data):
    """
    评估策略收益表现
    :param data: dataframe, 包含单次收益率数据
    :return results: dict, 评估指标数据
    """
    # 评估策略效果：总收益率、年化收益率、最大回撤、夏普比
    data = calculate.calculate_cum_prof(data)

    # 获取总收益率
    total_return = data['cum_profit'].iloc[-1]
    # 计算年化收益率（每月开仓）
    annual_return = data['profit_pct'].mean() * 12

    # 计算近一年最大回撤
    data = calculate.calculate_max_drawdown(data, window=12)
    # print(data)
    # 获取近一年最大回撤
    max_drawdown = data['max_dd'].iloc[-1]

    # 计算夏普比率
    sharpe, annual_sharpe = calculate.calculate_sharpe(data)

    # 放到dict中
    results = {'总收益率': total_return, '年化收益率': annual_return,
               '最大回撤': max_drawdown, '夏普比率': annual_sharpe}

    # 打印评估指标
    for key, value in results.items():
        print(key, value)

    return data
