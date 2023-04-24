from flask import request
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash

from golf.models import db, User, Event, Mail, Appeal


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


def add_mail():
    user_mail = request.form['email']
    if user_mail:
        mail_in_db = Mail.query.filter_by(mail=user_mail).all()
        if not mail_in_db:
            mail_obj = Mail(mail=user_mail)
            db.session.add(mail_obj)
            db.session.commit()
        return True


def check_is_join_req():
    is_join_req = False
    if request.path == '/join_request/':
        is_join_req = True

    return is_join_req


def data_for_appeal_from_auth_user():
    data = dict()
    data['name'] = current_user.account_number
    data['mail_id'] = Mail.query.get(current_user.mail_id).id

    return data


def data_for_appeal_from_anonim_user():
    data = dict()
    mail_from_req = request.form.get('email')
    mail_obj_list = Mail.query.filter_by(mail=mail_from_req).all()

    if not mail_obj_list:
        mail_obj = Mail(mail=mail_from_req)
        db.session.add(mail_obj)
        db.session.commit()
    else:
        mail_obj = mail_obj_list[0]

    data['name'] = request.form.get('full-name')
    data['mail_id'] = mail_obj.id

    return data


def send_appeal():
    if current_user.is_authenticated:
        data = data_for_appeal_from_auth_user()
    else:
        data = data_for_appeal_from_anonim_user()
    data['message'] = request.form.get('message')
    appeal = Appeal(join_to_club=check_is_join_req(), **data)
    db.session.add(appeal)
    db.session.commit()


def event_detail(event_id):
    event = db.get_or_404(Event, event_id)
    return event
