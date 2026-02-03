"""add final agreement fields safely

Revision ID: cd053ba9efdf
Revises: b0b605844851
Create Date: 2026-01-17 21:24:44.039178

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd053ba9efdf'
down_revision: Union[str, Sequence[str], None] = 'b0b605844851'
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
