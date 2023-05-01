from flask import request
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from golf.models import db, User, Event, Mail, Appeal, SiteData


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
        mail_id = Mail.query.get(current_user.mail_id).id
        data = {'name': current_user.account_number, 'mail_id': mail_id}
    else:
        data = data_for_appeal_from_anonim_user()
    data['message'] = request.form.get('message')
    appeal = Appeal(join_to_club=check_is_join_req(), **data)
    db.session.add(appeal)
    db.session.commit()

    return appeal


def event_detail(event_id):
    event = db.get_or_404(Event, event_id)
    return event


def save_settings():
    settings = db.get_or_404(SiteData, 1)
    settings.club_name = request.form.get('club-name')
    settings.email = request.form.get('club-email')
    settings.phone_number = request.form.get('club-phone')
    settings.city = request.form.get('club-city')
    settings.address = request.form.get('club-address')
    settings.club_history = request.form.get('club-history')
    settings.work_hours_weekdays = request.form.get('club-work-hours-weekdays')
    settings.work_hours_weekend = request.form.get('club-work-hours-weekend')
    settings.url_video_on_main_page = request.form.get('club-preview-video')
    db.session.commit()


def new_user():
    mail_obj_list = Mail.query.filter_by(mail=request.form.get('email')).all()
    if not mail_obj_list:
        mail_obj = Mail(mail=request.form.get('email'))
        db.session.add(mail_obj)
        db.session.commit()
    else:
        mail_obj = mail_obj_list[0]
    data = {
        'account_number': request.form.get('account-number'),
        'mail_id': mail_obj.id,
        'password': generate_password_hash(request.form.get('user-password')),
        'is_admin': False
    }
    user = User(**data)
    db.session.add(user)
    db.session.commit()
