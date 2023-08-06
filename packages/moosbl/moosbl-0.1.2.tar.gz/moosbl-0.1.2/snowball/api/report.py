from snowball import api_ref
from snowball import utils


def report(symbol) -> dict:
    """ 机构评级
    获取机构评级数据
    :param symbol:
    :return:
    """

    url = api_ref.report_latest_url.format(symbol)
    return utils.fetch(url)


def earning(symbol) -> dict:
    """ 业绩预告 (earning forecast)
    按年度获取业绩预告数据
    :param symbol:
    :return:
    """

    url = api_ref.report_earning_url.format(symbol)
    return utils.fetch(url)
