from datetime import date

import pytest

from conftest import client, app, db # noqa F401
from golf.utils import get_events, add_mail, check_is_join_req, data_for_appeal_from_anonim_user, send_appeal,\
    new_user, new_event, edit_user_util, edit_event_util, delete_user_util, delete_event_util
from golf.models import Mail, User, Event


def test_get_events_func(client):
    with app.test_request_context():
        events = get_events()
    assert events


def test_add_mail_func(client):
    with app.test_request_context("/", method="GET", data={"email": "test@test.ru"}):
        result_exist_email = add_mail()
    with app.test_request_context("/", method="GET", data={"email": "test2@test.ru"}):
        add_mail()
        result_not_exist_email = Mail.query.filter_by(mail="test2@test.ru")
        result_not_exist_email.delete()
        db.session.commit()

    assert result_exist_email
    assert result_not_exist_email


def test_check_is_join_req(client):
    with app.test_request_context("/join_request/", method='GET'):
        result_1 = check_is_join_req()
    with app.test_request_context("/", method='GET'):
        result_2 = check_is_join_req()

    assert result_1
    assert not result_2


def test_data_for_appeal_from_anonim_user(client):
    with app.test_request_context('/', method='GET', data={"email": "test@test.ru", "full-name": 'admin'}):
        data_1 = data_for_appeal_from_anonim_user()
    with app.test_request_context('/', method='GET', data={"email": "test2@test.ru", "full-name": 'admin'}):
        data_2 = data_for_appeal_from_anonim_user()
        result_not_exist_email = Mail.query.filter_by(mail="test2@test.ru")
        result_not_exist_email.delete()
        db.session.commit()

    assert data_1['name'] == 'admin' and data_1['mail_id'] == 7
    assert data_2['name'] == 'admin' and result_not_exist_email


@pytest.mark.usefixtures('authenticated_request')
def test_send_appeal(client):
    with app.test_request_context('/', method='GET', data={'message': 'test message from test_send_appeal'}):
        appeal = send_appeal()
        db.session.delete(appeal)
        db.session.commit()

    assert appeal


def test_new_user(client):
    with app.test_request_context('/create_user/', method='POST', data={'account-number': 'test',
                                                                        'email': 'test@test.ru',
                                                                        'user-password': 'testtesttest'}):
        new_user()
        user = User.query.filter_by(account_number='test').first()

    assert user


def test_edit_user_util(client):
    with app.test_request_context('/create_user/', method='POST', data={'account-number': 'test',
                                                                        'email': 'testtesttest@gmail.com',
                                                                        'user-password': 'testtesttest'}):

        user = User.query.filter_by(account_number='test').first()
        edit_user_util(user.id)
        user = User.query.filter_by(account_number='test').first()
        mail_id = Mail.query.filter_by(mail='testtesttest@gmail.com').first().id

    assert user.mail_id == mail_id


def test_delete_user_util(client):
    with app.test_request_context():
        user = User.query.filter_by(account_number='test').first()
        delete_user_util(user.id)
        user = User.query.filter_by(account_number='test').first()

    assert not user


def test_new_event(client):
    with app.test_request_context('/create_event/', method='POST', data={'event-title': 'test',
                                                                         'event-description': 'test desc',
                                                                         'event-date': date.today(),
                                                                         'event-location': 'test loc',
                                                                         'event-price': 1000}):
        new_event()
        event = Event.query.filter_by(title='test').first()

    assert event


def test_edit_event_util(client):
    with app.test_request_context('/create_event/', method='POST', data={'event-title': 'test',
                                                                         'event-description': 'test desc',
                                                                         'event-date': date.today(),
                                                                         'event-location': 'test loc',
                                                                         'event-price': 2000}):
        event = Event.query.filter_by(title='test').first()
        edit_event_util(event.id)
        event = Event.query.filter_by(title='test').first()

    assert event.ticket_price == 2000


def test_delete_event_util(client):
    with app.test_request_context():
        event = Event.query.filter_by(title='test').first()
        delete_event_util(event.id)
        event = Event.query.filter_by(title='test').first()

    assert not event
