import requests
from requests.auth import HTTPBasicAuth
import time

time.sleep(20)

def test_predict():
    # définition de l'adresse de l'API
    api_address = "trading_api"  # os.environ.get('API_ADDRESS')
    # port de l'API
    api_port = "8000"  # os.environ.get('API_PORT')
    tested_user = {'username': 'julien', 'password': 'chaplet'}
    
    r_ = requests.post(
        url='http://{address}:{port}/predictions'.format(address=api_address, port=api_port),
        auth=HTTPBasicAuth(tested_user['username'], tested_user['password']),
        json = {
            'tickers': ["CSCO", "TSLA"],
            'time_horizon': "1w",
            'trading_type': "market_and_fundamental"
        })
    
    status_code = r_.status_code
    
    assert status_code == 200

