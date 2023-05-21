def test_quiz_num(client):
    # отправка запроса с данными
    res = client.post('/quiz', json={'questions_num': 3})
    assert res.get_json()['answer']


def test_quiz_num_not_data(client):
    # отправка запроса без данных
    res = client.post('/quiz')
    assert res.status_code == 422
