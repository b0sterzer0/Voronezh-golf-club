import pytest

from conftest import client


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
