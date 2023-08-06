from snowball import api_ref
from snowball import utils


def watch_list() -> dict:
    """ user 自选列表

    :return:
    """
    return utils.fetch(api_ref.watch_list)


def watch_stock(uid) -> dict:
    """ user 自选列表详情

    :param uid:
    :return:
    """
    return utils.fetch(api_ref.watch_stock.format(uid))
