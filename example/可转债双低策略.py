# 导入所需的python库
import tushare as ts
import pandas as pd
import threading
import time

# 设置Token参数
ts.set_token('454f05abe72ea76f5479f1ef3e7943a35d92c7028bfae1e841c8d10d')


# 获取当前可转债列表并按照双低因素排序
def get_convertible_bonds():
    pro = ts.pro_api()
    # 获取当前可转债的基本信息
    df_bond = pro.cb_basic(fields='ts_code, bond_short_name,maturity_dt', is_mature=0)
    # 获取当前可转债的行情
    df_quote = pro.cb_daily(ts_code='', start_date=time.strftime("%Y%m%d", time.localtime(time.time() - 24 * 60 * 60)),
                            end_date=time.strftime("%Y%m%d", time.localtime()))
    # 将两个dataframe按code关联起来
    df_merged = pd.merge(df_bond, df_quote, on='ts_code')
    # 计算价格和溢价率并加入到新列中
    df_merged['price'] = df_merged.apply(lambda row: (row.close + row.convpr) if row.convprice == 'B' else row.close,
                                         axis=1)
    df_merged['prem_ratio'] = df_merged.apply(lambda row: round(row.premium / row.price * 100, 2), axis=1)
    # 按照时间、价格和溢价率降序排列
    df_sorted = df_merged.sort_values(by=['trade_date', 'price', 'prem_ratio'], ascending=[False, True, True])
    return df_sorted


# 定时执行任务的函数
def timing_task():
    while True:
        now = time.localtime()
        # 每天九点执行任务
        if now.tm_hour == 9 and now.tm_min == 0 and now.tm_sec < 10:
            print("开始执行量化策略")
            df = get_convertible_bonds()
            # 对前一天数据进行复盘并输出交易信号
            # ......
        time.sleep(1)


# 启动定时执行任务的线程
t = threading.Thread(target=timing_task)
t.start()
