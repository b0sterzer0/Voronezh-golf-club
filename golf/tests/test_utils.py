from flask import request, current_app
from werkzeug.datastructures import ImmutableMultiDict

from conftest import client, app, db
from golf.utils import get_events, add_mail
from golf.models import Mail


def test_get_events_func(client):
    with app.test_request_context():
        events = get_events()
    assert events


def test_add_mail_func(client):
    with app.test_request_context():
        with current_app.test_request_context("/", method="GET", data={"email": "test@test.ru"}):
            result_exist_email = add_mail()
        with current_app.test_request_context("/", method="GET", data={"email": "test2@test.ru"}):
            add_mail()
            result_not_exist_email = Mail.query.filter_by(mail="test2@test.ru")
            result_not_exist_email.delete()
            db.session.commit()

    assert result_exist_email
    assert result_not_exist_email
