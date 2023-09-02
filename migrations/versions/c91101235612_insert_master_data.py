"""Insert message_type table master data

Revision ID: c91101235612
Revises: d2f3b4664ed9
Create Date: 2023-08-26 17:22:44.060626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c91101235612"
down_revision = "d2f3b4664ed9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    message_type = sa.table("message_type", sa.column("message_type_name", sa.String))
    op.bulk_insert(
        message_type,
        [
            {"message_type_name": "human"},
            {"message_type_name": "artificial intelligence"},
        ],
    )
    pass


def downgrade() -> None:
    pass
