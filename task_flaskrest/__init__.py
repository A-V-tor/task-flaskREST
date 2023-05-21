from flask import Flask
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_apispec.extension import FlaskApiSpec


db = SQLAlchemy()
docs = FlaskApiSpec()
babel = Babel()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    babel.init_app(app)
    db.init_app(app)

    with app.app_context():
        from . import routes
        from task_flask_music import routes

        db.create_all()

        app.register_blueprint(routes.music)
        from .admin import admin

        docs.init_app(app)

        return app
