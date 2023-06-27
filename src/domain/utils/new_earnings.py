import time
from datetime import date
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


def search_symbol(symbol, driver):
    elem = driver.find_element(By.ID, "ticker")
    elem.send_keys(symbol)
    elem.send_keys(Keys.RETURN)
    #driver.implicitly_wait(3)

def find_estim_tables(driver):
    '''
    get a table with earnings on a page  ZACK
    '''
    #Find required table
    elem = driver.find_element(By.XPATH, '//*[@id="earnings_announcements_earnings_table"]') 
    #get all rows from the table
    rows = [row.text.encode("utf8") for row in elem.find_elements(By.TAG_NAME, 'tr')]
    #convert list of bytes to list of strings
    rows = [row.decode("utf-8").replace("\n"," ") for row in rows]
    #convert list of strings to a dataframe 
    earnings_history_df = pd.read_csv(io.StringIO('\n'.join(rows)), delim_whitespace=True, names = ['date', 'Period_Ending', 'Estimate', 'Reported', 'Surprise', 'Surprise_%', "str1", "str2"])
    
    #Find the latest estimate 
    elem = driver.find_element(By.XPATH, '//*[@id="right_content"]/section[2]/div') 
    #get all rows from the table
    rows1 = [row.text.encode("utf8") for row in elem.find_elements(By.TAG_NAME, 'td')]
    rows2 = [row.text.encode("utf8") for row in elem.find_elements(By.TAG_NAME, 'th')]
    #convert list of bytes to list of strings
    rows1 = [row.decode("utf-8").replace("\n"," ") for row in rows1]
    rows2 = [row.decode("utf-8").replace("\n"," ") for row in rows2]    
    #convert list of strings to a dataframe 
    earnings_latest_df = pd.DataFrame(rows1).transpose()
    earnings_latest_df.columns =  ['Period_Ending', 'Estimate', 'Surprise_%']
    earnings_latest_df["date"] = rows2[-1].split(" ")[0]
    
    earnings = pd.concat([earnings_latest_df, earnings_history_df], ignore_index = True, sort = False)
    earnings['date'] = pd.to_datetime(earnings['date'])
    earnings.set_index(["date"], inplace = True)
    #case when report just happened and current estimate not yet updated
    #earnings = earnings[~earnings.index.duplicated(keep='last')]
    
    return earnings

def find_divid_tables(driver, inference=False):
    '''
    get a table with dividends on a page  ZACK
    '''
    element = driver.find_element(By.XPATH, '//*[@id="earnings_announcements_tabs"]/ul')
    driver.execute_script('arguments[0].scrollIntoView({block: "center", inline: "center"})', element)
    
    elem = driver.find_element(By.XPATH, '//*[@id="ui-id-7"]')
    driver.execute_script ("arguments[0].click();",elem)
    # elem.click()
    #time.sleep(3) # try with comment
    
    #Expand 100 records if training
    if not inference:
        dropdown = driver.find_element(By.NAME, "earnings_announcements_dividends_table_length")
        Select(dropdown).select_by_visible_text("100")
    
    #Find required table
    elem = driver.find_element(By.XPATH, '//*[@id="earnings_announcements_dividends_table"]') 
    #get all rows from the table
    rows = [row.text.encode("utf8") for row in elem.find_elements(By.TAG_NAME, 'tr')]
    #convert list of bytes to list of strings
    rows = [row.decode("utf-8").replace("\n"," ") for row in rows]
    #convert list of strings to a dataframe 
    
    dividends_history_df = pd.read_csv(io.StringIO('\n'.join(rows)), delim_whitespace=True, header = 0, names = ['Date_Paid', 'Amount', 'Date_Announced', 'Ex-Dividend_Date'])
    dividends_history_df.dropna(axis = 0, inplace = True)
    dividends_history_df['Date_Paid'] = pd.to_datetime(dividends_history_df['Date_Paid'])
    dividends_history_df['Date_Announced'] = pd.to_datetime(dividends_history_df['Date_Announced'])
    dividends_history_df['Ex-Dividend_Date'] = pd.to_datetime(dividends_history_df['Ex-Dividend_Date'])
    dividends_history_df.rename(columns = {"Date_Announced":"date"}, inplace = True)
    dividends_history_df.set_index(["date"], inplace = True)
    
    return dividends_history_df

# =============================================================================
# def get_fundamentals(driver):
#     '''
#     get a table with fundamentals data on a page  ZACK
#     '''
#     elements = driver.find_element(By.ID, "DataTables_Table_0")
#     rows = [row.text.encode("utf8") for row in elem.find_elements(By.TAG_NAME, 'tr')]
#     
#     return fundamentals
# =============================================================================

def get_earn_and_dividends(symbol, inference=False):
    '''
    This function launches browser for data load and fetches earnings and dividends data
    '''
    #Start Chrome 
    #driver = webdriver.Chrome(ChromeDriverManager().install()) # deprecated
    # Options to solve DevToolsActivePort issue
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    #driver = webdriver.Chrome('/home/user/drivers/chromedriver')
    #Go to the website
    driver.get(f'https://www.zacks.com/stock/research/{symbol}/earnings-calendar')
    time.sleep(1)
    
    # Handling data privacy pop up
    try:
        elem = driver.find_element(By.XPATH, '//*[text()="Tout rejeter"]')
        elem.click()
    except:
        elem = driver.find_element(By.XPATH, '//*[text()="Reject all"]')
        elem.click()
    except:
        pass
    # #Search stock
    # search_symbol(symbol, driver)
    
    #expand_100_earnings values if training
    if not inference:
        dropdown = driver.find_element(By.NAME, "earnings_announcements_earnings_table_length")
        Select(dropdown).select_by_visible_text("100")
        time.sleep(3)
    
    #Get earnings
    earnings = find_estim_tables(driver)
    #time.sleep(3) # try to comment
    
    #Get dividends
    dividends = find_divid_tables(driver, inference)
    
