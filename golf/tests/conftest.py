import pytest
from flask_login import login_user

from golf import app, db
from golf.models import User


@pytest.fixture()
def my_app():
    app.config.update({'TESTING': True})
    yield app


@pytest.fixture()
def client(my_app):
    return app.test_client()


@pytest.fixture()
def runner(my_app):
    return app.test_cli_runner()


@pytest.fixture()
def authenticated_request():
    with app.test_request_context():
        test_user = db.session.query(User).filter_by(account_number='admin').first()
        yield login_user(test_user)
