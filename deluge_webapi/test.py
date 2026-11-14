import requests
from os import environ

PASSWORD = environ.get('WEBAPI_PASSWORD', '*****')
COOKIES = None
REQUEST_ID = 0


def send_request(method, params=None):
    global REQUEST_ID
    global COOKIES
    REQUEST_ID += 1

    try:

        response = requests.post(
            'http://localhost:8112/json',
            json={'id': REQUEST_ID, 'method': method, 'params': params or []},
            cookies=COOKIES)

    except requests.exceptions.ConnectionError:
        raise Exception('WebUI seems to be unavailable. Run deluge-web or enable WebUI plugin using other thin client.')

    data = response.json()

    error = data.get('error')

    if error:
        msg = error['message']

        if msg == 'Unknown method':
            msg += '. Check WebAPI is enabled.'

        raise Exception('API response: %s' % msg)

    COOKIES = response.cookies

    return data['result']


assert send_request('auth.login', [PASSWORD]), 'Unable to log in. Check password.'

version_number = send_request('webapi.get_api_version')
assert version_number

print('WebAPI version: %s' % version_number)

print('Success')
