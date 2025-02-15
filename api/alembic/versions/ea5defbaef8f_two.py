"""two

Revision ID: ea5defbaef8f
Revises: 59e24c9d7b13
Create Date: 2025-01-24 12:23:53.682624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea5defbaef8f'
down_revision: Union[str, None] = '59e24c9d7b13'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('video', sa.String(), nullable=True),
    sa.Column('photo', sa.String(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('recipient_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    # ### end Alembic commands ###
