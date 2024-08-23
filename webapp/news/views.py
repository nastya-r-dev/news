from flask import Blueprint, abort, render_template, request, redirect, url_for
from webapp.news.models import New
from webapp.user.models import Comment, User
from webapp.db import db

blueprint = Blueprint('news', __name__)

@blueprint.route('/')
def root():
    # Перенаправление на первую страницу
    return redirect(url_for('news.index', page=1))

@blueprint.route('/<int:page>')
def index(page):
    per_page = 9
    title = 'TodayNews'
    news = New.query.order_by(New.date.desc())
    all_news = news.paginate(page=page, per_page=per_page, error_out=False)
    actual_news = list(news)[:4]
    return render_template(
        'index.html',
        all_news=all_news,
        actual_news=actual_news,
        title=title
    )


@blueprint.route('/news/<int:news_id>')
def single_news(news_id):
    my_news = New.query.filter(New.id == news_id).first()
    comments = db.session.query(Comment, User).join(User, Comment.user_id == User.id).all()
    number = len(comments)
    if not my_news:
        abort(404)
    return render_template(
        'single_news.html',
        title=my_news.title,
        news=my_news,
        comments=comments,
        number=number
    )


@blueprint.route('/save_comment_process', methods=['POST'])
def save_comment_process():
    res = request.form
    news_id = res['news_id']
    comment = Comment(text=res['text'], news_id=news_id, user_id=res['user_id'])
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('news.single_news', news_id=news_id))
