from celery import Celery
from celery.schedules import crontab
from webapp import create_app
from webapp.news.utils.python_news import get_python_news


celery_app = Celery('tasks', broker='redis://localhost:6379/0')
flask_app = create_app()


@celery_app.task
def python_news():
    with flask_app.app_context():
        get_python_news()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute="*/1"), python_news)



