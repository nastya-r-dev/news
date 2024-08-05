from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from webapp.user.models import User
from webapp.db import db
from webapp.user.forms import LoginForm, RegisterForm

blueprint = Blueprint('admin', __name__,
                      url_prefix='/admin')  # __name__ - наполняет блюпринт содержимым данного файла, user - название


@blueprint.route('/admin_panel')
@login_required
def admin_index():
    if current_user.is_admin:
        users = User.query.all()
        return render_template(
            'admin_panel.html',
            users=users
        )
    else:
        return 'свяжитесь с администратором для получения доступа'


@blueprint.route('/change_right_process', methods=['POST'])
def change_right_process():
    res = request.form
    users = User.query.filter(User.id.in_(res)).all()
    for user in users:
        user.status = res[str(user.id)]
    db.session.commit()
    return redirect(url_for('admin.admin_index'))
