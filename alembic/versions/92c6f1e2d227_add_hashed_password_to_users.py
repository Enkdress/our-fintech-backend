"""add_hashed_password_to_users

Revision ID: 92c6f1e2d227
Revises: 789d18bb0463
Create Date: 2026-04-26 21:09:03.474523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '92c6f1e2d227'
down_revision: Union[str, Sequence[str], None] = '789d18bb0463'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False, server_default=''))


def downgrade() -> None:
    with op.batch_alter_table('users') as batch_op:
        batch_op.drop_column('hashed_password')
