# -*- coding: utf-8 -*-
# @Author  : BoPo
# @Time    : 2021/10/21 17:40
# @Function:

from snowball import api_ref
from snowball.utils import fetch


def test_fetch():
    response = fetch(api_ref.watch_list)
    assert response, response
