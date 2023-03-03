"""
数据过滤处理
"""


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
