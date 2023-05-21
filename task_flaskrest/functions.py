import requests


def get_questions_data(url, num):
    """Запрос данных викторины.

    Args:
        url: string ссылка
        num: int кол-во нужных вопросов

    Returns:
        dict with data
    """
    return requests.get(f'{url}{num}').json()


def save_records(quantity, model, session_db, data):
    """Сохранение данных в бд.
    Args:
        quantity: int кол-во нужных вопросов
        model: Model object модель бд
        session_db: session database сессия бд
        data: dict словарь с данными

    Returns:
        miss_question: int or None кол-во не уникальных

        обьетов для повторного запроса
    """
    # счетчик повторяющихся вопросов
    miss_question = 0
    try:
        for i in range(quantity):
            question_id = int(data[i]['id'])
            check = model.query.filter_by(id_question=question_id).first()

            # если вопрос уже есть в бд увеличиваем счетчик
            if check:
                miss_question += 1
                continue

            question = data[i]['question']
            answer = data[i]['answer']
            created_at = data[i]['created_at']
            quiz = model(
                id_question=question_id,
                question_created_at=created_at,
                question=question,
                answer=answer,
            )
            session_db.add(quiz)
        session_db.commit()
    except Exception:
        session_db.rollback()
    finally:
        return miss_question
