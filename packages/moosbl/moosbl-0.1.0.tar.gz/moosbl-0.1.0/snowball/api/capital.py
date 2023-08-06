from snowball import api_ref
from snowball import utils


def margin(symbol, page=1, size=180) -> dict:
    """融资融券
    融资融券数据

    :param symbol:
    :param page:
    :param size:
    :return:
    """
    url = api_ref.capital_margin_url.format(symbol)
    return utils.fetch(url=url, params={'page': page, 'size': size})


def block_trans(symbol, page=1, size=30) -> dict:
    """大宗交易
     大宗交易数据

    :param symbol:
    :param page:
    :param size:
    :return:
    """

    url = api_ref.capital_blocktrans_url.format(symbol)
    return utils.fetch(url=url, params={'page': page, 'size': size})


def capital_assort(symbol) -> dict:
    """ 资金成交分布
     获取资金成交分布数据

    :param symbol:
    :return:
    """
    url = api_ref.capital_assort_url.format(symbol)
    return utils.fetch(url)


def capital_flow(symbol) -> dict:
    """资金流向趋势
     获取当日资金流如流出数据，每分钟数据

    :param symbol:
    :return:
    """
    url = api_ref.capital_flow_url.format(symbol)
    return utils.fetch(url)


def capital_history(symbol, count=20) -> dict:
    """资金流向历史
     获取历史资金流如流出数据，每日数据

    :param symbol:
    :param count:
    :return:
    """
    url = api_ref.capital_history_url.format(symbol)
    return utils.fetch(url=url, params={'count': count})
