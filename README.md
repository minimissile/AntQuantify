![py37][py37] ![version][version]

# 蚂蚁量化

> 专注于股票、可转债、ETF量化研究

# 目录结构
```markdown
|-- AntQuantify
    |-- .gitignore
    |-- directoryList.md
    |-- README.md
    |-- .idea
    |   |-- .gitignore
    |   |-- AntQuantify.iml
    |   |-- misc.xml
    |   |-- modules.xml
    |   |-- vcs.xml
    |   |-- workspace.xml
    |   |-- inspectionProfiles
    |       |-- profiles_settings.xml
    |       |-- Project_Default.xml
    |-- config
    |   |-- jq.py
    |   |-- __init__.py
    |   |-- __pycache__
    |       |-- config.cpython-311.pyc
    |       |-- jq.cpython-311.pyc
    |       |-- __init__.cpython-311.pyc
    |-- data
    |   |-- convertible_bond - 可转债数据
    |   |-- etf - etf数据
    |   |-- stock - 股票数据
    |-- example
    |-- strategy
    |-- trader
    |-- helpers 
        |-- stock.py

```


# 使用
> 新建 config/jq.py 文件， 并写入以下方法

```python
def jq_account():
    """
    获取聚宽账号
    :return: 聚宽本地api的账号
    """
    return '账号', '密码'
```

## 数据本地化
> 运行 helpers/init_db.py
> 
聚宽每日api数据请求数有显示，需要多天才能全部将数据存储至本地

如果本地化时提示文件路径相关错误，请手动新建 data/convertible_bond, data/etf, data/stock 等文件夹


# 第三方工具

# 更新计划

# 相关文档
[聚宽在线量化 api文档](https://www.joinquant.com/help/api/help#api:API%E6%96%87%E6%A1%A3)

[JQData-本地量化数据说明书](https://www.joinquant.com/help/api/help#JQData:JQData)

[tushare](https://tushare.pro/)
