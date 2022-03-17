import requests


def get_wall_upload_server(vk_token, vk_group):
    params = {
        'group_id': vk_group
    }
    result = call_vk_api('photos.getWallUploadServer', vk_token, params)
    return result['upload_url']


def save_wall_photo(vk_token, vk_group, photo_properties):
    params = {
        'group_id': vk_group,
        'photo': photo_properties['photo'],
        'server': photo_properties['server'],
        'hash': photo_properties['hash']
    }
    result = call_vk_api('photos.saveWallPhoto', vk_token, params)[0]
    return result['id'], result['owner_id']


def wall_post(vk_token, vk_group, photo_id, owner_id, text):
    params = {
        'owner_id': -vk_group,
        'from_group': 1,
        'message': text,
        'attachments': [f"photo{owner_id}_{photo_id}"]
    }
    result = call_vk_api('wall.post', vk_token, params)
    return result


def call_vk_api(method, access_token, params):
    url = f'https://api.vk.com/method/{method}'
    payload = {
        'access_token': access_token,
        'v': '5.81',
        **params
    }

    response = requests.get(url, params=payload)
    response.raise_for_status()

    data = response.json()

    if data.get('error'):
        raise RuntimeError(f"API Call failed - {data['error']['error_msg']}")

    return data['response']
