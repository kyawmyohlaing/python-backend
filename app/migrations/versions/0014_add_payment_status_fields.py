"""Add payment status fields to orders table

Revision ID: 0014
Revises: 0013
Create Date: 2025-10-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0014'
down_revision = '0013'
branch_labels = None
depends_on = None

def upgrade():
    # Add payment status fields to orders table
    op.add_column('orders', sa.Column('payment_status', sa.String(length=20), server_default='pending', nullable=True))
    op.add_column('orders', sa.Column('paid_at', sa.DateTime(), nullable=True))
    op.add_column('orders', sa.Column('payment_reference', sa.String(length=100), nullable=True))
    op.add_column('orders', sa.Column('refund_status', sa.String(length=20), nullable=True))
    op.add_column('orders', sa.Column('refunded_at', sa.DateTime(), nullable=True))

def downgrade():
    # Remove payment status fields from orders table
    op.drop_column('orders', 'refunded_at')
    op.drop_column('orders', 'refund_status')
    op.drop_column('orders', 'payment_reference')
    op.drop_column('orders', 'paid_at')
    op.drop_column('orders', 'payment_status')