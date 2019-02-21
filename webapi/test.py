import requests


PASSWORD = '*****'
COOKIES = None
REQUEST_ID = 0


def send_request(method, params=None):
    global REQUEST_ID
    global COOKIES
    REQUEST_ID += 1

    response = requests.post(
        'http://localhost:8112/json',
        json={'id': REQUEST_ID, 'method': method, 'params': params or []},
        cookies=COOKIES)

    data = response.json()

    error = data.get('error')

    if error:
        raise Exception('API response: %s' % error['message'])

    COOKIES = response.cookies

    return data['result']


assert send_request('auth.login', [PASSWORD]), 'Unable to log in. Check password.'

version_number = send_request('webapi.get_api_version')
assert version_number, 'No WebAPI version available. Check plugin is enabled.'
print('WebAPI version: %s' % version_number)

print('Success')
