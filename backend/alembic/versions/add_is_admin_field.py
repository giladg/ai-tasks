"""Add is_admin field to users

Revision ID: add_is_admin_field
Revises: add_data_access_field
Create Date: 2026-01-27

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_is_admin_field'
down_revision = 'add_data_access_field'
branch_labels = None
depends_on = None


def upgrade():
    # Add is_admin field
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))

    # Set default value for existing users (all false)
    op.execute("UPDATE users SET is_admin = 0")

    # Make the column non-nullable with default False
    op.alter_column('users', 'is_admin',
               existing_type=sa.Boolean(),
               nullable=False,
               server_default='0')


def downgrade():
    # Remove is_admin field
    op.drop_column('users', 'is_admin')
