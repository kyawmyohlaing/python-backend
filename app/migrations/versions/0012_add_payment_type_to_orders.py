"""Add payment_type column to orders table

Revision ID: 0012
Revises: 0011
Create Date: 2025-09-30 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0012'
down_revision = '0011'
branch_labels = None
depends_on = None

def upgrade():
    # Check if the enum type already exists
    connection = op.get_bind()
    result = connection.execute(sa.text("""
        SELECT 1 FROM pg_type WHERE typname = 'paymenttype'
    """))
    
    if not result.fetchone():
        # Create the enum type only if it doesn't exist
        paymenttype_enum = sa.Enum('cash', 'card', 'qr', 'e_wallet', 'gift_card', name='paymenttype')
        paymenttype_enum.create(op.get_bind())
    
    # Add payment_type column to orders table without default value first
    op.add_column('orders', sa.Column('payment_type', sa.Enum('cash', 'card', 'qr', 'e_wallet', 'gift_card', name='paymenttype'), nullable=True))

def downgrade():
    # Remove payment_type column from orders table
    op.drop_column('orders', 'payment_type')
    # Drop the enum type if it exists
    op.execute("DROP TYPE IF EXISTS paymenttype")