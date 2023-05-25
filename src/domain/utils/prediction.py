import numpy as np 
import pandas as pd
import sklearn.preprocessing._label as label
import sys
#sys.path.append("C:/Users/Julien/Documents/EI/Datascientest/MLOps/Projet/MAR23_MLOps_Trading_Bot")
from src.domain.utils.features_engineering import market_features_engineering, fundamental_features_engineering
from src.domain.utils.fetch_data import fetch_stock, fetch_fundamental
from src.domain.utils import US_bond_yfinance, VIX

# Stocks environment (Dow30)
env_tickers = ["AXP", "AMGN", "AAPL", "BA", "CAT", "CSCO", "CVX", "GS", "HD", "HON", "IBM", "INTC", "JNJ", "KO", "JPM", "MCD", "MMM", "MRK", "MSFT", "NKE", "PG", "TRV", "UNH", "CRM", "VZ", "V", "WBA", "WMT", "DIS", "DOW"]

def make_prediction(model, sector_encoder: label.LabelEncoder, time_horizon: str, trading_type: str, tickers: list = []) -> dict:
    """
    
    Parameters
    ----------
    tickers : list of tickers. If empty (default) , takes all tickers in environment
    time_horizon: str in ("1d", "1w", "2w", "1m")
    trading_type: str in ("market", "fundamental", "market_and_fundamental")
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
        
    X_fundamental = pd.DataFrame(columns=["date", "stock"]).set_index("date")
    if "fundamental" in trading_type:
        for ticker in tickers:
            # Get fundamental data
            fundamental_data = fetch_fundamental(ticker)
            # Add stock identifier to merge with market data
            fundamental_data["stock"] = ticker
            # Append
            X_fundamental = pd.concat([X_fundamental, fundamental_data]) 
        # Get US bond data (more than 31 days to make sure to be able to compute MoM)
        us_bond = US_bond_yfinance.get_bonds(historical_days = 35)
        X_fundamental = X_fundamental.join(us_bond, how = 'left')
        # Get VIX data
        vix_df = VIX.get_vix(historical_days=35)
        X_fundamental = X_fundamental.join(vix_df, how = 'left')
        # Get fundamental features
        X_fundamental = fundamental_features_engineering(X_fundamental)
        # Sector encoding with original label encoder
        X_fundamental.loc[:, "sector"] = sector_encoder.transform(X_fundamental["sector"])
        
    X_market = pd.DataFrame(columns=["date", "stock"]).set_index("date")
    if "market" in trading_type: 
        for ticker in tickers:
            # Get at least 200 days of market data to compute features (for MA_200) 
            market_data = fetch_stock(ticker)
            # Compute features
            market_data_engineered = market_features_engineering(market_data, time_horizon)
            market_data_engineered["stock"] = ticker
            X_market = pd.concat([X_market, market_data_engineered])
     
    # Concatenate fundamental and market features
    X = pd.merge(X_fundamental, X_market, left_on=["date", "stock"], right_on=["date", "stock"], how="outer")
    
    for ticker in tickers:
        X_ticker = X[X["stock"]==ticker].drop(["stock"], axis=1)
        # Sort by ascending date
        X_ticker.sort_values(by="date", inplace=True)    
        # Make prediction
        prediction = model.predict(np.array(X_ticker.iloc[-1]).reshape(1, -1))
        # Append to predictions dict
        predictions[ticker] = prediction[0] 
        
    # Sort predictions dict by values
    predictions = dict(sorted(predictions.items(), key=lambda x:x[1], reverse=True))
    
    return predictions