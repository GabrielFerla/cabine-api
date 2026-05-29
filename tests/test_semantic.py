# tests/test_semantic.py
import os, pytest
from .conftest import login
from .llm_judge import semantic_assert

pytestmark = [
    pytest.mark.semantic,
    pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="sem ANTHROPIC_API_KEY"),
]

def test_mensagem_de_alerta_descreve_o_problema(client):
    """assert == so confere que existe alerta. A IA confere se a MENSAGEM faz sentido."""
    token = login(client)
    client.post("/readings", headers={"Authorization": f"Bearer {token}"},
                json={"sensor_id": 1, "value": 18})         # umidade muito baixa p/ alface
    alerts = client.get("/alerts", headers={"Authorization": f"Bearer {token}"}).json()
    msg = alerts[-1]["message"]

    ok, reason = semantic_assert(
        claim=f"A mensagem de alerta '{msg}' indica corretamente que a UMIDADE DO SOLO "
              f"esta baixa demais para a cultura de ALFACE.",
        context="Uma leitura de umidade do solo de 18% chegou numa cabine cultivando alface. "
                "A faixa saudavel e 40-80% e a critica abaixo de 30%.",
    )
    assert ok, f"Juiz reprovou: {reason}"
