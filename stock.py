from jqdatasdk import *
import config.jq as jq

account, password = jq.jq_account()
auth(account, password)


def main():
    df = get_price(security='000001.XSHE', start_date='2022-01-01', end_date='2022-05-01')
    print(df)


if __name__ == '__main__':
    main()
