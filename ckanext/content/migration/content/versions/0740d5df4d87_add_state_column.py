"""Add State column

Revision ID: 0740d5df4d87
Revises: c8f5146ec6d8
Create Date: 2025-06-17 22:42:52.798117

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0740d5df4d87"
down_revision = "c8f5146ec6d8"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "content",
        sa.Column("state", sa.Text(), nullable=False),
    )


def downgrade():
    op.drop_column("content", "state")
