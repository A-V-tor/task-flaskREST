import datetime
from task_flaskrest import db


class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True)
    id_question = db.Column(db.Integer, index=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    question_created_at = db.Column(db.DateTime)
    question = db.Column(db.String(255), unique=True, nullable=False)
    answer = db.Column(db.String(255), unique=True, nullable=False)

    def __str__(self):
        return f'{self.id_question}>'

    def __repr__(self):
        return f'{self.__dict__}'
