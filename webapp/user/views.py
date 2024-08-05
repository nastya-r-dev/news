from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from webapp.user.models import User
from webapp.db import db
from webapp.user.forms import LoginForm, RegisterForm

blueprint = Blueprint('user', __name__,
                      url_prefix='/user')  # __name__ - наполняет блюпринт содержимым данного файла, user - название


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = 'Авторизация'
    form = LoginForm()
    referrer = request.referrer
    return render_template(
        'login.html',
        form=form,
        title=title,
        referrer=referrer
    )


@blueprint.route('/login-process', methods=['POST'])
def login_process():
    form = LoginForm()
    # form = LoginForm(user)
    user = User.query.filter(User.login == form.login.data).first()
    if user and user.check_password(form.password.data):
        login_user(user, remember=form.remember_me.data)
        flash('С возвращением!')
        return redirect(request.form["url"])
    flash('Проверьте данные!')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    referrer = request.referrer
    return redirect(referrer)


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    form = RegisterForm()
    return render_template(
        'register.html',
        form=form,
    )


@blueprint.route('/register-process', methods=['POST'])
def register_process():
    form = RegisterForm()
    if form.validate_on_submit():
        # form = RegisterForm(user)
        # RegisterForm(User)
        # User(form)

        new_user = User(
            login=form.login.data,
            first_name=form.first_name.data,
            second_name=form.second_name.data,
            middle_name=form.middle_name.data,
            birthday=form.birthday.data,
            city=form.city.data,
            gender=form.gender.data,
            email=form.email.data,
            status='user'

        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрированы!')
        return redirect(url_for('user.login'))
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{error}')
    # if User.query.filter(User.login == form.login.data).count():
    #     flash('Логин занят!')
    return redirect(url_for('user.register'))
