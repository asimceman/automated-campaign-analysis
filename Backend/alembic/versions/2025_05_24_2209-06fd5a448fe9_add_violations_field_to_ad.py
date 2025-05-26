"""add violations field to ad

Revision ID: 06fd5a448fe9
Revises: af4257e3c1d7
Create Date: 2025-05-24 22:09:19.434851

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06fd5a448fe9'
down_revision: Union[str, None] = 'af4257e3c1d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('ad', sa.Column('has_violations', sa.Boolean(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('ad', 'has_violations')
