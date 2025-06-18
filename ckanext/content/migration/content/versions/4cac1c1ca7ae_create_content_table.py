"""Create content table

Revision ID: 4cac1c1ca7ae
Revises:
Create Date: 2025-06-16 23:30:23.324160

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "4cac1c1ca7ae"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "content",
        sa.Column("id", sa.Text, primary_key=True, unique=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("alias", sa.Text(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
    )


def downgrade():
    op.drop_table("content")
