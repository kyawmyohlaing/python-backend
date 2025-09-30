"""Add payment_type column to invoices table

Revision ID: 0013
Revises: 0012
Create Date: 2025-09-30 10:05:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0013'
down_revision = '0012'
branch_labels = None
depends_on = None

def upgrade():
    # Add payment_type column to invoices table
    op.add_column('invoices', sa.Column('payment_type', sa.String(length=20), server_default='cash', nullable=True))

def downgrade():
    # Remove payment_type column from invoices table
    op.drop_column('invoices', 'payment_type')