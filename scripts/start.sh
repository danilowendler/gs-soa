#!/usr/bin/env bash
# Aplica as migrações e sobe o serviço na porta 8000 (útil como ExecStart do systemd na VM).
set -euo pipefail
cd "$(dirname "$0")/.."
alembic upgrade head
exec uvicorn app.main:app --host "${HOST:-0.0.0.0}" --port "${PORT:-8000}"
