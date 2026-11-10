"""cria tabela previsoes

Revision ID: 0001
Revises:
Create Date: 2026-11-05
"""
import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "previsoes",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("data", sa.Date(), nullable=False),
        sa.Column("temperatura_max_ontem", sa.Float(), nullable=False),
        sa.Column("temperatura_min_ontem", sa.Float(), nullable=False),
        sa.Column("umidade_media_ontem", sa.Float(), nullable=False),
        sa.Column("vento_medio_ontem", sa.Float(), nullable=False),
        sa.Column("probabilidade", sa.Float(), nullable=False),
        sa.Column("perigoso", sa.Boolean(), nullable=False),
        sa.Column("versao_modelo", sa.String(length=32), nullable=False),
        sa.Column("criado_em", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("probabilidade >= 0 AND probabilidade <= 1", name="ck_previsoes_probabilidade"),
    )


def downgrade() -> None:
    op.drop_table("previsoes")
