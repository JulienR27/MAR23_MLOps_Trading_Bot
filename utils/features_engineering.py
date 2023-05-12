import numpy as np 

def market_features_engineering(df):
    """

    Parameters
    ----------
    df : Raw historical DataFrame.

    Returns
    -------
    TYPE
        Features DataFrame.

    """    
    df_temp = df.sort_values("date", ascending=True)
    df_temp["volume_chg"] = df_temp["volume"].pct_change()
    df_temp["volume_chg_5day"] = df_temp["volume"].pct_change(5)
    df_temp["volume_chg_1month"] = df_temp["volume"].pct_change(21)
    df_temp["open_return"] = np.log(df_temp["open"].pct_change() + 1)
    df_temp["high_return"] = np.log(df_temp["high"].pct_change() + 1)
    df_temp["low_return"] = np.log(df_temp["low"].pct_change() + 1)
    df_temp["close_return"] = np.log(df_temp["close"].pct_change() + 1)
    df_temp["intraday_amplitude"] = np.log(df_temp["high"] / df_temp["low"] + 1)
    
    df_temp["MA5"] = df_temp['close'].rolling(window=5, min_periods=5).mean()
    df_temp["MA21"] = df_temp['close'].rolling(window=21, min_periods=21).mean()
    df_temp["MA50"] = df_temp['close'].rolling(window=50, min_periods=50).mean()
    df_temp["MA100"] = df_temp['close'].rolling(window=100, min_periods=100).mean()
    df_temp["close_to_MA5"] = (df_temp["close"] - df_temp["MA5"]) / df_temp["MA5"]
    df_temp["close_to_MA21"] = (df_temp["close"] - df_temp["MA21"]) / df_temp["MA21"]
    df_temp["close_to_MA50"] = (df_temp["close"] - df_temp["MA50"]) / df_temp["MA50"]
    df_temp["close_to_MA100"] = (df_temp["close"] - df_temp["MA100"]) / df_temp["MA100"]
    df_temp["MA5_21_cross"] = (df_temp["MA5"] - df_temp["MA21"]) / df_temp["MA21"]

    df_temp["return_2d"] = np.log(df_temp["close"].pct_change(2) + 1)
    df_temp["return_3d"] = np.log(df_temp["close"].pct_change(3) + 1)
    df_temp["return_4d"] = np.log(df_temp["close"].pct_change(4) + 1)
    df_temp["return_5d"] = np.log(df_temp["close"].pct_change(5) + 1)
    df_temp["return_2w"] = np.log(df_temp["close"].pct_change(10) + 1)
    df_temp["return_1m"] = np.log(df_temp["close"].pct_change(21) + 1)
    df_temp["return_2m"] = np.log(df_temp["close"].pct_change(42) + 1)
    df_temp["return_3m"] = np.log(df_temp["close"].pct_change(63) + 1)
    df_temp["volatility_1m"] = np.log(df_temp["close"]).diff().rolling(window=21, min_periods=21).std()
    df_temp["volatility_2m"] = np.log(df_temp["close"]).diff().rolling(window=42, min_periods=42).std()
    #df_temp["volatility_3m"] = np.log(df_temp["close"]).diff().rolling(window=63, min_periods=42).std()

    return df_temp[["volume_chg", "open_return", "high_return", "low_return", "intraday_amplitude", "close_return", 
               "volume_chg_5day", "volume_chg_1month",
               "MA5_21_cross", "close_to_MA5", "close_to_MA21", "close_to_MA50", "close_to_MA100",
               "return_2d", "return_3d", "return_4d", "return_5d", "return_2w", "return_1m", "return_2m", "return_3m",
              "volatility_1m", "volatility_2m"]]
