import requests
from requests.auth import HTTPBasicAuth


# définition de l'adresse de l'API
api_address = "trading_api"  # os.environ.get('API_ADDRESS')
# port de l'API
api_port = "8000"  # os.environ.get('API_PORT')


def test_authentification():
    tested_users = [{'username': 'alice', 'password': 'wonderland'},
                    {'username': 'bob', 'password': 'builder'},
                    {'username': 'clementine', 'password': 'mandarine'}
                    ]

    expected_results = [200, 200, 403]

    r = []
    for tested_user in tested_users:
        r_ = requests.get(
            url='http://{address}:{port}/permissions'.format(address=api_address, port=api_port),
            auth=HTTPBasicAuth(tested_user['username'], tested_user['password']))
        r.append(r_)

    for i, r_ in enumerate(r):
        # statut de la requête
        status_code = r_.status_code

        # test
        assert status_code == expected_results[i]