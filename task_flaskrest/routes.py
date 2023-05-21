from flask import request, session, current_app as app
from .models import Quiz, db
from .schema import QuestionSchema, QuizSchema
from .functions import save_records, get_questions_data
from flask_apispec import use_kwargs, marshal_with, doc
from task_flaskrest import docs, babel


API_URL_QUIZ = 'https://jservice.io/api/random?count='


@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'ru')


@docs.register
@doc(description='Запрос кол-ва обьектов для сохранения в бд')
@app.route('/quiz', methods=['POST'])
@use_kwargs(QuestionSchema)
@marshal_with(QuizSchema)
def quiz_request(**kwargs):
    """Получение обьектов викторины."""
    questions_num = kwargs['questions_num']

    # пока есть не уникальные обьекты
    while questions_num:

        # получение данных
        response = get_questions_data(API_URL_QUIZ, questions_num)

        # сохранение в бд
        quantity = len(response)

        # возврат числа не уникальных вопросов
        questions_num = save_records(quantity, Quiz, db.session, response)

    return Quiz.query.order_by(Quiz.created_at.desc()).first()
