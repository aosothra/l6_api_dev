import os
from random import Random

import requests
from dotenv import load_dotenv

import vk_basic as vk
from xkcd_fetcher import get_xkcd_count, get_xkcd_by_index


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
    upload_url = vk.get_wall_upload_server(vk_token, vk_group)

    photo_properties = upload_image(upload_url)

    photo_id, owner_id = vk.save_wall_photo(vk_token, vk_group, photo_properties)

    vk.wall_post(vk_token, vk_group, photo_id, owner_id, caption)


def main():
    load_dotenv()
    vk_token = os.getenv('VK_ACCESS_TOKEN')
    vk_group = int(os.getenv('VK_GROUP_ID'))

    comic_count = get_xkcd_count()
    comic_index = Random().randint(100, comic_count)

    comic_url, comic_caption = get_xkcd_by_index(comic_index)
    download_image(comic_url)

    try:
        post_image_to_vk(vk_token, vk_group, comic_caption)
    finally:
        os.remove('xkcd.png')


if __name__ == '__main__':
    main()
