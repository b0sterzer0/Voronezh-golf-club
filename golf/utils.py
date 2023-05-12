from typing import Union

from flask import request
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from golf.models import db, User, Event, Mail, Appeal, SiteData


def login_custom_func() -> Union[None, User]:
    account_number = request.form.get('member-login-number')
    password = request.form.get('member-login-password')
    user = User.query.filter_by(account_number=account_number).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
    else:
        return user


def get_events() -> Event:
    events = Event.query.order_by(Event.date).all()
    return events


def get_one_event(event_id) -> Event:
    return db.get_or_404(Event, event_id)


def get_users() -> User:
    users = User.query.filter_by(is_admin=False).all()
    return users


def get_one_user_with_email(user_id: int) -> User:
    user = db.get_or_404(User, user_id)
    email = db.get_or_404(Mail, user.mail_id)
    return user, email.mail


def delete_user_util(user_id: int) -> None:
    """
    Удаляет пользователя
    """
    user, email = get_one_user_with_email(user_id)
    db.session.delete(user)
    db.session.commit()


def delete_event_util(event_id: int) -> None:
    """
    Удаляет событие
    """
    event = get_one_event(event_id)
    db.session.delete(event)
    db.session.commit()


def add_mail() -> int:
    """
    Получает из формы email, находить в БД и возвращает его id. Если email не в БД - создает
    """
    user_mail = request.form.get('email')
    if user_mail:
        mail_in_db = Mail.query.filter_by(mail=user_mail).all()
        if not mail_in_db:
            mail_obj = Mail(mail=user_mail)
            db.session.add(mail_obj)
            db.session.commit()
            return mail_obj.id
        return mail_in_db[0].id


def edit_user_util(user_id: int) -> None:
    """
    Используя полученные данные из формы, изменяет пользователя в БД (административный раздел)
    """
    user, email = get_one_user_with_email(user_id)
    user.account_number = request.form.get('account-number')
    user.mail_id = add_mail()
    if request.form.get('user-password'):
        user.password = generate_password_hash(request.form.get('user-password'))
    db.session.commit()


def edit_event_util(event_id: int) -> None:
    """
    Используя полученные данные из формы, изменяет событие в БД (административный раздел)
    """
    event = get_one_event(event_id)
    event.title = request.form.get('event-title')
    event.description = request.form.get('event-description')
    event.date = request.form.get('event-date')
    event.location = request.form.get('event-location')
    event.ticket_price = request.form.get('event-price')
    db.session.commit()


def check_is_join_req() -> bool:
    """
    Проверяет, является ли обращение пользователем заявкой на вступление в клуб
    """
    is_join_req = False
    if request.path == '/join_request/':
        is_join_req = True

    return is_join_req


def data_for_appeal_from_anonim_user() -> dict:
    """
    Собирает данные из формы обращения анонимного пользователя
    """
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


def send_appeal() -> Appeal:
    """
    Сохраняет обращение пользователя в БД
    """
    if current_user.is_authenticated:
        mail_id = db.get_or_404(Mail, current_user.mail_id).id
        data = {'name': current_user.account_number, 'mail_id': mail_id}
    else:
        data = data_for_appeal_from_anonim_user()
    data['message'] = request.form.get('message')
    appeal = Appeal(join_to_club=check_is_join_req(), **data)
    db.session.add(appeal)
    db.session.commit()

    return appeal


def event_detail(event_id: int) -> Event:
    event = db.get_or_404(Event, event_id)
    return event


def save_settings() -> None:
    """
    Используя полученные из формы данные, обновляет настройки сайта
    """
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


def new_user() -> None:
    """
    Создает нового пользователя (административный раздел)
    """
    mail_id = add_mail()
    data = {
        'account_number': request.form.get('account-number'),
        'mail_id': mail_id,
        'password': generate_password_hash(request.form.get('user-password')),
        'is_admin': False
    }
    user = User(**data)
    db.session.add(user)
    db.session.commit()


def new_event() -> None:
    """
    Создает новое событие (административный раздел)
    """
    data = {
        'title': request.form.get('event-title'),
        'description': request.form.get('event-description'),
        'date': request.form.get('event-date'),
        'location': request.form.get('event-location'),
        'ticket_price': request.form.get('event-price')
    }

    event = Event(**data)
    db.session.add(event)
    db.session.commit()
