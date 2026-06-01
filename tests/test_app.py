import pytest
from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({"DATABASE": str(tmp_path / "test.db")})
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_create_user(client):
    res = client.post("/api/users/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "pw1234"
    })
    assert res.status_code == 201


def test_create_todo(client):
    client.post("/api/users/register", json={
        "username": "bob", "email": "bob@example.com", "password": "pw"
    })
    res = client.post("/api/todos/", json={
        "user_id": 1, "title": "buy milk"
    })
    assert res.status_code == 201
