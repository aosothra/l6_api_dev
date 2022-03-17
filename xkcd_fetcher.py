import requests


def get_xkcd_count():
    url = 'https://xkcd.com/info.0.json'

    response = requests.get(url)
    response.raise_for_status()

    comic_data = response.json()
    return comic_data['num']


def get_xkcd_by_index(index):
    url = f'https://xkcd.com/{index}/info.0.json'

    response = requests.get(url)
    response.raise_for_status()

    comic_data = response.json()
    return comic_data['img'], comic_data['alt']
