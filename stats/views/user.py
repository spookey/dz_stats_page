from logging import getLogger

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user
from werkzeug.http import parse_authorization_header

from stats.forms.user import LoginForm
from stats.models.user import User
from stats.start.extensions import LOGIN_MANAGER

BLUEPRINT_USER = Blueprint('user', __name__)
LOG = getLogger(__name__)


@LOGIN_MANAGER.user_loader
def user_loader(prime):
    return User.by_prime(prime)


@LOGIN_MANAGER.request_loader
def request_loader(req):
    auth = parse_authorization_header(req.headers.get('authorization'))
    if auth is not None:
        if auth.username is not None and auth.password is not None:
            user = User.by_username(auth.username)
            if user is not None and user.check_password(auth.password):
                return user
    return None


@BLUEPRINT_USER.route('/logout')
@login_required
def logout():
    LOG.info('logout for user "%s"', current_user.username)
    logout_user()
    flash('See you soon!', 'dark')
    return redirect(url_for('main.index'))


@BLUEPRINT_USER.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        if form.action():
            flash('Welcome back!', 'dark')
            return redirect(
                request.args.get('next') or url_for('main.index')
            )

    return render_template(
        'user/login.html',
        title='Tickets, please!',
        form=form
    )