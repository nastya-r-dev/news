from getpass import getpass
from webapp import create_app
from webapp.db import db
from webapp.user.models import User


app = create_app()

with app.app_context():
    login = input('Введите логин: ')

    if User.query.filter(User.login == login).count():
        print('Имя занято!')
        exit()

    password = getpass('Пароль: ')
    password2 = getpass('Повторите пароль: ')
    if password == password2:
        new_user = User(
            login=login,
            status='admin',
            )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
