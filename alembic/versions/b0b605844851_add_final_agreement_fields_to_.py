"""add final agreement fields to negotiation session

Revision ID: b0b605844851
Revises: 8fedd09d3936
Create Date: 2026-01-17 18:21:46.018642
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b0b605844851"
down_revision: Union[str, Sequence[str], None] = "8fedd09d3936"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Add final agreement fields to negotiation_sessions
    SAFE migration – no data loss
    """

    op.add_column(
        "negotiation_sessions",
        sa.Column(
            "final_price",
            sa.Numeric(precision=10, scale=2),
            nullable=True
        ),
    )

    op.add_column(
        "negotiation_sessions",
        sa.Column(
            "agreed_at",
            sa.DateTime(timezone=True),
            nullable=True
        ),
    )

    op.add_column(
        "negotiation_sessions",
        sa.Column(
            "agreement_channel",
            sa.Enum(
                "web",
                "whatsapp",
                "telecalling",
                name="agreementchannelenum"
            ),
            nullable=True
        ),
    )


def downgrade() -> None:
    """
    Rollback agreement fields
    """

    op.drop_column("negotiation_sessions", "agreement_channel")
    op.drop_column("negotiation_sessions", "agreed_at")
    op.drop_column("negotiation_sessions", "final_price")

    # Drop ENUM explicitly (Postgres requirement)
    op.execute("DROP TYPE IF EXISTS agreementchannelenum")
