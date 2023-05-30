from src.domain.utils.fetch_data import fetch_stock, fetch_fundamental

# def test_fetch_fundamental():
#     fundamental = fetch_fundamental("AAPL")
#     assert all(feature in list(fundamental.columns) for feature in ['close', 'eps', 'trailing_eps_1Y', 'epsQoQ', 'surprise_%', 'expected_growth', 'previous_surprise', 'days_after_earn_report', 'Amount', 
#     'dividends_change', 'prev_div_change', 'days_after_divid_report', 'sector', 'industry'])


def test_fetch_stock():
    market = fetch_stock("AAPL")
    assert all(feature in list(market.columns) 
               for feature in ['close', 'high', 'low', 'open', 'volume'])
