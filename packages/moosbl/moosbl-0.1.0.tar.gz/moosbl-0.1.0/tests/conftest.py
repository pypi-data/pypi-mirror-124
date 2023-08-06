# -*- coding: utf-8 -*-
import pytest


@pytest.fixture(scope='session')
def api():
    from snowball import snowball
    return snowball
