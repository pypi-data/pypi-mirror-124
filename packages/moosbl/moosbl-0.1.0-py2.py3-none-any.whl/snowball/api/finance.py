from snowball import api_ref
from snowball import utils


def cash_flow(symbol, is_annals=0, count=10) -> dict:
    """ 现金流量表

    :param symbol:
    :param is_annals:
    :param count:
    :return:
    """

    url = api_ref.finance_cash_flow_url.format(symbol)

    params = {'count': count, 'type': 'Q4' if is_annals == 1 else ''}
    return utils.fetch(url, params=params)


def indicator(symbol, is_annals=0, count=10) -> dict:
    """ 业绩指标

     按年度、季度获取业绩报表数据。
    :param symbol:
    :param is_annals:
    :param count:
    :return:
    """

    url = api_ref.finance_indicator_url.format(symbol)

    params = {'count': count, 'type': 'Q4' if is_annals == 1 else ''}
    return utils.fetch(url, params=params)


def balance(symbol, is_annals=0, count=10) -> dict:
    """ 资产负债表

    :param symbol:
    :param is_annals:
    :param count:
    :return:
    """

    url = api_ref.finance_balance_url.format(symbol)

    params = {'count': count, 'type': 'Q4' if is_annals == 1 else ''}
    return utils.fetch(url, params=params)


def income(symbol, is_annals=0, count=10) -> dict:
    """ 利润表

    :param symbol:
    :param is_annals:
    :param count:
    :return:
    """

    url = api_ref.finance_income_url.format(symbol)

    params = {'count': count, 'type': 'Q4' if is_annals == 1 else ''}
    return utils.fetch(url, params=params)


def business(symbol, is_annals=0, count=10) -> dict:
    """ 主营业务构成

    :param symbol:
    :param is_annals:
    :param count:
    :return:
    """

    url = api_ref.finance_business_url.format(symbol)

    params = {'count': count, 'type': 'Q4' if is_annals == 1 else ''}
    return utils.fetch(url, params=params)
