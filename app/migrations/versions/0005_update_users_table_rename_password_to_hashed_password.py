"""update users table rename password to hashed_password

Revision ID: 0005
Revises: 0004
Create Date: 2025-09-16 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = None

def upgrade():
    # Rename the 'password' column to 'hashed_password' in the users table
    op.alter_column('users', 'password', new_column_name='hashed_password')

def downgrade():
    # Rename the 'hashed_password' column back to 'password' in the users table
    op.alter_column('users', 'hashed_password', new_column_name='password')