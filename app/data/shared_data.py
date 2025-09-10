from typing import List
from models.order import OrderResponse
from models.kitchen import KitchenOrderResponse

# Shared data storage - in a real application, this would be replaced with a database
sample_orders: List[OrderResponse] = []
sample_kitchen_orders: List[KitchenOrderResponse] = []