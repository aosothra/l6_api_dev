import requests


def get_xkcd_count():
    url = 'https://xkcd.com/info.0.json'

    response = requests.get(url)
    response.raise_for_status()

    json_data = response.json()
    return json_data['num']


def get_xkcd_by_index(i):
    url = f'https://xkcd.com/{i}/info.0.json'

    response = requests.get(url)
    response.raise_for_status()

    json_data = response.json()
    return json_data['img'], json_data['alt']
