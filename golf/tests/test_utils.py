from datetime import date

import pytest

from conftest import client, app, db
from golf.utils import get_events, add_mail, check_is_join_req, data_for_appeal_from_anonim_user, send_appeal,\
    new_user, new_event
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
        db.session.delete(user)
        db.session.commit()

    assert user


def test_new_event(client):
    with app.test_request_context('/create_user/', method='POST', data={'event-title': 'test',
                                                                        'event-description': 'test desc',
                                                                        'event-date': date.today(),
                                                                        'event-location': 'test loc',
                                                                        'event-price': 1000}):
        new_event()
        event = Event.query.filter_by(title='test').first()
        db.session.delete(event)
        db.session.commit()

    assert event
