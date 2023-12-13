import pytest
from app import schemas


def test_root(client):
    res = client.get("/")
    assert res.json() == {"message": "Hello!"}
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/alchemy/users/", json={"email": "hello@gmail.com", "password": "pass123"})

    new_user = schemas.UserOut(**res.json())
    assert res.json().get("email") == "hello@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": 'testUser@gmail.com', "password": 'testUser123'})
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrong@gmail.com', 'testUser123', 403),
    ('testUser@gmail.com', 'wrongpass', 403),
    ('wrong@gmail.com', 'wrongpass', 403),
    (None, 'testUser123', 422),
    ('testUser@gmail.com', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code