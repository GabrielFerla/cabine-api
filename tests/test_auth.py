# tests/test_auth.py
from .conftest import login

def test_login_valido(client):
    r = client.post("/auth/login", data={"username": "admin@test.dev", "password": "senha123"})
    assert r.status_code == 200 and "access_token" in r.json()

def test_login_invalido(client):
    r = client.post("/auth/login", data={"username": "admin@test.dev", "password": "errada"})
    assert r.status_code == 401
