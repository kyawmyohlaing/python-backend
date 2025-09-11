from typing import List
from models.order import OrderResponse
from models.kitchen import KitchenOrderResponse
from models.table import TableResponse

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
        status="available",
        seats=[{"status": "available", "customer_name": None} for _ in range(4)]
    ),
    TableResponse(
        id=2,
        table_number=2,
        capacity=2,
        is_occupied=False,
        current_order_id=None,
        status="available",
        seats=[{"status": "available", "customer_name": None} for _ in range(2)]
    ),
    TableResponse(
        id=3,
        table_number=3,
        capacity=6,
        is_occupied=False,
        current_order_id=None,
        status="available",
        seats=[{"status": "available", "customer_name": None} for _ in range(6)]
    ),
    TableResponse(
        id=4,
        table_number=4,
        capacity=4,
        is_occupied=False,
        current_order_id=None,
        status="available",
        seats=[{"status": "available", "customer_name": None} for _ in range(4)]
    )
]