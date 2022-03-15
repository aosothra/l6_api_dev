import requests


def call_vk_api(method, access_token, params):
    url = f'https://api.vk.com/method/{method}'
    params['access_token'] = access_token
    params['v'] = '5.81'

    response = requests.get(url, params=params)
    response.raise_for_status()

    json_data = response.json()

    if json_data.get('error'):
        raise RuntimeError(f"API Call failed - {json_data['error']['error_msg']}")

    return json_data['response']
