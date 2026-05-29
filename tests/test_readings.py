# tests/test_readings.py
from .conftest import login

def test_leitura_abaixo_do_threshold_gera_alerta(client):
    token = login(client)
    r = client.post("/readings", headers={"Authorization": f"Bearer {token}"},
                    json={"sensor_id": 1, "value": 20})     # umid_solo 20 < crit_min(30)
    body = r.json()
    assert r.status_code == 201
    assert body["alert_generated"] is True
    assert body["alert_severity"] == "critical"

def test_sensor_inexistente(client):
    token = login(client)
    r = client.post("/readings", headers={"Authorization": f"Bearer {token}"},
                    json={"sensor_id": 99999, "value": 50})
    assert r.status_code == 404
