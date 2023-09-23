"""create tables

Revision ID: 507afc1b8807
Revises: 9a59146cd0c5
Create Date: 2023-09-23 13:32:04.329491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '507afc1b8807'
down_revision = '9a59146cd0c5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message_store')
    op.add_column('messages', sa.Column('message_token_count', sa.Integer(), nullable=True))
    op.add_column('messages', sa.Column('consumed_token_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'consumed_token_count')
    op.drop_column('messages', 'message_token_count')
    op.create_table('message_store',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('session_id', sa.TEXT(), nullable=True),
    sa.Column('message', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
