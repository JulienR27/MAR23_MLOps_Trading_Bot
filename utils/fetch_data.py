import pandas as pd
import datetime
from datetime import date
import requests

Tiingo_API = "070e58c9f4bc1e4a5239300dad12ae1c4a87c892"

def get_last_historic_date(last_date = date.today(), historical_days = 200):
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

def fetch_stock(ticker, last_date = date.today(), historical_days = 200):
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
    return response
