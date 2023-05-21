from flask import current_app as app
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from task_flaskrest import db
from .models import Quiz
from task_flask_music.models import User, Audio


class MyAdminIndexView(AdminIndexView):
    @expose('/admin')
    def default_view(self):
        print(self.__dict__)
        return self.render('admin/index.html')

    def is_accessible(self):
        try:
            return True
        except Exception:
            pass


admin = Admin(
    app,
    name='',
    static_url_path='admin/static/',
    template_mode='bootstrap3',
    index_view=MyAdminIndexView(
        name='Админка',
        menu_icon_type='glyph',
        menu_icon_value='glyphicon-send',
    ),
)


class QuizAdminView(ModelView):
    column_display_pk = True
    can_view_details = True
    column_descriptions = dict(
        created_at='Время создания записи в базе данных.',
        question_created_at='Время создания вопроса на ресурсе викторины.',
    )
    column_labels = dict(
        id_question='ID вопроса',
        created_at='Создание записи',
        question_created_at='Создание вопроса',
        question='Вопрос',
        answer='Ответ',
    )
    create_modal = True
    edit_modal = True


class UserAdminView(ModelView):
    column_display_pk = True
    can_view_details = True
    column_list = ['id', 'name', 'token', 'musics']
    column_labels = dict(
        name='Логин',
        token='Токен',
    )
    create_modal = True
    edit_modal = True


class AudioAdminView(ModelView):
    column_display_pk = True
    can_view_details = True
    column_list = ['id', 'name', 'token_audio', 'owner_id']
    column_labels = dict(
        name='Имя записи',
        token_audio='Токен',
        owner_id='Пользователь',
    )
    create_modal = True
    edit_modal = True


admin.add_views(
    QuizAdminView(
        Quiz,
        db.session,
        name='Викторина',
        menu_icon_type='glyph',
        menu_icon_value='glyphicon-question-sign',
    )
)

admin.add_views(
    UserAdminView(
        User,
        db.session,
        name='Пользователи',
        menu_icon_type='glyph',
        menu_icon_value='glyphicon-user',
    )
)

admin.add_views(
    AudioAdminView(
        Audio,
        db.session,
        name='Мелодии',
        menu_icon_type='glyph',
        menu_icon_value='glyphicon-music',
    )
)
