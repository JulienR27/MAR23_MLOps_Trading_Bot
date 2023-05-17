import os
import requests

# définition de l'adresse de l'API
api_address = os.environ.get('API_ADDRESS')

# # port de l'API
api_port = os.environ.get('API_PORT')


users = [
    {'username': 'alice', 'password': 'wonderland'},
    {'username': 'bob', 'password': 'builder'},
    {'username': 'clementine', 'password': 'mandarine'}
]
response = []

for user in users:
    # requête
    r = requests.get(
        url='http://{address}:{port}/permissions'.format(address=api_address, port=api_port),
        params= user
    )
    response.append([user['username'], r])

output = '''
============================
    Authentication test
============================

request done at "/permissions"
username = {username}
expected result = 200
actual restult = {status_code}

==>  {test_status}
'''


# statut de la requête
for combo in response:
    username = combo[0]
    r = combo[1]

    status_code = r.status_code

    # affichage des résultats
    if status_code == 200:
        test_status = 'SUCCESS'
    else:
        test_status = 'FAILURE'
    print(output.format(status_code=status_code, test_status=test_status, username= username))

    # impression dans un fichier
    if os.environ.get('LOG') == "1":
        with open('/logs/api_test.log', 'a') as file:
            file.write(output.format(status_code=status_code, test_status=test_status, username= username))
