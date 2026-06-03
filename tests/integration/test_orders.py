"""
Integration tests for the order flow.

Coverage gap: no tests for cancel/refund, no tests for legacy endpoints,
no tests for rate limiting.
"""
import pytest
from app import create_app


@pytest.fixture
def client(tmp_path):
    import os
    os.environ["DATABASE_URL"] = f"sqlite:///{tmp_path}/test.db"
    app = create_app("development")
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def _make_user_and_token(client, email="a@b.com"):
    client.post("/api/v2/users/register", json={"email": email, "password": "longenough"})
    res = client.post("/api/v2/users/login", json={"email": email, "password": "longenough"})
    return res.get_json()["token"]


def test_create_order_requires_auth(client):
    res = client.post("/api/v2/orders/", json={"items": []})
    assert res.status_code == 401
