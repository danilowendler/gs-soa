"""guarda os 3 dias de clima enviados em cada previsão (contrato com o modelo de ML)

Revision ID: 0003
Revises: 0002
Create Date: 2026-11-09
"""
import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("previsoes", sa.Column("dias_json", sa.Text(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("previsoes") as tabela:
        tabela.drop_column("dias_json")
