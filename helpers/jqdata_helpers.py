from jqdatasdk import *
import config.jq as jq

# 登录聚宽账号
account, password = jq.jq_account()
auth(account, password)


def get_jq_query_count():
    query_count = get_query_count()
    print('查询当日剩余可调用数据条数: {}'.format(query_count))
