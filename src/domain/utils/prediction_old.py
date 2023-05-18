import numpy as np 
import pandas as pd
from utils.features_engineering import market_features_engineering, fundamental_features_engineering
from utils.fetch_data import fetch_stock, fetch_fundamental
from utils import US_bond_yfinance, VIX

# Stocks environment (Dow30)
env_tickers = ["AXP", "AMGN", "AAPL", "BA", "CAT", "CSCO", "CVX", "GS", "HD", "HON", "IBM", "INTC", "JNJ", "KO", "JPM", "MCD", "MMM", "MRK", "MSFT", "NKE", "PG", "TRV", "UNH", "CRM", "VZ", "V", "WBA", "WMT", "DIS", "DOW"]

def make_prediction(model, sector_encoder, time_horizon, trading_style, tickers=[]):
    """
    
    Parameters
    ----------
    tickers : list of tickers. If empty (default) , takes all tickers in environment
    time_horizon: str in ("1d", "1w", "2w", "1m")
    trading_style: str in ("market", "fundamental", "market_and_fundamental")
    model : regression model
    sector_encoder : label encoder for sector feature

    Returns
    -------
    sorted dictionnary of predictions

    """
    
    predictions = dict()

    # If tickers is empty, we make predictions on entire environment
    if not tickers:
        tickers = env_tickers
        
    X_fundamental = pd.DataFrame()
    if "fundamental" in trading_style:
        # Get US bond data (more than 31 days to make sure to be able to compute MoM)
        us_bond = US_bond_yfinance.get_bonds(historical_days = 35)
        us_bond["10Y_bond_MoM"] = fundamental_features["10Y_bonds"].pct_change(21)
        # Get VIX data
        vix_df = VIX.get_vix(historical_days=35)
        # Get fundamental data
        fundamental_data = fetch_fundamental(ticker)
        # Get fundamental features
        X_fundamental = fundamental_features_engineering(fundamental_data)
        # Sector encoding with original label encoder
        X_fundamental.loc[:, "sector"] = sector_encoder.transform(X_fundamental["sector"])
        
    X_market = pd.DataFrame()
    if "market" in trading_style: 
        # Get at least 200 days of market data to compute features (for MA_200) 
        market_data = fetch_stock(ticker)
        # Compute features
        X_market = market_features_engineering(market_data, time_horizon)
     
    # Concatenate fundamental and market features
    X = pd.concat([X_fundamental, X_market], axis=1)
            
        # Make prediction
        prediction = model.predict(np.array(X.iloc[-1]).reshape(1, -1))
        # Append to predictions dict
        predictions[ticker] = prediction[0] 
        
    # Sort predictions dict by values
    predictions = dict(sorted(predictions.items(), key=lambda x:x[1], reverse=True))
    
    return predictions