import pytest
import json

from auth import app

DUMMY_USERNAME = "dummy"
DUMMY_EMAIL = "dummy@dummy.com"
DUMMY_PASS = "dummy"


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_user_signup(client):
    response = client.post(
        "api/auth/register",
        data=json.dumps(
            {"username": DUMMY_USERNAME, "email": DUMMY_EMAIL, "password": DUMMY_PASS}
        ),
        content_type="application/json",
    )

    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert "The user was successfully registered" in data["msg"]


def test_user_signup_invalid_data(client):
    response = client.post(
        "api/auth/register",
        data=json.dumps(
            {"username": DUMMY_USERNAME, "email": "", "password": DUMMY_PASS}
        ),
        content_type="application/json",
    )

    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "'' is too short" in data["msg"]


def test_user_login_correct(client):
    response = client.post(
        "api/auth/login",
        data=json.dumps({"email": DUMMY_EMAIL, "password": DUMMY_PASS}),
        content_type="application/json",
    )

    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data["token"] != ""


def test_user_login_error(client):
    response = client.post(
        "api/auth/login",
        data=json.dumps({"email": DUMMY_EMAIL, "password": DUMMY_EMAIL}),
        content_type="application/json",
    )

    data = json.loads(response.data.decode())
    assert response.status_code == 400
    assert "Wrong credentials." in data["msg"]
