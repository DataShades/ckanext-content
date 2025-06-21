"""Add content_revision table

Revision ID: 2a0ba263873f
Revises: 0740d5df4d87
Create Date: 2025-06-18 11:56:59.572617

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "2a0ba263873f"
down_revision = "0740d5df4d87"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "content_revision",
        sa.Column("id", sa.Text, primary_key=True, unique=True),
        sa.Column(
            "content_id",
            sa.Text(),
            sa.ForeignKey("content.id"),
            nullable=False,
        ),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("alias", sa.Text(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("modified", sa.DateTime(), nullable=False),
        sa.Column("author", sa.Text(), nullable=False),
        sa.Column("state", sa.Text(), nullable=False),
    )


def downgrade():
    op.drop_table("content_revision")
