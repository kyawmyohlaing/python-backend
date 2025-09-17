from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002_add_order_type_fields'
down_revision = '001_initial'
branch_labels = None
depends_on = None

def upgrade():
    # Add new columns to support order type functionality
    op.add_column('orders', sa.Column('order_type', sa.String(length=20), nullable=True, server_default='dine_in'))
    op.add_column('orders', sa.Column('table_number', sa.String(length=10), nullable=True))
    op.add_column('orders', sa.Column('customer_name', sa.String(length=100), nullable=True))
    op.add_column('orders', sa.Column('customer_phone', sa.String(length=20), nullable=True))
    op.add_column('orders', sa.Column('delivery_address', sa.Text, nullable=True))
    
    # Update existing orders with default values
    op.execute("""
        UPDATE orders
        SET order_type = 'dine_in'
    """)
    
    # Alter columns to set nullable=False after migration
    op.alter_column('orders', 'order_type', nullable=False)


def downgrade():
    # Remove the new columns
    op.drop_column('orders', 'order_type')
    op.drop_column('orders', 'table_number')
    op.drop_column('orders', 'customer_name')
    op.drop_column('orders', 'customer_phone')
    op.drop_column('orders', 'delivery_address')