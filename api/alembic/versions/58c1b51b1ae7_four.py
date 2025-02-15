"""four

Revision ID: 58c1b51b1ae7
Revises: 4e054a6dd924
Create Date: 2025-01-24 17:52:44.272106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58c1b51b1ae7'
down_revision: Union[str, None] = '4e054a6dd924'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat_users',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('chat_id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chat.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chat_users')
    # ### end Alembic commands ###
