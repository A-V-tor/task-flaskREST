import os
from config import basedir


def test_create_user_not_data(client):
    # отправка запроса без данных
    res = client.post('/user')
    assert res.status_code == 422


def test_create_user(client):
    # проверка создания новго юзера
    res = client.post('/user', json={'name': 'user'})
    assert res.status_code == 200


def test_add_music(client, user):
    # проверка отправки формата wav и получение mp3
    path = os.path.join(basedir, 'someaudio.wav')
    file = open(path, 'rb')
    data = {
        'audio': (file, 'someaudio.wav'),
        'token': user.token,
        'user_id': user.id,
    }

    res = client.post(
        '/music-add',
        data=data,
        buffered=True,
        content_type='multipart/form-data',
    )
    file.close()
    assert 'http://' in res.get_json()['url']
    newres = client.get(res.get_json()['url'])
    assert newres.status_code == 200


def test_add_music_chunk(client, user):
    # проверка отправки части данных
    path = os.path.join(basedir, 'someaudio.wav')
    file = open(path, 'rb')
    data = {
        'audio': (file, 'someaudio.wav'),
        'user_id': user.id,
    }

    res = client.post(
        '/music-add',
        data=data,
        buffered=True,
        content_type='multipart/form-data',
    )
    file.close()
    assert 'Missing required fields' in res.get_json()['error']


def test_add_music_bad_user(client, user):
    # проверка данных с несуществующим юзером
    path = os.path.join(basedir, 'someaudio.wav')
    file = open(path, 'rb')
    data = {
        'audio': (file, 'someaudio.wav'),
        'token': user.token,
        'user_id': '3',
    }

    res = client.post(
        '/music-add',
        data=data,
        buffered=True,
        content_type='multipart/form-data',
    )
    file.close()
    assert (
        'Invalid access token or non-existent user' in res.get_json()['error']
    )
