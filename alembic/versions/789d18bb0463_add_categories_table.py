"""add_categories_table

Revision ID: 789d18bb0463
Revises: 060311cebf17
Create Date: 2026-04-26 20:56:32.288281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '789d18bb0463'
down_revision: Union[str, Sequence[str], None] = '060311cebf17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'categories',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=True),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('icon', sqlmodel.sql.sqltypes.AutoString(length=10), nullable=False),
        sa.Column('color', sqlmodel.sql.sqltypes.AutoString(length=9), nullable=False),
        sa.Column('is_system', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_categories_user_id', 'categories', ['user_id'], unique=False)

    # SQLite doesn't support ALTER TABLE ADD CONSTRAINT — batch mode does a copy-and-move
    with op.batch_alter_table('transactions') as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Uuid(), nullable=False))
        batch_op.create_index('ix_transactions_category_id', ['category_id'], unique=False)
        batch_op.create_foreign_key(
            'fk_transactions_category_id', 'categories', ['category_id'], ['id']
        )
        batch_op.drop_column('category')


def downgrade() -> None:
    with op.batch_alter_table('transactions') as batch_op:
        batch_op.add_column(sa.Column('category', sa.VARCHAR(), nullable=False))
        batch_op.drop_constraint('fk_transactions_category_id', type_='foreignkey')
        batch_op.drop_index('ix_transactions_category_id')
        batch_op.drop_column('category_id')

    op.drop_index('ix_categories_user_id', table_name='categories')
    op.drop_table('categories')
