"""Add has_data_access field to users

Revision ID: add_data_access_field
Revises:
Create Date: 2026-01-27

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_data_access_field'
down_revision = None  # Update this if there's a previous revision
branch_labels = None
depends_on = None


def upgrade():
    # Make token fields nullable
    op.alter_column('users', 'access_token',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('users', 'refresh_token',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('users', 'token_expires_at',
               existing_type=sa.DateTime(),
               nullable=True)

    # Add has_data_access field
    op.add_column('users', sa.Column('has_data_access', sa.Boolean(), nullable=True))

    # Set default value for existing users (assume they have data access if they have tokens)
    op.execute("UPDATE users SET has_data_access = (access_token IS NOT NULL AND refresh_token IS NOT NULL)")

    # Make the column non-nullable with default False
    op.alter_column('users', 'has_data_access',
               existing_type=sa.Boolean(),
               nullable=False,
               server_default='0')


def downgrade():
    # Remove has_data_access field
    op.drop_column('users', 'has_data_access')

    # Revert token fields to non-nullable (this might fail if there are NULL values)
    op.alter_column('users', 'access_token',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('users', 'refresh_token',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('users', 'token_expires_at',
               existing_type=sa.DateTime(),
               nullable=False)
