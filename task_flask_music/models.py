import uuid
import secrets
from task_flaskrest import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = 'myuser'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    token = db.Column(
        db.String(255), default=uuid.UUID(bytes=secrets.token_bytes(16))
    )
    musics = relationship('Audio', cascade='all, delete')

    def __str__(self):
        return self.name


class Audio(db.Model):
    __tablename__ = 'audio'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    token_audio = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, ForeignKey('myuser.id'))

    def __str__(self):
        return self.name
