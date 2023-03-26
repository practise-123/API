"""tasks table

Revision ID: f1946cc7ca05
Revises: 65c9778718ac
Create Date: 2023-03-25 17:28:34.686587

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = 'f1946cc7ca05'
down_revision = '65c9778718ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column('tid', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.String),
        sa.Column('status',sa.String),
        sa.Column('created_dt',sa.Date, nullable=False, server_default=func.now()),
        sa.Column('last_updated_dt', sa.Date, nullable=False, onupdate=func.now()),
        sa.Column('uid', sa.Integer, nullable=False,),
        schema= 'tasks-api'
                    )
def downgrade() -> None:
    op.drop_table('tasks')
