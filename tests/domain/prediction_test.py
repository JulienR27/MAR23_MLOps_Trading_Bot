import sys, os
from pathlib import Path
current_path = Path(os.getcwd())
project_path = current_path.parent.parent.as_posix()
sys.path.append(project_path)
from src.domain.utils.prediction import make_prediction


def test_make_prediction():
    time_horizon = "2w"
    trading_type = "market_and_fundamental"
    tickers = ["AAPL"]
    # Loading the right model
    model = load(f'{project_path}/src/domain/trained_models/lgbm_{trading_type}_{time_horizon}.joblib') 
    # Loading sector encoder
    sector_encoder = load(f'{project_path}/src/domain/trained_models/label_encoder.joblib') 
    # Prediction
    predictions = make_prediction(model, sector_encoder, time_horizon, trading_type, tickers)
    assert predictions