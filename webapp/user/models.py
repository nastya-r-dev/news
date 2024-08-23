from flask_login import UserMixin
from webapp.db import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String, nullable=False, unique=True, index=True)
    first_name = db.Column(db.String)
    second_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    birthday = db.Column(db.DateTime)
    city = db.Column(db.String)
    gender = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default='user')

    @property
    def is_admin(self):
        return self.status == 'admin'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    news_id = db.Column(
        db.Integer,
        db.ForeignKey('new.id', ondelete='CASCADE'),
        index=True,
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        index=True,
    )
