from flask import Flask
from flask_login import LoginManager, current_user, login_required
from flask_migrate import Migrate
from webapp.db import db
from webapp.news.views import blueprint as news_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint
from webapp.admin.views import blueprint as admin_blueprint
from webapp.news.utils.weather import get_weather_by_city
from transliterate import translit


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_pyfile('config.py')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app) # подключение к приложению
    login_manager.login_view = 'user.login'
    login_manager.login_message = 'Доступ только для авторизованных!'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.register_blueprint(news_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)

    @app.context_processor
    def get_weather():
        # city = current_user.city if current_user.is_authenticated else 'Москва'
        city = 'Москва'
        weather = get_weather_by_city(translit(city, language_code='ru', reversed=True))
        return dict(city=city, weather=weather)

    return app



