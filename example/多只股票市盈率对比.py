#
# import helpers.stock as hs
# from jqdatasdk import *
# import config.jq as jq
# import matplotlib.pyplot as plt
# import pandas as pd
#
# # 登录聚宽账号
# account, password = jq.jq_account()
# auth(account, password)
#
# stock_list = ['贵州茅台', '五粮液', '洋河股份', '泸州老窖', '古井贡酒']
#
# stocks_df = get_all_securities()
# stock_code_list = [stocks_df[stocks_df['display_name'] == stock].index.item() for stock in stock_list]
#
# print(stock_code_list)
#
# days = pd.date_range(start='2018-12-05', end='2019-12-05')
#
# multi_pe_ratio = {}
# for i in range(len(stock_list)):
#     stock_code = stock_code_list[i]
#     stock_name = stock_list[i]
#     q = query(valuation.day, valuation.code, valuation.pe_ratio).filter(valuation.code == stock_code)
#     pe_ratio = [get_fundamentals(q, date=day).loc[0, 'pe_ratio'] for day in days]
#     multi_pe_ratio[stock_name] = pe_ratio
#
# df = pd.DataFrame(multi_pe_ratio)
# df.index = days
# df.plot(figsize=(20, 10))
#
