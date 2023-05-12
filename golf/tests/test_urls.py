from datetime import date

import pytest

from conftest import client # noqa F401

from conftest import app
from golf.models import User, Event


def test_url_main_page(client):
    get_response = client.get('/')
    post_response = client.post('/')
    assert get_response.status == '200 OK'
    assert post_response.status == '302 FOUND'


def test_url_events_page(client):
    response = client.get('/events/')
    assert response.status == '200 OK'


def test_url_event_detail_page(client):
    response = client.get('/events/detail/1/')
    assert response.status == '200 OK'


@pytest.mark.usefixtures("authenticated_request")
def test_url_site_settings_page(client):
    get_response = client.get('/settings/')
    post_response = client.post('/settings/')

    assert get_response.status == '200 OK'
    assert post_response.status == '302 FOUND'
    assert post_response.request.path == "/settings/"


@pytest.mark.usefixtures('authenticated_request')
def test_url_logout(client):
    response = client.get('/logout/')

    assert response.status == '302 FOUND'


def test_url_add_mail(client):
    response = client.post('/add_mail/', data={'email': 'test@test.ru'})

    assert response.status == '302 FOUND'


def test_admin_url(client):
    response = client.get('/admin/')

    assert response.status == '200 OK'


@pytest.mark.usefixtures('authenticated_request')
def test_admin_user_url(client):
    with app.test_request_context():
        response = client.post('/admin/create_user/', data={'account-number': 'test', 'email': 'test@test.ru',
                                                            'user-password': '12345'})

    assert response.status == '302 FOUND'


def test_edit_user_url(client):
    response = client.get('/admin/edit_user/1/')

    assert response.status == '200 OK'


@pytest.mark.usefixtures('authenticated_request')
def test_delete_user_url(client):
    with app.test_request_context():
        user = User.query.filter_by(account_number='test').first()
        response = client.get(f'/admin/delete_user/{ user.id }/')

    assert response.status == '302 FOUND'


@pytest.mark.usefixtures('authenticated_request')
def test_admin_events_url(client):
    with app.test_request_context():
        response = client.post('/admin/create_event/', data={'event-title': 'new test', 'event-date': date.today(),
                                                             'event-location': 'test loc', 'event-price': 1000,
                                                             'event-description': 'test desc'})

    assert response.status == '302 FOUND'


def test_edit_event_url(client):
    response = client.get('/admin/edit_event/1/')

    assert response.status == '200 OK'


@pytest.mark.usefixtures('authenticated_request')
def test_delete_event_url(client):
    with app.test_request_context():
        event = Event.query.filter_by(title='new test').first()
        response = client.get(f'/admin/delete_event/{ event.id}/')

    assert response.status == '302 FOUND'
