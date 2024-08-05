from webapp.db import db


class New(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False, unique=True)
    date = db.Column(db.DateTime)
    text = db.Column(db.Text)
    img = db.Column(db.Text)