symbol = 'SH600036'


def test_cash_flow(api):
    """ 现金流量表
    """

    result = api.cash_flow(symbol, is_annals=0, count=10)
    assert result, result


def test_indicator(api):
    """ 业绩指标
    """

    result = api.indicator(symbol, is_annals=0, count=10)
    assert result, result


def test_balance(api):
    """ 资产负债表
    """

    result = api.balance(symbol, is_annals=0, count=10)
    assert result, result


def test_income(api):
    """ 利润表
    """

    result = api.income(symbol, is_annals=0, count=10)
    assert result, result


def test_business(api):
    """ 主营业务构成
    """

    result = api.business(symbol, is_annals=0, count=10)
    assert result, result
