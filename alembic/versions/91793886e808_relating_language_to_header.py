"""relating language to header

Revision ID: 91793886e808
Revises: 4a23603c6c50
Create Date: 2025-05-01 16:12:42.274209

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '91793886e808'
down_revision: Union[str, None] = '4a23603c6c50'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('header', sa.Column('language_id', sa.Uuid(), nullable=False))
    op.create_foreign_key(None, 'header', 'language', ['language_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'header', type_='foreignkey')
    op.drop_column('header', 'language_id')
    # ### end Alembic commands ###
