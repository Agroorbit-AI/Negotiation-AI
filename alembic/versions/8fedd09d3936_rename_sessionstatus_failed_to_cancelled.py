"""rename sessionstatus failed to cancelled

Revision ID: 8fedd09d3936
Revises: 538f7bc288fb
Create Date: 2026-01-10 10:57:52.063589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fedd09d3936'
down_revision: Union[str, Sequence[str], None] = '538f7bc288fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        "ALTER TYPE sessionstatus RENAME VALUE 'failed' TO 'cancelled';"
    )


def downgrade():
    op.execute(
        "ALTER TYPE sessionstatus RENAME VALUE 'cancelled' TO 'failed';"
    )
