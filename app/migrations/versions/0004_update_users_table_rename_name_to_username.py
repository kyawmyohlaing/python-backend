"""update users table rename name to username

Revision ID: 0004
Revises: 0003
Create Date: 2025-09-16 10:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None

def upgrade():
    # Rename the 'name' column to 'username' in the users table
    op.alter_column('users', 'name', new_column_name='username')

def downgrade():
    # Rename the 'username' column back to 'name' in the users table
    op.alter_column('users', 'username', new_column_name='name')