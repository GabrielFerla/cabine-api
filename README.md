# Cabine API — núcleo (Banco · API · Segurança · Testes com IA)

Backend em **FastAPI + SQLModel + MySQL** do projeto Cabine Autossuficiente (Global Solution FIAP 2026/1).
Cobre P1 (banco), P2 (API REST em camadas), P5 (segurança/JWT) e P3 (testes — com camada de IA).

## Rodar (3 passos)

```bash
# 1. banco
docker compose up -d mysql

# 2. ambiente + deps
python -m venv .venv
.venv\Scripts\activate            # Windows (PowerShell/CMD)
# source .venv/bin/activate       # Linux/Mac/WSL
pip install -r requirements.txt

# 3. subir a API (cria schema + carrega seeds no startup)
uvicorn app.main:app --reload
```

Abra **http://localhost:8000/docs** → botão **Authorize**.
Login de demo (campo `username` = email): `admin@cabine.dev` / `senha123`

## Testes

```bash
pytest -m "not semantic"      # suíte determinística (rubrica), rápida e sem custo — usa SQLite em memória
pytest -m semantic            # camada de IA (juiz Claude) — precisa de ANTHROPIC_API_KEY

# Windows:  set ANTHROPIC_API_KEY=sk-ant-...
# Linux:    export ANTHROPIC_API_KEY=sk-ant-...
```

## Entregáveis SQL
- `sql/create_tables.sql` — DDL (CREATE TABLE + PK + FK + índices), 6 tabelas
- `sql/queries_exemplo.sql` — 5 consultas de exemplo

## Estrutura
`app/routers` (Controller) → `app/services` (regra de negócio) → `app/repositories` (acesso a dados).
Models em `app/models.py`, schemas/validação em `app/schemas.py`, segurança em `app/core/security.py`.

## Notas de montagem (o que mudou do guia)
Itens que o guia deixava como "segue o mesmo padrão" e foram completados pra app subir:
`user_repository.py`, `alert_repository.py`, `routers/alerts.py`, `routers/crops.py`, `tests/__init__.py`.
Dois fixes de compatibilidade: removido `from __future__ import annotations` do `models.py`
(quebrava os `Relationship` no SQLAlchemy atual) e corrigido o import de `utcnow` no `seed.py`
(estava apontando pra `core.database`; vive em `models`).
