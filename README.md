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
    |-- utils
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

# 第三方工具
