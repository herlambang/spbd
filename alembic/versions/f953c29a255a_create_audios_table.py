"""create audios table

Revision ID: f953c29a255a
Revises: 633b8160df32
Create Date: 2025-01-27 16:04:27.772171

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f953c29a255a"
down_revision: Union[str, None] = "633b8160df32"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "audios",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("phrase_id", sa.Integer, sa.ForeignKey("phrases.id")),
        sa.Column("path", sa.String(255), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("audios")
