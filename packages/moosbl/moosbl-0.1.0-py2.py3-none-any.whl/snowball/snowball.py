"""Main module."""

try:
    from snowball.api.capital import (margin, block_trans, capital_assort, capital_flow, capital_history)
    from snowball.api.cube import (nav_daily, re_balancing_history)
    from snowball.api.f10 import (sk_holder_chg, sk_holder, main_indicator, industry, holders, bonus, org_holding_change, industry_compare, business_analysis, shareschg, top_holders)
    from snowball.api.finance import (cash_flow, indicator, balance, income, business)
    from snowball.api.live import (quote, depth)
    from snowball.api.report import (report, earning)
    from snowball.utils.token import (get_token, set_token)
    from snowball.api.user import (watch_list, watch_stock)
except ImportError as ex:
    raise ex
