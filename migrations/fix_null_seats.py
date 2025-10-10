"""Migration script to fix tables with null seats values"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
import json

# revision identifiers
revision = 'fix_null_seats_001'
down_revision = 'create_stock_tables'  # Update this to match the latest migration
branch_labels = None
depends_on = None

def upgrade():
    """Fix tables that have null seats values"""
    # Get connection to database
    connection = op.get_bind()
    
    # Reflect the tables
    tables_table = table('tables',
        column('id', sa.Integer),
        column('table_number', sa.Integer),
        column('capacity', sa.Integer),
        column('seats', sa.JSON)
    )
    
    # Select all tables with null seats
    result = connection.execute(
        sa.select([tables_table.c.id, tables_table.c.table_number, tables_table.c.capacity])
        .where(tables_table.c.seats.is_(None))
    )
    
    # Update each table to have an empty seats array
    for row in result:
        table_id = row[0]
        table_number = row[1]
        capacity = row[2]
        
        print(f"Fixing table {table_id} (Table #{table_number}) with capacity {capacity}")
        
        # Initialize seats based on capacity
        seats = []
        for i in range(capacity):
            seats.append({
                "seat_number": i + 1,
                "status": "available",
                "customer_name": None
            })
        
        # Update the table record
        connection.execute(
            tables_table.update()
            .where(tables_table.c.id == table_id)
            .values(seats=json.dumps(seats))
        )
    
    print("Successfully fixed all tables with null seats")

def downgrade():
    """Downgrade - in this case, we don't need to do anything"""
    pass