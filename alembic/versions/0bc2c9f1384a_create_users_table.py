"""create users table

Revision ID: 0bc2c9f1384a
Revises:
Create Date: 2025-01-26 20:10:57.510935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bc2c9f1384a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255)),
    )


def downgrade() -> None:
    op.drop_table('users')
