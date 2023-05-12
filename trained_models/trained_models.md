All models are LightGBM regressors aiming at predicting US stocks future price variation.

They are trained on three dataset types: 

- market data only : Open, High, Low, Close, Volume.
We then compute various features based on those : log return with various lags, close value to various moving averages, moving averages cross, historical volatility, volume changes with different lags.

- fundamental data (macro economics, stock financials) only : 10Y US bonds, VIX, EPS, PEG, pe ratio, dividends yield, earnings announcement surprise, sector, ... 

- both market and fundamental data

Models are trained to predict stocks price variation at different time horizons. More precisely, as we are supposed to get the end of day prices the day after, all models are actually trained to predict the horizon + 1 day.

lgbm_market_1d: trained on market data only to predict tomorrow price
lgbm_market_1w: trained on market data only to predict price in one week
lgbm_market_2w: trained on market data only to predict price in two weeks
lgbm_market_1m: trained on market data only to predict price in one month
lgbm_fundamental_1d: trained on fundamental data only to predict tomorrow price
lgbm_fundamental_1w: trained on fundamental data only to predict price in one week
lgbm_fundamental_2w: trained on fundamental data only to predict price in two weeks
lgbm_fundamental_1m: trained on fundamental data only to predict price in one month
lgbm_market_and_fundamental_1d: trained on market and fundamental data to predict tomorrow price
lgbm_market_and_fundamental_1w: trained on market and fundamental data to predict price in one week
lgbm_market_and_fundamental_2w: trained on market and fundamental data to predict price in two weeks
lgbm_market_and_fundamental_data_1m: trained on market and fundamental data to predict price in one month