# =============================================================================
#     #Get fundamentals
#     driver.get(f'https://www.zacks.com/stock/chart/{symbol}/price-book-value')
#     fundamentals = get_fundamentals(driver)
# =============================================================================
    
    #Close browser
    driver.close()
    
    #Transforming Earnings dataframe to a final version
    #Transform string values to numeric
    earnings.replace({"--":np.nan},inplace = True)
    earnings["Reported"], earnings["Estimate"], earnings["Surprise_%"] = pd.to_numeric(earnings.Reported.str.replace("$","")), pd.to_numeric(earnings.Estimate.str.replace("$","")), pd.to_numeric(earnings["Surprise_%"].str.replace("%","").str.replace(",",""))
    earnings["surprise_%"] = earnings["Surprise_%"]/100
    earnings["date_of_report"] = earnings.index
    #getting expected future earnings change
    earnings["future_estimate"] = earnings["Estimate"].shift(1)
    earnings["previous_surprise"] = earnings["surprise_%"].shift(-1)
    earnings = earnings.rename(columns={"Reported" : "eps"})
    earnings["expected_growth"]= (earnings["future_estimate"] - earnings["eps"]) / earnings["eps"]
    earnings["trailing_eps_1Y"] = earnings["eps"].iloc[::-1].rolling(window=4).sum()
    earnings["epsQoQ"] = earnings["eps"] / earnings["eps"].shift(-4) - 1
    earnings = earnings[["eps", "trailing_eps_1Y", "epsQoQ", "surprise_%", "expected_growth", "previous_surprise", "date_of_report"]]
    
    #Transforming Dividends dataframe to a final version
    #STR to value
    dividends.replace({"--":np.nan},inplace = True)
    dividends['Amount'] = pd.to_numeric(dividends['Amount'].str.replace("$",""))
    #get date that we later can use to count days after the announcement
    dividends["date_announced"] = dividends.index
    #Getting dividends trend
    dividends["previous_divid"] = dividends.Amount.shift(-1)
    dividends["dividends_change"] = (dividends['Amount'] - dividends["previous_divid"]) / dividends["previous_divid"]
    dividends = dividends[dividends.dividends_change != 0]
    dividends["prev_div_change"] = dividends.dividends_change.shift(-1)
    dividends = dividends[["Amount", "dividends_change","prev_div_change","date_announced"]]
    
    #earnings = a.copy()
    #dividends = b.copy()
    
    #Match earnings with dates
    #Creating Dates dataframe with all possible dates values
    dates_df=pd.DataFrame()
    dates_df["date"] = pd.date_range(start=earnings.index.min(), end=earnings.index.max())
    #Set dates column as index
    dates_df.set_index(["date"], inplace = True)
    #Creating a dates_earnings dataset where we extrapolate existing quarterly data to daily
    dates_earnings = dates_df.copy()
    dates_earnings = dates_earnings.join(earnings, how = 'left')
    dates_earnings.sort_values(by = 'date', axis = 0, ascending = True, inplace = True)
    dates_earnings.ffill(axis = 0, inplace = True)
    dates_earnings.sort_values(by = 'date', axis = 0, ascending = False, inplace = True)
    dates_earnings["days_after_earn_report"] = dates_earnings.index - dates_earnings["date_of_report"] 
    dates_earnings['days_after_earn_report'] = pd.to_numeric(dates_earnings['days_after_earn_report'].dt.days, downcast='integer')
    dates_earnings.drop(["date_of_report"], axis = 1, inplace = True)
    
    #Match dividends with dates
    #Creating Dates dataframe with all possible dates values
    if dividends.empty:
        dates_dividends = pd.DataFrame(columns = ["Amount", "days_after_divid_report", "dividends_change","prev_div_change"])
        dates_dividends.index.names = ['date']
    else:
        dates_df=pd.DataFrame()
        dates_df["date"] = pd.date_range(start=dividends.index.min(), end=date.today())
        #Set dates column as index
        dates_df.set_index(["date"], inplace = True)
        #Creating a dates_ividends dataset where we extrapolate existing quarterly data to daily
        dates_dividends = dates_df.copy()
        dates_dividends = dates_dividends.join(dividends, how = 'left')
        dates_dividends.sort_values(by = 'date', axis = 0, ascending = True, inplace = True)
        dates_dividends.ffill(axis = 0, inplace = True)
        dates_dividends.sort_values(by = 'date', axis = 0, ascending = False, inplace = True)
        dates_dividends["days_after_divid_report"] = dates_dividends.index - dates_dividends["date_announced"] 
        dates_dividends['days_after_divid_report'] = pd.to_numeric(dates_dividends['days_after_divid_report'].dt.days, downcast='integer')
        dates_dividends.drop(["date_announced"], axis = 1, inplace = True)
    
    return dates_earnings, dates_dividends
    

# =============================================================================
# symbol = "AAPL"
# dates_earnings, dates_dividends = get_earn_and_dividends(symbol)
# #Start Chrome 
# driver = webdriver.Chrome(ChromeDriverManager().install())
# #driver = webdriver.Chrome('/home/user/drivers/chromedriver')
# #Go to the website
# driver.get(f'https://www.zacks.com/stock/research/{symbol}/earnings-calendar')
# earnings = find_estim_tables(driver)
# =============================================================================
