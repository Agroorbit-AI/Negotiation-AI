"""align sessionstatus enum values

Revision ID: 538f7bc288fb
Revises: f28a2b3fe1cb
Create Date: 2026-01-08 17:29:07.534266

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '538f7bc288fb'
down_revision: Union[str, Sequence[str], None] = 'f28a2b3fe1cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("ALTER TYPE sessionstatus ADD VALUE IF NOT EXISTS 'active'")
    op.execute("ALTER TYPE sessionstatus ADD VALUE IF NOT EXISTS 'completed'")
    op.execute("ALTER TYPE sessionstatus ADD VALUE IF NOT EXISTS 'failed'")


def downgrade():
    raise RuntimeError("Downgrade not supported for enum changes")
