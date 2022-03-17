import requests


def call_vk_api(method, access_token, params):
    url = f'https://api.vk.com/method/{method}'
    params['access_token'] = access_token
    params['v'] = '5.81'

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    if data.get('error'):
        raise RuntimeError(f"API Call failed - {data['error']['error_msg']}")

    return data['response']
