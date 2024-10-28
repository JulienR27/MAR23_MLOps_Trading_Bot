import datetime
from datetime import date
import yfinance as yf

def get_bonds(last_date = date.today(), historical_days = 1450):
    '''
    Downloads 10-Y bond historical daily data
    '''

    #Calculating current and historical periods
    historical_date = last_date - datetime.timedelta(days=historical_days)

    #Retrieving data from yahoo, keeping only close value (which is same as "Adj Close")
    histo = yf.download("^TNX", start=historical_date, end=last_date, interval="1d", progress=False)['Close']
    
    histo.rename(columns = {"^TNX":"10Y_bonds"}, inplace = True)
    
    histo = histo.tz_localize(None)
    
    histo["10Y_bond_MoM"] = histo["10Y_bonds"].pct_change(21)
    
    return histo

bond = get_bonds()