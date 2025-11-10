from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_deve_retornar_ola_mundo():
    client = TestClient(app)
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK


def test_home():
    client = TestClient(app)
    response = client.get('/home')
    assert '<h1> Ol\xe1 home </h1>' in response.text


def test_create_user():
    client = TestClient(app)

    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }
