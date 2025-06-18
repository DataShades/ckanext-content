"""Add Author column

Revision ID: c8f5146ec6d8
Revises: 4cac1c1ca7ae
Create Date: 2025-06-17 17:09:53.762439

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c8f5146ec6d8"
down_revision = "4cac1c1ca7ae"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "content",
        sa.Column("author", sa.Text(), nullable=False),
    )


def downgrade():
    op.drop_column("content", "author")
