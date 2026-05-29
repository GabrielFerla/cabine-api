# Plano de Testes — Cabine API (P3)

Plano de testes do backend, no formato exigido pela rubrica (**cenário · entrada · saída esperada · status**).
São **8 casos** — 7 determinísticos (automatizados com `pytest` + `httpx`, banco SQLite em memória) e
1 com **camada de IA** (juiz Claude avalia o *sentido* da saída). Rubrica pede ≥5 casos e ≥3 executados.

## Como executar

```bash
# 1. crie o .env (uma vez):  copy .env.example .env   (Windows)  |  cp .env.example .env  (Linux/Mac)
pytest -m "not semantic" -v    # suite deterministica (sem custo) — usa SQLite em memoria
pytest -m semantic -v          # camada de IA — requer ANTHROPIC_API_KEY
```

A evidência da execução fica em [`evidencias/`](evidencias/).

## Casos de teste

| # | Cenário | Entrada | Saída esperada | Status | Camada |
|---|---------|---------|----------------|--------|--------|
| 1 | Login com credenciais válidas | `POST /auth/login` · `username=admin@test.dev` `password=senha123` | `200` + corpo com `access_token` | ✅ Pass | determinística |
| 2 | Login com senha incorreta | `POST /auth/login` · `username=admin@test.dev` `password=errada` | `401` Credenciais inválidas | ✅ Pass | determinística |
| 3 | Listar cabines autenticado | `GET /cabins` com header `Authorization: Bearer <token>` | `200` + corpo é uma lista | ✅ Pass | determinística |
| 4 | Listar cabines sem token | `GET /cabins` sem `Authorization` | `401` Não autenticado | ✅ Pass | determinística |
| 5 | Criar cabine sem ser admin | `POST /cabins` com token de `operator` | `403` Requer permissão de admin | ✅ Pass | determinística |
| 6 | Leitura abaixo do limite crítico gera alerta | `POST /readings` · `sensor_id=1` (umid_solo, cabine c/ alface) `value=20` | `201` + `alert_generated=true` + `alert_severity="critical"` | ✅ Pass | determinística |
| 7 | Leitura para sensor inexistente | `POST /readings` · `sensor_id=99999` `value=50` | `404` sensor inexistente | ✅ Pass | determinística |
| 8 | Mensagem de alerta é semanticamente coerente | `POST /readings` `value=18` → `GET /alerts`; juiz Claude avalia a mensagem | Juiz aprova (`pass=true`): a mensagem indica umidade baixa demais p/ alface | ✅ Pass¹ | IA (semântica) |

¹ Requer `ANTHROPIC_API_KEY` no ambiente; sem a chave, o caso é **pulado** (`skipped`) automaticamente.

## Cobertura por área da rubrica

- **Autenticação (P5):** casos 1, 2 (login + hash via bcrypt).
- **Autorização/JWT (P5):** casos 3, 4, 5 (token obrigatório + RBAC admin).
- **Regra de negócio (P3/IoT):** casos 6, 7 (threshold → alerta automático).
- **Qualidade semântica (diferencial com IA):** caso 8.

## Arquivos-fonte dos testes
`tests/test_auth.py` (1–2) · `tests/test_cabins.py` (3–5) · `tests/test_readings.py` (6–7) ·
`tests/test_semantic.py` + `tests/llm_judge.py` (8) · fixtures em `tests/conftest.py`.
