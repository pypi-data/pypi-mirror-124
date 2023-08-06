from snowball import api_ref
from snowball import utils


def sk_holder_chg(symbol) -> dict:
    """ 控股人变更

    :param symbol:
    :return:
    """
    url = api_ref.f10_skholderchg.format(symbol)
    return utils.fetch(url)


def sk_holder(symbol) -> dict:
    """ 控股人

    :param symbol:
    :return:
    """
    url = api_ref.f10_skholder.format(symbol)
    return utils.fetch(url)


def industry(symbol) -> dict:
    """ 行业数据

    :param symbol:
    :return:
    """
    url = api_ref.f10_industry.format(symbol)
    return utils.fetch(url)


def holders(symbol) -> dict:
    """F10 股东人数

    :param symbol:
    :return:
    """
    url = api_ref.f10_holders.format(symbol)
    return utils.fetch(url)


def bonus(symbol, page=1, size=10) -> dict:
    """ F10 分红融资

    :param symbol:
    :param page:
    :param size:
    :return:
    """
    url = api_ref.f10_bonus.format(symbol)
    return utils.fetch(url=url, params={'page': page, 'size': size})


def org_holding_change(symbol) -> dict:
    """ F10 机构持仓

    :param symbol:
    :return:
    """
    url = api_ref.f10_org_holding_change.format(symbol)
    return utils.fetch(url)


def industry_compare(symbol) -> dict:
    """ F10 行业对比

    :param symbol:
    :return:
    """
    url = api_ref.f10_industry_compare.format(symbol)
    return utils.fetch(url)


def business_analysis(symbol) -> dict:
    """

    :param symbol:
    :return:
    """
    url = api_ref.f10_business_analysis.format(symbol)
    return utils.fetch(url)


def shareschg(symbol, count=5) -> dict:
    """

    :param symbol:
    :param count:
    :return:
    """
    url = api_ref.f10_shareschg.format(symbol)
    return utils.fetch(url=url, params={'count': count})


def top_holders(symbol, circula: int = 1) -> dict:
    """ F10 十大股东

    :param symbol:
    :param circula:
    :return:
    """
    url = api_ref.f10_top_holders.format(symbol)
    return utils.fetch(url=url, params={'circula': circula, })


def main_indicator(symbol) -> dict:
    """ F10 主要指标

    :param symbol:
    :return:
    """
    url = api_ref.f10_indicator.format(symbol)
    return utils.fetch(url)
