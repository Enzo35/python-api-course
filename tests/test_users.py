from app import schemas
from .database import session, client

def test_root(client):
    res = client.get("/")
    assert res.json() == {"message": "Hello!"}
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/alchemy/users/", json={"email": "hello@gmail.com", "password": "pass123"})

    new_user = schemas.UserOut(**res.json())
    assert res.json().get("email") == "hello@gmail.com"
    assert res.status_code == 201