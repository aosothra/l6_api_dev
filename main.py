import os
from random import Random

import requests
from dotenv import load_dotenv


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


def download_image(url):
    response = requests.get(url)
    response.raise_for_status()

    with open('xkcd.png', 'wb') as file:
        file.write(response.content)


def upload_image(url):
    with open('xkcd.png', 'rb') as file:
        files={
            'photo': file
        }

        response = requests.post(url, files=files)
        response.raise_for_status()

        return response.json()


def call_vk_api(method, access_token, params):
    url = f'https://api.vk.com/method/{method}'
    params['access_token'] = access_token
    params['v'] = '5.81'


    response = requests.get(url, params=params)
    response.raise_for_status()

    json_data = response.json()

    if json_data.get('error'):
        print(json_data['error'])
        raise RuntimeError('API Call failed.')

    return json_data['response']


def main():
    load_dotenv()
    vk_token = os.getenv('VK_ACCESS_TOKEN')
    vk_group = int(os.getenv('VK_GROUP_ID'))

    method = 'photos.getWallUploadServer'
    params = {
        'group_id': vk_group
    }
    result = call_vk_api(method, vk_token, params)
    upload_url = result['upload_url']

    result = upload_image(upload_url)

    method = 'photos.saveWallPhoto'
    params = {
        'group_id': vk_group,
        'photo': result['photo'],
        'server': result['server'],
        'hash': result['hash']
    }
    result = call_vk_api(method, vk_token, params)[0]
    print(result)

    method = 'wall.post'
    params = {
        'owner_id': -vk_group,
        'from_group': 1,
        'message': 'Test',
        'attachments': [f"photo{result['owner_id']}_{result['id']}"]
    }
    result = call_vk_api(method, vk_token, params)
    print(result)
    # count = get_xkcd_count()
    # index = Random().randint(100, count)

    # url, alt = get_xkcd_by_index(index)
    # download_image(url)
    # print(alt)

if __name__ == '__main__':
    main()