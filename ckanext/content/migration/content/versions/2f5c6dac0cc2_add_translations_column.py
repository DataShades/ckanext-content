"""Add translations column

Revision ID: 2f5c6dac0cc2
Revises: 2a0ba263873f
Create Date: 2025-07-15 16:11:50.129693

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "2f5c6dac0cc2"
down_revision = "2a0ba263873f"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "content",
        sa.Column(
            "translations",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )


def downgrade():
    op.drop_column("content", "translations")
