from jqdatasdk import *
import pandas as pd
import datetime
import config.jq as jq

# 打印信息时不省略打印信息
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)

# 文件存储路径
root = '../data/'

# 登录聚宽账号
account, password = jq.jq_account()
auth(account, password)


def init_db():
    """
    初始化本地数据库
    :return:
    """
    stocks = get_stock_codes()
    for code in stocks:
        df = get_single_price(code, 'daily')
        export_date(df)


def get_single_price(code, time_freq, start_date=None, end_date=None):
    """
    获取单个股票行情数据
    :param code: 股票代码
    :param time_freq: 时间周期
    :param start_date: 开始时间
    :param end_date: 结束时间
    :return:
    """

    # 如果start_date为None, 默认从上市日期获取
    if start_date is None:
        start_date = get_security_info(code).start_date

    if end_date is None:
        end_date = datetime.datetime.today()

    # 获取行情数据
    df = get_price(
        code,
        start_date=start_date,
        end_date=end_date,
        frequency=time_freq,
        panel=False)
    # df.index.name = 'date'
    return df


def get_stock_codes():
    """
    获取所有A股的股票代码
    :return: stock_list 所有股票代码
    """
    stocks = list(get_all_securities(['stock']).index)
    return stocks


def export_date(data, filename, type, mode=None):
    """
    导出股票数据, 以csv格式存储
    :param data: 导出的数据
    :param filename: 文件名
    :param type: 数据类型 [stock：股票  etf：etf  convertible_bond: 可转债]
    :param mode: 导出方式： a表示追加 None表示默认写入
    :return:
    """
    file_root = root + type + '/' + filename + '.csv'
    # 解决索引未命名的问题
    data.index.name = 'date'

    if mode == 'a':
        data.to_csv(file_root, mode=mode, header=False)
        # 删除重复值
        data = pd.read_csv(file_root)
        data = data.drop_duplicates(subset=['date'])  # 以日期列为准
        data.to_csv(file_root)  # 重新写入
    else:
        data.to_csv(file_root)
    print('股票{}已成功存储至{}'.format(filename, file_root))


def filter_kcb_stock(stock_list):
    """
    过滤科创北交股票
    :param stock_list: 要过滤的股票列表
    :return: 过滤后的股票列表
    """
    for stock in stock_list[:]:
        if stock[0] == '4' or stock[0] == '8' or stock[:2] == '68':
            stock_list.remove(stock)
    return stock_list


def calculate_change_pct(data):
    """
    获取当前涨跌幅
    涨跌幅计算公式：(当天收盘价 - 前期收盘价) / 前期收盘价
    :param data: dataframe, 带有收盘价
    :return: dataframe, 带有涨跌幅
    """
    data['close_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    return data


# 获取单个股票财务指标
def get_single_valuation(code, date, statDate):
    """
    获取单个股票估值指标
    :param code:
    :param date:
    :param statDate:
    :return:
    """
    data = get_fundamentals(query(valuation).filter(valuation.code == code), date=date, statDate=statDate)
    return data


if __name__ == '__main__':
    test_df = get_stock_codes()
    print(test_df)