"""indice por data em previsoes (consulta do alerta do dia)

Revision ID: 0002
Revises: 0001
Create Date: 2026-11-05
"""
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index("ix_previsoes_data", "previsoes", ["data"])


def downgrade() -> None:
    op.drop_index("ix_previsoes_data", table_name="previsoes")
