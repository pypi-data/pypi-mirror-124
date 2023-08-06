from snowball import api_ref
from snowball import utils


def quote(*symbols) -> dict:
    """ 实时行情
     获取某支股票的行情数据
    :param symbols:
    :return:
    """
    url = api_ref.realtime_quote.format(','.join(symbols))
    return utils.fetch(url, token=False)


def depth(symbol: str = None) -> dict:
    """ 盘口行情
    获取某支股票的盘口数据
    :param symbol:
    :return:
    """

    url = api_ref.realtime_depth.format(symbol)
    return utils.fetch(url)
