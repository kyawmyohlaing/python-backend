from typing import List

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.schemas.order_schema import OrderResponse
    from app.schemas.kitchen_schema import KitchenOrderResponse
    from app.schemas.table_schema import TableResponse
except ImportError:
    # Try importing directly (Docker container)
    from schemas.order_schema import OrderResponse
    from schemas.kitchen_schema import KitchenOrderResponse
    from schemas.table_schema import TableResponse

# Shared data storage - in a real application, this would be replaced with a database
sample_orders: List[OrderResponse] = []
sample_kitchen_orders: List[KitchenOrderResponse] = []
sample_tables: List[TableResponse] = [
    TableResponse(
        id=1,
        table_number=1,
        capacity=4,
        is_occupied=False,
        current_order_id=None,
        status="available"
    ),
    TableResponse(
        id=2,
        table_number=2,
        capacity=2,
        is_occupied=False,
        current_order_id=None,
        status="available"
    ),
    TableResponse(
        id=3,
        table_number=3,
        capacity=6,
        is_occupied=False,
        current_order_id=None,
        status="available"
    ),
    TableResponse(
        id=4,
        table_number=4,
        capacity=4,
        is_occupied=False,
        current_order_id=None,
        status="available"
    )
]