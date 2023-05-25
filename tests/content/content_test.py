import os
import requests
import json

# définition de l'adresse de l'API
api_address = "127.0.0.1"  # os.environ.get('API_ADDRESS')
# port de l'API
api_port = "8000"  # os.environ.get('API_PORT')

response = []

users = [
    {'username': 'alice', 'password': 'wonderland', 'right': 'market'},
    {'username': 'bob', 'password': 'builder', 'right': 'fundamental'},
    {'username': 'damien', 'password': 'vannetzel', 'right': 'admin'},
]

queries = [
    {'tickers': ['AAPL', 'GOOG'], 'time_horizon': '1y', 'trading_type': 'long'},
    {'tickers': ['TSLA', 'FB'], 'time_horizon': '6m', 'trading_type': 'short'}
]

for user in users:
    for query in queries:
        # requête
        r = requests.post(
            url='http://{address}:{port}/predictions'.format(address=api_address, port=api_port),
            json=query,
            auth=(user['username'], user['password'])
        )
        response.append([user['username'], query, r.json(), r])

output = '''
============================
    Content test
============================

request done at "/predictions"
username = {username}
Query = {query}
expected result = 200
actual result = {status_code}

==>  {test_status}
Response JSON = {response_json}

'''
for combo in response:
    username = combo[0]
    query = combo[1]
    response_json = json.dumps(combo[2], indent=4)
    r = combo[3]

    # statut de la requête
    status_code = r.status_code

    # affichage des résultats
    if status_code == 200:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'
    print(output.format(status_code=status_code, test_status=test_status, response_json=response_json, query=query, username=username))

    # impression dans un fichier
    if os.environ.get('LOG') == "1":
        with open('/logs/api_test.log', 'a') as file:
            file.write(output.format(status_code=status_code, test_status=test_status, response_json=response_json, query=query, username=username))