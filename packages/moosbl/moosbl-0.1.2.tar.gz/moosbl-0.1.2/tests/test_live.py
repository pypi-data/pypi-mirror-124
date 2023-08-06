# -*- coding: utf-8 -*-
# @Author  : BoPo
# @Time    : 2021/10/21 17:40
# @Function:


def test_quote(api):
    result = api.quote('SZ002027', 'SH600036')
    assert result, result


def test_depth(api):
    result = api.depth('SZ002027')
    assert result, result
