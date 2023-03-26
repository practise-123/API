"""users table

Revision ID: 65c9778718ac
Revises: 
Create Date: 2023-03-25 16:00:56.918353

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = '65c9778718ac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('uid', Integer, primary_key=True, autoincrement=True),
        sa.Column('username', String, unique=True, nullable=False),
        sa.Column('full_name', String),
        sa.Column('email', String),
        sa.Column('is_active', Boolean, default=True),
        sa.Column('hashed_password', String, nullable=False),
        sa.Column('last_updated_dt', Date, onupdate=func.now()),
        schema= "tasks-api"
    )


def downgrade() -> None:
    op.drop_table('users')
