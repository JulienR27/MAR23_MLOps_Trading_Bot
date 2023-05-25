import pandas as pd
import datetime
from datetime import date
import requests
import yfinance as yf
import sys
#sys.path.append("C:/Users/Julien/Documents/EI/Datascientest/MLOps/Projet/MAR23_MLOps_Trading_Bot")
from src.domain.utils import new_earnings

Tiingo_API = "070e58c9f4bc1e4a5239300dad12ae1c4a87c892"

def get_last_historic_date(last_date = date.today(), historical_days = 350):
    '''
    As output come 2 variables:        the min/max dates as str value
    '''
    todays_year = last_date.year
    todays_month = last_date.month
    todays_day = last_date.day
    historical_date = last_date - datetime.timedelta(days=historical_days)
    historical_year = historical_date.year
    historical_month = historical_date.month
    historical_day = historical_date.day
    #Transfrom dates to str    
    historical_date_str =str(historical_year) + "-" + str(historical_month) + "-" + str(historical_day)
    latest_date_str = str(todays_year) + "-" + str(todays_month) + "-" + str(todays_day)
    
    return historical_date_str, latest_date_str


def fetch_stock(ticker, last_date = date.today(), historical_days = 350):
    '''
    Get the trading information about a stock for a range of days in "historical_days" before the "last_date"
    The output is a DataFrame with columns "close","high","low","open","volume","splitFactor"
    The output are adjusted prices
    '''
    #Get latest and historical day, month, year for API request
    historical_date_str, latest_date_str = get_last_historic_date(last_date, historical_days)

    #The request itself
    url = f'https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={historical_date_str}&endDate={latest_date_str} '
    headers = {
            'Content-Type': 'application/json',
            'Authorization' : f'Token {Tiingo_API}'
            }
    r = requests.get(url, headers=headers)
    response = r.json()
    response = pd.DataFrame(response)
    response.set_index(["date"], inplace = True)
    response.index = pd.to_datetime(response.index)
    response.drop(columns = ["close","high","low","open","volume","splitFactor"],axis = 1, inplace = True)
    response.rename(columns = {"adjClose":"close","adjHigh":"high","adjLow":"low","adjOpen":"open","adjVolume":"volume"}, inplace = True)
    # Delete timezone from the stock dataset
    response.index = response.index.tz_convert(None)
    return response


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
