#!/usr/bin/env python

"""Tests for `snowball` package."""

symbol = 'SH600036'


def test_sk_holder_chg(api):
    """ 控股人变更
    """

    result = api.sk_holder_chg(symbol)
    assert result, result


def test_sk_holder(api):
    """ 控股人
    """
    result = api.sk_holder(symbol)
    assert result, result


def test_industry(api):
    """ 行业数据
    """
    result = api.industry(symbol)
    assert result, result


def test_holders(api):
    """F10 股东人数
    """
    result = api.holders(symbol)
    assert result, result


def test_bonus(api):
    """ F10 分红融资
    """
    result = api.bonus(symbol, page=1, size=10)
    assert result, result


def test_org_holding_change(api):
    """ F10 机构持仓
    """
    result = api.org_holding_change(symbol)
    assert result, result


def test_industry_compare(api):
    """ F10 行业对比
    """
    result = api.industry_compare(symbol)
    assert result, result


def test_business_analysis(api):
    """ 业务分析
    """
    result = api.business_analysis(symbol)
    assert result, result


def test_shareschg(api):
    """

    """
    result = api.shareschg(symbol, count=5)
    assert result, result


def test_top_holders(api):
    """ F10 十大股东
    """
    result = api.top_holders(symbol, circula=1)
    assert result, result


def test_main_indicator(api):
    """ F10 主要指标
    """
    result = api.main_indicator(symbol)
    assert result, result
