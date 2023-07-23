from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime
import sys, os
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service # new line caused by DeprecationWarning: executable_path has been deprecated, please pass in a Service object
from selenium.webdriver.chrome.options import Options # new line for DevToolsActivePort issue
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import io
from pathlib import Path
current_path = Path(os.getcwd())
project_path = current_path.parent.parent.as_posix()
sys.path.append(project_path)
from src.domain.utils.fetch_data import fetch_fundamental


fetch_data_dag = DAG(
    dag_id="fetch_stock_data_dag",
    doc_md="""# Fetching fundamental data DAG
This `DAG` :

* extract and transform stocks data from Zacks website

This DAG has been made by the trading bot datascientest team

    """,
    schedule_interval="0 6 * * 1-5",
    tags=['tradingbot'],
    default_args={
            'start_date': datetime(2023,7,19)
        }
)

tickers = ["AAPL", "TSLA"]

def fetch_fundamental(ticker, historical_days=35):
    # Get close data to compute peRatio and DividendsYield
    fundamental_data = fetch_stock(ticker, historical_days=historical_days)["close"]
    # Get stock dividents & earnings
    stock_earnings, stock_dividends = new_earnings.get_earn_and_dividends(ticker, inference=True) 
    # Combining data with earnings & dividends info
    fundamental_data = pd.concat([fundamental_data, stock_earnings], axis=1, join="inner")
    fundamental_data = fundamental_data.join(stock_dividends, how = 'left')
    # Get stock sector and industry from yahoo finance
    stock_metadata = yf.Ticker(ticker).info
    # They are not always there
    try:
        fundamental_data['sector'] = stock_metadata['sector']
    except:
        fundamental_data['sector'] = "Industrials" #to check
    try:
        fundamental_data['industry'] = stock_metadata['industry']
    except:
        fundamental_data['industry'] = float("nan")
   #  # Get VIX Volatility index and join
   #  vix_df = VIX.get_vix(historical_days=historical_days)
   #  fundamental_data = fundamental_data.join(vix_df, how = 'left')
   #  # Get 10Y_bond index and combine data with US Bonds
   #  us_bond = US_bond_yfinance.get_bonds(historical_days = 35)
   #  fundamental_data = fundamental_data.join(us_bond, how = 'left')
    # Sorting values by date
    fundamental_data.sort_values(by = 'date', axis = 0, ascending = True, inplace = True)
    
    return fundamental_data

def fetch_all_fundamental():
    X_fundamental = pd.DataFrame(columns=["date", "stock"]).set_index("date")
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
    # not here
    # # Sector encoding with original label encoder
    # X_fundamental.loc[:, "sector"] = sector_encoder.transform(X_fundamental["sector"])
    now = datetime.now().strftime("%Y%m%d %H:%M")
    X_fundamental.to_csv("./log"+now+".csv")


task_1 = PythonOperator(
    task_id='fetch_all_fundamental',
    dag=fetch_data_dag,
    python_callable=fetch_all_fundamental
)