from snowball import api_ref
from snowball import utils


def nav_daily(symbol) -> dict:
    """ cube 组合净值

    :param symbol:
    :return:
    """
    url = api_ref.nav_daily.format(symbol)
    return utils.fetch(url=url, headers={"Host": "xueqiu.com"})


def re_balancing_history(symbol, count=20, page=1) -> dict:
    """ cube 组合历史交易信息

    :param symbol:
    :param count:
    :param page:
    :return:
    """
    url = api_ref.rebalancing_history.format(symbol)
    return utils.fetch(url=url, headers={"Host": "xueqiu.com"}, params={'page': page, 'count': count})
