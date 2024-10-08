"""Added tables

Revision ID: a09b724c9f57
Revises: 
Create Date: 2024-04-20 08:12:22.830180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a09b724c9f57'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('login', sa.String(length=32), nullable=False),
    sa.Column('password', sa.LargeBinary(), nullable=False),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login'),
    sa.UniqueConstraint('username')
    )
    op.create_table('palette',
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_palette_user_name', 'palette', ['user_id', 'name'], unique=True)
    op.create_table('color',
    sa.Column('palette_id', sa.BigInteger(), nullable=True),
    sa.Column('color_hex', sa.LargeBinary(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
    sa.ForeignKeyConstraint(['palette_id'], ['palette.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_color_name_palette_id', 'color', ['palette_id', 'name'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_color_name_palette_id', table_name='color')
    op.drop_table('color')
    op.drop_index('idx_palette_user_name', table_name='palette')
    op.drop_table('palette')
    op.drop_table('user')
    # ### end Alembic commands ###
