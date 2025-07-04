"""adding created_at and updated_at to headers

Revision ID: d5c008cfd164
Revises: 411343d7c72b
Create Date: 2025-05-11 16:50:44.254083

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'd5c008cfd164'
down_revision: Union[str, None] = '411343d7c72b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('header', sa.Column('created_at', sa.DateTime(), nullable=False, server_default=str(datetime.now())))
    op.add_column('header', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_header_created_at'), 'header', ['created_at'], unique=False)
    op.create_index(op.f('ix_header_updated_at'), 'header', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_header_updated_at'), table_name='header')
    op.drop_index(op.f('ix_header_created_at'), table_name='header')
    op.drop_column('header', 'updated_at')
    op.drop_column('header', 'created_at')
    # ### end Alembic commands ###
