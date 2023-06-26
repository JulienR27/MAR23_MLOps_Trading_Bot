import requests
from requests.auth import HTTPBasicAuth
import time

time.sleep(20)

def test_authentification():
    # définition de l'adresse de l'API
    api_address = "trading_api"  # os.environ.get('API_ADDRESS')
    # port de l'API
    api_port = "8000"  # os.environ.get('API_PORT')
    tested_users = [{'username': 'alice', 'password': 'wonderland'},
                    {'username': 'bob', 'password': 'builder'},
                    {'username': 'clementine', 'password': 'mandarine'}
                    ]

    expected_results = [200, 200, 401]

    r = []
    for tested_user in tested_users:
        r_ = requests.get(
            url='http://{address}:{port}/'.format(address=api_address, port=api_port),
            auth=HTTPBasicAuth(tested_user['username'], tested_user['password']))
        r.append(r_)

    for i, r_ in enumerate(r):
        # statut de la requête
        status_code = r_.status_code

        # test
        assert status_code == expected_results[i]

def test_authorization():
    # définition de l'adresse de l'API
    api_address = "trading_api"  # os.environ.get('API_ADDRESS')
    # port de l'API
    api_port = "8000"  # os.environ.get('API_PORT')
    tested_users = [{'username': 'alice', 'password': 'wonderland', 'trading_type': 'fundamental'},
                    {'username': 'bob', 'password': 'builder', 'trading_type': 'market'},
                    #{'username': 'julien', 'password': 'chaplet'}
                    ]

    expected_results = [401, 401]

    r = []
    for tested_user in tested_users:
        r_ = requests.post(
            url='http://{address}:{port}/predictions'.format(address=api_address, port=api_port),
            auth=HTTPBasicAuth(tested_user['username'], tested_user['password']),
            json = {
                'tickers': ["AAPL"],
                'time_horizon': "1m",
                'trading_type': tested_user["trading_type"]
            })
        r.append(r_)

    for i, r_ in enumerate(r):
        # statut de la requête
        status_code = r_.status_code

        # test
        assert status_code == expected_results[i]

if __name__== "__main__":
    test_authentification()
    test_authorization()


# # définition de l'adresse de l'API
# api_address = "trading_api"  # os.environ.get('API_ADDRESS')
# # port de l'API
# api_port = "8000"  # os.environ.get('API_PORT')
# tested_users = [{'username': 'alice', 'password': 'wonderland'},
#                 {'username': 'bob', 'password': 'builder'},
#                 {'username': 'clementine', 'password': 'mandarine'}
#                 ]

# expected_results = [200, 200, 401]

# r = []
# for tested_user in tested_users:
#     r_ = requests.get(
#         url='http://{address}:{port}/'.format(address=api_address, port=api_port),
#         auth=HTTPBasicAuth(tested_user['username'], tested_user['password']))
#     r.append(r_)


# output = '''
# ============================
#     Authentication test
# ============================

# request done at "/permissions"
# | username="{username}"
# | password="{password}"

# expected result = {expected_result}
# actual result = {status_code}

# ==>  {test_status}

# '''

# for i, r_ in enumerate(r):
#     # statut de la requête
#     status_code = r_.status_code

#     # affichage des résultats
#     if status_code == expected_results[i]:
#         test_status = 'SUCCESS'
#     else:
#         test_status = 'FAILURE'
#     output_temp = output.format(username=tested_users[i]["username"], password=tested_users[i]["password"], expected_result=expected_results[i], status_code=status_code, test_status=test_status)
#     print(output_temp)

#     # impression dans un fichier
#     if os.environ.get('LOG') == '1':
#         with open('log/api_test.log', 'a') as file:
#             file.write(output_temp)