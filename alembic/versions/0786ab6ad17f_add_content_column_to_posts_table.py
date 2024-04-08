"""add content column  to posts  table

Revision ID: 0786ab6ad17f
Revises: 4ed867317dca
Create Date: 2024-04-08 12:39:12.997453

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0786ab6ad17f'
down_revision: Union[str, None] = '4ed867317dca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
