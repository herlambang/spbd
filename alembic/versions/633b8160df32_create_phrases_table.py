"""create phrases table

Revision ID: 633b8160df32
Revises: 0bc2c9f1384a
Create Date: 2025-01-27 15:56:27.444065

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "633b8160df32"
down_revision: Union[str, None] = "0bc2c9f1384a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "phrases",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("words", sa.Text),
    )


def downgrade() -> None:
    op.drop_table("phrases")
