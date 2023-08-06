# -*- coding: utf-8 -*-
# @Author  : BoPo
# @Time    : 2021/10/21 17:40
# @Function:


def test_nav_daily(api):
    result = api.nav_daily(symbol='ZH2567925')
    assert result, result


def test_re_balancing_history(api):
    result = api.re_balancing_history(symbol='ZH2567925')
    assert result, result
