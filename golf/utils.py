from flask import request
from flask_login import login_user
from werkzeug.security import check_password_hash

from golf.models import db, User, Event


def login_custom_func():
    account_number = request.form.get('member-login-number')
    password = request.form.get('member-login-password')
    user = User.query.filter_by(account_number=account_number).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
    else:
        return user


def get_events():
    events = Event.query.order_by(Event.date).all()
    return events
