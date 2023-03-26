"""adding fk

Revision ID: 41a292022db7
Revises: f1946cc7ca05
Create Date: 2023-03-25 17:37:16.642370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41a292022db7'
down_revision = 'f1946cc7ca05'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key(
                          source_schema='tasks-api',
                          referent_schema='tasks-api',
                          source_table='tasks',
                          referent_table='users',
                          constraint_name='fk_tasks_users',
                          local_cols=['uid'],
                          remote_cols=['uid']
                          )


def downgrade() -> None:
    op.drop_constraint(
        schema='tasks-api',
        constraint_name='fk_tasks_users')
