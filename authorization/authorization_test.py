import os
import requests

# définition de l'adresse de l'API
api_address = "127.0.0.1" # os.environ.get('API_ADDRESS')
# port de l'API
api_port = "8000" # os.environ.get('API_PORT')
# version du model

response = []


users = [
    {'username': 'alice', 'password': 'wonderland', 'right': 'market only'},
    {'username': 'bob', 'password': 'builder', 'right': 'market only'},
    {'username': 'damien', 'password': 'vannetzel', 'right': 'admin'},
]

for user in users:
    # requête
    r = requests.get(
        url='http://{address}:{port}/_admin_get'.format(address=api_address, port=api_port),
        params= user
    )
    response.append([user['username'], user['right'], r])

output = '''
============================
    Authorization test
============================

request done at "/_admin_get"
username = {username}
rights = {right}
expected result = 200
actual restult = {status_code}

==>  {test_status}

'''

for combo in response:
    username = combo[0]
    right = combo[1]
    r = combo[2]

    # statut de la requête
    status_code = r.status_code

    # affichage des résultats
    if status_code == 200:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'
    print(output.format(status_code=status_code, test_status=test_status, username= username, right= right))

    # impression dans un fichier
    if os.environ.get('LOG') == "1":
        with open('/logs/api_test.log', 'a') as file:
            file.write(output.format(status_code=status_code, test_status=test_status, username= username, right= right))
