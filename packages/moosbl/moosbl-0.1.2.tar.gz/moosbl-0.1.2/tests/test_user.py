# -*- coding: utf-8 -*-
# @Author  : BoPo
# @Time    : 2021/10/21 17:40
# @Function:


def test_watch_list(api):
    result = api.watch_list()
    assert result, result


def test_watch_stock(api):
    result = api.watch_stock(11)
    assert result, result
