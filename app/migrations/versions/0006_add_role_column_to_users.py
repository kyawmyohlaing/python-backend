"""add role column to users

Revision ID: 0006
Revises: 0005
Create Date: 2025-09-16 10:35:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0006'
down_revision = '0005'
branch_labels = None
depends_on = None

def upgrade():
    # Create the enum type first
    user_role_enum = sa.Enum('admin', 'waiter', 'cashier', 'manager', 'chef', 'kitchen', 'bar', name='userrole')
    user_role_enum.create(op.get_bind())
    
    # Add the 'role' column to the users table
    op.add_column('users', sa.Column('role', sa.Enum('admin', 'waiter', 'cashier', 'manager', 'chef', 'kitchen', 'bar', name='userrole'), nullable=True))

def downgrade():
    # Remove the 'role' column from the users table
    op.drop_column('users', 'role')
    
    # Drop the enum type
    user_role_enum = sa.Enum('admin', 'waiter', 'cashier', 'manager', 'chef', 'kitchen', 'bar', name='userrole')
    user_role_enum.drop(op.get_bind())