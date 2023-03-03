import easytrader

# 设置客户端信息（同花顺）
user = easytrader.use('ths')

# 连接客户端(同花顺：先登录且保存密码且勾选自动登录)
ths_path = r'D:\同花顺\同花顺远航版\transaction\xiadan.exe'
user.connect(ths_path)

# 设置客户端编辑文本形式：type_keys(不设置会出现无法自动输入的请求)
user.enable_type_keys_for_editor()

# 账户余额
balance = user.balance
print('账户余额', balance)

# 查询持仓（仓位）
position = user.position
print('查询持仓', position)

# 查询当日成交
today_trades = user.today_trades
print('查询当日成交', today_trades)

# 查询当日委托
today_entrusts = user.today_entrusts
print('查询当日委托', today_entrusts)

# 买入
# sell_no = user.buy('000001', price='', amount=100)
# print(sell_no)

# 自动打新
# user.auto_ipo()

# 撤单：根据单号撤销，不稳定有效，待解决
# cancel = user.cancel_entrust('')
# print(cancel)

# 撤单：全部撤销
# cancel = user.cancel_all_entrusts()
# print(cancel)


