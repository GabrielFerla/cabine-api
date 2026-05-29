# tests/test_cabins.py
from .conftest import login

def test_listar_com_token(client):
    token = login(client)
    r = client.get("/cabins", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200 and isinstance(r.json(), list)

def test_listar_sem_token(client):
    assert client.get("/cabins").status_code == 401

def test_criar_sem_ser_admin(client):
    token = login(client, "op@test.dev")                   # role operator
    r = client.post("/cabins", headers={"Authorization": f"Bearer {token}"},
                    json={"name": "Nova", "location": "X", "type": "terrestre"})
    assert r.status_code == 403
