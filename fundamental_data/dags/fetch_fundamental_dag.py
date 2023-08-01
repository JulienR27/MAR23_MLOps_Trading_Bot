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
from src.domain.utils.fetch_data import fetch_fundamental#, fetch_stock


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
            'start_date': datetime(2023,7,21)
        }
)

tickers = ["AAPL", "TSLA"]

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