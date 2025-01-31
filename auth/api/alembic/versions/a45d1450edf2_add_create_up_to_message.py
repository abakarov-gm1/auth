"""add create_up_to_message

Revision ID: a45d1450edf2
Revises: e0ea82236b99
Create Date: 2025-01-31 06:13:39.926502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a45d1450edf2'
down_revision: Union[str, None] = 'e0ea82236b99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('file', sa.String(), nullable=True))
    op.add_column('message', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.drop_column('message', 'video')
    op.drop_column('message', 'photo')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('photo', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('message', sa.Column('video', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('message', 'created_at')
    op.drop_column('message', 'file')
    # ### end Alembic commands ###
