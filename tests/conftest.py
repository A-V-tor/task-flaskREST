import pytest
from task_flaskrest import create_app, db
from task_flask_music.models import User


@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config.update(
        {
            'TESTING': True,
        }
    )
    with app.app_context():
        db.metadata.drop_all(bind=db.engine)
        db.metadata.create_all(bind=db.engine)

        yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def user():
    user = User(
        name='test-user',
    )
    db.session.add(user)
    db.session.commit()
    return user
