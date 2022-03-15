import os
from random import Random

import requests
from dotenv import load_dotenv

from xkcd_fetcher import get_xkcd_count, get_xkcd_by_index
from vk_basic import call_vk_api


def download_image(url):
    response = requests.get(url)
    response.raise_for_status()

    with open('xkcd.png', 'wb') as file:
        file.write(response.content)


def upload_image(url):
    with open('xkcd.png', 'rb') as file:
        files = {
            'photo': file
        }

        response = requests.post(url, files=files)
        response.raise_for_status()

        return response.json()


def post_image_to_vk(vk_token, vk_group, caption):
    params = {
        'group_id': vk_group
    }
    result = call_vk_api('photos.getWallUploadServer', vk_token, params)
    upload_url = result['upload_url']

    result = upload_image(upload_url)

    params = {
        'group_id': vk_group,
        'photo': result['photo'],
        'server': result['server'],
        'hash': result['hash']
    }
    result = call_vk_api('photos.saveWallPhoto', vk_token, params)[0]

    params = {
        'owner_id': -vk_group,
        'from_group': 1,
        'message': caption,
        'attachments': [f"photo{result['owner_id']}_{result['id']}"]
    }
    result = call_vk_api('wall.post', vk_token, params)


def main():
    load_dotenv()
    vk_token = os.getenv('VK_ACCESS_TOKEN')
    vk_group = int(os.getenv('VK_GROUP_ID'))

    count = get_xkcd_count()
    index = Random().randint(100, count)

    comic_url, comic_caption = get_xkcd_by_index(index)
    download_image(comic_url)

    try:
        post_image_to_vk(vk_token, vk_group, comic_caption)
    finally:
        os.remove('xkcd.png')


if __name__ == '__main__':
    main()
