"""
可转债双低策略
"""

# 双低是指股票的市盈率和市净率都比较低。在可转债领域，双低也意味着债券价格与对应股票价差距较大，而债券溢价率和回售触发率都比较低。所以，该策略将会考虑股票的市盈率、市净率，以及可转债的债券价格和溢价率等因素。

# 下面是具体步骤:
# 1. 设置筛选条件
# 2. 定义选取标准, 可根据历史数据进行优化和改进
# 3. 获取数据
# 4. 利用聚宽平台提供的数据接口获取需要的数据。可以使用 pandas 对数据进行清洗和格式化处理。这些数据包括：可转债的基本信息（名称、代码、债券价格等）
# 5. 对应可转债的股票市盈率和市净率数据分析与处理
# 6. 对从接口中获取的数据进行分析和处理。根据选定的筛选条件，在所有满足条件的可转债中，挑选符合双低条件的可转债。最终选择的可转债的数据会通过预设的通知方式推送给用户。
# 7.自动化发送结果,利用 Python 的定时任务模块 APScheduler 或是 Linux 系统的 Crontab，定时执行策略并通过邮件或其他社交媒体方式将排序表格推送给用户。
#
# 最后，要区别于人工操作的模型，模型的质量默认取决于输入，所以完全依赖机器操作可能会有风险，请使用可靠性高且处于谷歌云或者类似的服务器上运行。

import jqdatasdk as jq
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import config.jq as app_account
import akshare as ak
import jqdata

account, password = app_account.jq_account()

jq.auth(account, password)


def get_cbonds():
    # 初始化聚宽账号密码
    # jq.auth(username='你的聚宽账号',
    #         password='你的聚宽密码')

    # 聚宽模块，查询可转债列表并过滤出符合双低条件
    cb_list = jq.get_all_convertibles()
    return cb_list
    # cb_df = cb_list[['code', 'bond_nm', 'price', 'convert_price', 'pb_ratio']].set_index('code')
    # return cb_df[(cb_df['convert_price'] > cb_df['price']) & (cb_df['pb_ratio'] < 1.2)]


# 获取可转债数据
def get_bonds():
    bonds = ak.stock_zh_a_convertible_list(indicator="BOND", fields="convert_price_at")
    return bonds


# 获取可转债数据
def get_convertible_bonds():
    # 使用akshare模块获取可转债数据
    cbonds_df = ak.stock_zh_a_cbonds()
    # 选取符合双低条件的数据，如价格低于100，剩余规模大于1亿等
    cbonds_df_filtered = cbonds_df[cbonds_df['现价'] < 100]
    cbonds_df_filtered = cbonds_df_filtered[cbonds_df_filtered['剩余规模(万元)'] > 10000]
    return cbonds_df_filtered


def bond_screen():
    # 定义筛选条件：剩余年限小于等于3年且现价在100元以下的可转债
    df = jq.get_bars(convertible=True, multiple_benchmark=None)
    print(df)
    df_filtered = df[
        (df['convert_ratio'] > 0) & (df['maturity_date'] <= datetime.datetime.now() + datetime.timedelta(days=1095)) & (
                df['last_price'] < 100)]

    # 按照溢价率排序，取前10只作为推荐结果
    df_res = df_filtered.sort_values(by='premium_rate', ascending=True)[:10]

    # 输出推荐结果
    print(df_res.to_string())


if __name__ == '__main__':
    # bond_screen()

    test_df = get_cbonds()
    print(test_df)
