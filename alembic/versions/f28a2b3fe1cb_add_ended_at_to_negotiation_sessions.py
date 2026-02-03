"""add ended_at to negotiation_sessions

Revision ID: f28a2b3fe1cb
Revises: 1819382f403d
Create Date: 2026-01-08 17:12:35.345009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f28a2b3fe1cb'
down_revision: Union[str, Sequence[str], None] = '1819382f403d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "negotiation_sessions",
        sa.Column("final_price", sa.Float(), nullable=True)
    )
    op.add_column(
        "negotiation_sessions",
        sa.Column("agreed_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "negotiation_sessions",
        sa.Column("agreement_channel", sa.String(), nullable=True)
    )


def downgrade():
    op.drop_column("negotiation_sessions", "agreement_channel")
    op.drop_column("negotiation_sessions", "agreed_at")
    op.drop_column("negotiation_sessions", "final_price")
