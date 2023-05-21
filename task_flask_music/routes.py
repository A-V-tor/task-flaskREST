import os
import uuid
import secrets
from flask import Blueprint, request, send_file
from flask_apispec import use_kwargs, marshal_with, doc
from task_flaskrest import docs
from pydub import AudioSegment
from .models import User, Audio, db
from .schema import UserShcema, TokenShcema


BASEDIR_AUDIO = os.path.join(os.getcwd(), 'task_flask_music/audio')
HOST = 'http://localhost:5000/'


music = Blueprint(
    'music',
    '__name__',
)


@doc(description='Добавление пользователя')
@music.route('/user', methods=['POST'])
@use_kwargs(UserShcema)
@marshal_with(TokenShcema)
def create_user(**kwargs):
    name = kwargs['name']
    try:
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
    except Exception:
        return {'message': 'User already exists'}, 409
    return user


@music.route('/music-add', methods=['POST'])
def add_music():
    try:
        audio = request.files['audio']
    except Exception:
        return {'error': 'Missing required fields'}, 400

    token = request.form.get('token')
    user_id = request.form.get('user_id')
    if not user_id or not token:
        return {'error': 'Missing required fields'}, 400

    # проверка формата
    check_format = audio.filename[-3:]
    if check_format != 'wav':
        return {'error': 'wrong format'}, 400

    # Проверка валидности токена доступа
    user = User.query.filter_by(id=user_id, token=token).first()
    if not user:
        return {'error': 'Invalid access token or non-existent user'}, 401

    # сохранение формата wav
    audio_path = BASEDIR_AUDIO + f'/{audio.filename}'
    audio.save(audio_path)

    # Преобразование аудиозаписи в формат mp3
    audio_converter = AudioSegment.from_wav(audio_path)
    os.remove(audio_path)
    audio_converter.export(
        f'{BASEDIR_AUDIO}/' + audio.filename[:-4] + '.mp3', format='mp3'
    )

    # запись в владельца в бд
    try:
        token_audio = uuid.UUID(bytes=secrets.token_bytes(16))
        new_audio = Audio(
            token_audio=token_audio,
            name=audio.filename[:-4] + '.mp3',
            owner_id=user.id,
        )
        db.session.add(new_audio)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return {'error': 'Internal Server Error'}, 500

    url = f'{HOST}record?id={token_audio}&user={user.id}'
    return {'url': url}, 200


@music.route('/record', methods=['GET'])
def get_record():
    record_id = request.args.get('id')
    user_id = request.args.get('user')

    # Проверяем, что оба параметра присутствуют
    if not record_id or not user_id:
        return {'error': 'Missing required fields'}, 400

    # проверка идентификатора и пользователя
    audio = Audio.query.filter_by(
        token_audio=record_id, owner_id=user_id
    ).first()
    if not audio:
        return {'error': 'Wrong data was given'}, 400

    file_path = os.path.join(BASEDIR_AUDIO, audio.name)
    return send_file(file_path, as_attachment=True)


docs.register(create_user, blueprint='music')
