# -*- coding: utf-8 -*-
# @Author  : BoPo
# @Time    : 2021/10/21 17:40
# @Function:


def test_report(api):
    result = api.report('SZ002027')
    assert result, result


def test_earning_forecast(api):
    result = api.earning('SZ002027')
    assert result, result
