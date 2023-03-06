from jqdatasdk import *
import pandas as pd
import datetime
import config.jq as jq
import os

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

    # 保存所有股票基本数据
    get_all_stocks()

    # 保存所有股票数据
    stocks = get_all_stock_codes()

    for code in stocks:
        update_daily_price(code, 'stock')


def get_single_price(code, time_freq='daily', start_date=None, end_date=None):
    """
    获取单个股票行情数据
    :param code: 股票代码
    :param time_freq: 时间周期, 默认为一天
    :param start_date: 开始时间
    :param end_date: 结束时间
    :return:
    """

    # 获取上市时间
    listing_date = get_security_info(code).start_date

    # 如果start_date为None, 默认从上市日期获取
    if start_date is None:
        start_date = listing_date

    # 如果start_date为None, 默认结束日期为今天
    if end_date is None:
        end_date = datetime.datetime.today()

    # 如果开始日期小于上市日期，则开始日期为上市日期
    if pd.to_datetime(start_date) < pd.to_datetime(listing_date):
        start_date = listing_date

    # 获取行情数据
    df = get_price(
        code,
        start_date=start_date,
        end_date=end_date,
        frequency=time_freq,
        panel=False)
    # df.index.name = 'date'
    return df


def get_all_stock_codes():
    """
    获取所有A股的股票代码
    :return: stock_list 所有股票代码
    """
    stocks = list(get_all_securities(['stock']).index)
    return stocks


def get_all_stocks():
    """
    获取所有A股的股票基本信息
    :return: stock_info_list 所有股票代码
    """
    stocks = pd.DataFrame(get_all_securities())
    file_path = export_date(stocks, 'all_stocks', type='stock', index='code')
    print('所有股票基本信息已保存至: {}'.format(file_path))
    return stocks


def export_date(data, filename, type='stock', mode=None, index='date'):
    """
    导出股票数据, 以csv格式存储
    :param data: 导出的数据
    :param filename: 文件名
    :param type: 数据类型 [stock：股票  etf：etf  convertible_bond: 可转债]
    :param mode: 导出方式： a表示追加 None表示默认写入
    :param index: 导出方式： 定义索引
    :return:
    """

    file_root = root + type + '/' + filename + '.csv'
    # 解决索引未命名的问题
    data.index.name = index

    # 如果是追加数据
    if mode == 'a':
        data.to_csv(file_root, mode=mode, header=False)
        # 删除重复值
        # data = pd.read_csv(file_root)
        # data = data.drop_duplicates(subset=['date'])  # 以日期列为准
        # data.to_csv(file_root)  # 重新写入
    else:
        data.to_csv(file_root)
    print('股票 {} 已成功存储至 {}'.format(filename, file_root))
    return file_root


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


def update_daily_price(stock_code, type='stock'):
    """
    更新股票数据至csv文件
    :param stock_code: 股票代码
    :param type: 要存储的类型： price
    :return:
    """
    # 判断某一个路径是否存在
    file_root = root + type + '/' + stock_code + '.csv'

    if os.path.exists(file_root):
        print('股票 {} 开始增量更新'.format(stock_code))

        # 本地数据最后一个日期
        local_end_date = pd.read_csv(file_root, usecols=['date'])['date'].iloc[-1]
        print('股票 {} 最后存储日期是{}'.format(stock_code, local_end_date))

        # 计算开始时间
        start_date = (pd.to_datetime(local_end_date) + datetime.timedelta(days=1)).date()
        print('开始从 {} 获取数据'.format(start_date))

        df = get_single_price(stock_code, 'daily', start_date, datetime.datetime.today())
        df.index.name = 'date'

        export_date(df, stock_code, type, 'a')
        print('股票 {} 更新成功'.format(stock_code))
    else:
        df = get_single_price(stock_code, 'daily', None, None)
        export_date(df, stock_code, type)
        print('新增股票 {} 的数据'.format(stock_code))


def get_csv_data(code, type='stock'):
    """
    返回存储在本地的csv文件
    :param code: 股票代码
    :param type: 文件类型, 默认为股票
    :return:
    """
    file_root = root + type + '/' + code + '.csv'
    return pd.read_csv(file_root)


def get_csv_price(code, start_date, end_date, type='stock', columns=None):
    """
    获取本地的股票价格
    :param start_date: 开始时间
    :param end_date: 结束时间
    :param code: 股票代码
    :param type: 文件类型
    :param columns: 提取的列，默认提取全部列
    :return:
    """
    # update_daily_price(code, type)
    file_root = root + type + '/' + code + '.csv'

    if columns is None:
        data = pd.read_csv(file_root, index_col="date")
    else:
        data = pd.read_csv(file_root, columns=columns, index_col="date")

    return data[(data.index >= start_date) & (data.index <= end_date)]


def transfer_price_freq(data, time_freq):
    """
    将收据转换为指定周期：
    开盘价-周期第一天，收盘价-周期最后一天，最高价-周期内最高价，最低价-周期内最低价
    :param data: 源数据
    :param time_freq: 要转换的时间周期
    :return: 转换时间范围后的数据
    """
    df = pd.DataFrame()
    df['open'] = data['open'].resample(time_freq).first()
    df['close'] = data['close'].resample(time_freq).last()
    df['high'] = data['high'].resample(time_freq).max()
    df['low'] = data['low'].resample(time_freq).min()
    return df


def get_single_finance(code, date, statDate):
    """
    获取单个股票估值指标
    :param code: 股票代码
    :param date:
    :param statDate:
    :return:
    """

    data = get_fundamentals(query(indicator).filter(indicator.code == code), date=date, statDate=statDate)
    return data


def get_stock_code(stock_name):
    """
    根据股票名，获取股票 code
    :param stock_name:
    :return:
    """

    file_root = root + 'stock/all_stocks.csv'
    # 先从本地获取股票基本数据
    if os.path.exists(file_root):
        securities = pd.read_csv(file_root)
    else:
        # 从线上获取数据并保存
        securities = jq.get_all_securities()
        get_all_stocks()

    stock_code = securities[securities['display_name'] == stock_name].iloc[0].at['code']
    return stock_code


if __name__ == '__main__':
    test_code = '689010.XSHG'
    test_start_time = '2023-02-20'
    test_display_name = '好想你'

    r_code = get_stock_code(test_display_name)
    print(r_code)

    # print(datetime(test_time))
    # print(datedays.datedays(test_time).gettomorrow())
    # datedays(test_time)
    # datedays.datedays()

    # today = datetime.date.today()
    # print('这一天一天是', today)
    # tomorrow = (pd.to_datetime(test_time) + datetime.timedelta(days=1)).date()
    # print('下一天是', tomorrow)

    # test_df = get_all_stocks()
    # print(test_df)
    # update_daily_price(test_code)

    # 查询当日剩余可调用数据条数   2857902405
    # query_count = get_query_count()
    # print('查询当日剩余可调用数据条数: {}'.format(query_count))

    # test_code = '689009.XSHG'
    # test_df = get_single_price(test_code, 'daily', start_date='2023-02-01', end_date='2023-02-20')
    # print(test_df)
    # export_date(test_df, test_code, mode='a')

    # test_stocks = get_index_stocks('000300.XSHG')
    # print(test_stocks)
