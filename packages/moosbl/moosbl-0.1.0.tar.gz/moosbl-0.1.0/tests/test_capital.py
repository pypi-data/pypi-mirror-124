symbol = 'SH600036'


def test_margin(api):
    """融资融券
    """
    result = api.margin(symbol, page=1, size=180)
    assert result, result


def test_block_trans(api):
    """大宗交易
    """

    result = api.block_trans(symbol, page=1, size=30)
    assert result, result


def test_capital_assort(api):
    """ 资金成交分布
    """
    result = api.capital_assort(symbol)
    assert result, result


def test_capital_flow(api):
    """资金流向趋势
    """
    result = api.capital_flow(symbol)
    assert result, result


def test_capital_history(api):
    """资金流向历史
    """
    result = api.capital_history(symbol, count=20)
    assert result, result
