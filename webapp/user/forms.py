from flask_wtf import FlaskForm
from webapp.user.models import User
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from webapp.user.utils.cities import get_russian_cities
import re


class LoginForm(FlaskForm):
    login = StringField(
        'Имя пользователя',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
        )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
        )
    remember_me = BooleanField('Запомнить меня', render_kw={'class': 'form-check-input'}, default=True)
    submit = SubmitField('Войти', render_kw={'class': 'btn btn-primary'})


class RegisterForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()], render_kw={'class': 'form-control'})
    first_name = StringField('Имя', validators=[DataRequired()], render_kw={'class': 'form-control'})
    second_name = StringField('Фамилия', validators=[DataRequired()], render_kw={'class': 'form-control'})
    middle_name = StringField('Отчество', render_kw={'class': 'form-control'})
    birthday = DateField("Дата Рождения",  render_kw={'class': 'form-control'})
    city = StringField('Город', validators=[DataRequired()], render_kw={'class': 'form-control'})
    gender = SelectField('Пол', choices=[('f', 'Женский'), ('m', 'Мужской')], render_kw={'class': 'form-control'})
    email = StringField("Email ", validators=[Email(), DataRequired()], render_kw={'class': 'form-control'})
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
        )
    password2 = PasswordField(
        'Повторите пароль',
        validators=[DataRequired(), EqualTo('password', 'Пароли не совпадают')],
        render_kw={'class': 'form-control'},
        )

    submit = SubmitField('Зарегистрироваться', render_kw={'class': 'btn btn-primary'})

    def validate_login(self, login):
        users_counter = User.query.filter(User.login == self.login.data).count()
        if users_counter:
            raise ValidationError('Логин занят')

    def validate_email(self, email):
        emails_counter = User.query.filter(User.email == self.email.data).count()
        if emails_counter:
            raise ValidationError('Такая почта уже зарегистрирована')

    def validate_password(self, password):
        if len(self.password.data) < 8:
            raise ValidationError('Пароль должен содержать не менее 8 символов')
        elif re.search('[0-9]', self.password.data) is None:
            raise ValidationError('Пароль должен содержать хотя бы 1 цифру')
        elif re.search('[A-Z]', self.password.data) is None:
            raise ValidationError('Пароль должен содержать хотя бы 1 заглавную букву')
        elif re.search('[a-z]', self.password.data) is None:
            raise ValidationError('Пароль должен содержать хотя бы 1 строчную букву')

    def validate_city(self, city):
        if self.city.data not in get_russian_cities():
            raise ValidationError('Такого города не существует')

