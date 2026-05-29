# Cabine API — núcleo (Banco · API · Segurança · Testes com IA)

Backend em **FastAPI + SQLModel + MySQL** do projeto Cabine Autossuficiente (Global Solution FIAP 2026/1).
Cobre P1 (banco), P2 (API REST em camadas), P5 (segurança/JWT) e P3 (testes — com camada de IA).

## Rodar (4 passos)

```bash
# 1. banco
docker compose up -d mysql

# 2. ambiente + deps
python -m venv .venv
.venv\Scripts\activate            # Windows (PowerShell/CMD)
# source .venv/bin/activate       # Linux/Mac/WSL
pip install -r requirements.txt

# 3. variaveis de ambiente: copie o template
copy .env.example .env            # Windows
# cp .env.example .env            # Linux/Mac/WSL
# (opcional) gere uma JWT_KEY forte e cole no .env:
# python -c "import secrets; print(secrets.token_urlsafe(48))"

# 4. subir a API (cria schema + carrega seeds no startup)
uvicorn app.main:app --reload
```

Abra **http://localhost:8000/docs** → botão **Authorize**.
Login de demo (campo `username` = email): `admin@cabine.dev` / `senha123`

## Testes

> Requer o `.env` criado no passo 3 — o `conftest.py` importa `app.main`, que lê as configs no import.

```bash
pytest -m "not semantic"      # suíte determinística (rubrica), rápida e sem custo — usa SQLite em memória
pytest -m semantic            # camada de IA (juiz Claude) — precisa de ANTHROPIC_API_KEY

# Windows:  set ANTHROPIC_API_KEY=sk-ant-...
# Linux:    export ANTHROPIC_API_KEY=sk-ant-...
```

## Entregáveis SQL
- `sql/create_tables.sql` — DDL (CREATE TABLE + PK + FK + índices), 6 tabelas
- `sql/queries_exemplo.sql` — 5 consultas de exemplo

## Entregáveis (documentação)
- `docs/DER.md` — Diagrama ER (Mermaid + DBML p/ dbdiagram.io) das 6 entidades
- `docs/plano-de-testes.md` — plano com 8 casos (cenário/entrada/saída/status)
- `docs/evidencias/` — saída do `pytest` (evidência de execução exigida pela rubrica)

## Estrutura
`app/routers` (Controller) → `app/services` (regra de negócio) → `app/repositories` (acesso a dados).
Models em `app/models.py`, schemas/validação em `app/schemas.py`, segurança em `app/core/security.py`.

## Notas de montagem (o que mudou do guia)
Itens que o guia deixava como "segue o mesmo padrão" e foram completados pra app subir:
`user_repository.py`, `alert_repository.py`, `routers/alerts.py`, `routers/crops.py`, `tests/__init__.py`.
Dois fixes de compatibilidade: removido `from __future__ import annotations` do `models.py`
(quebrava os `Relationship` no SQLAlchemy atual) e corrigido o import de `utcnow` no `seed.py`
(estava apontando pra `core.database`; vive em `models`).
