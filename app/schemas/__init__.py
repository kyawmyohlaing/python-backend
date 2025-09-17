# Import all schema classes for easier imports
from .user_schema import UserCreate, UserResponse, UserLogin, Token
from .menu_schema import MenuItemBase, MenuItemCreate, MenuItemResponse
from .order_schema import OrderItem, OrderBase, OrderCreate, OrderUpdate, OrderResponse
from .table_schema import TableBase, TableCreate, TableUpdate, TableResponse
from .invoice_schema import InvoiceItem, InvoiceBase, InvoiceCreate, InvoiceUpdate, InvoiceResponse
from .kitchen_schema import KitchenOrderBase, KitchenOrderCreate, KitchenOrderUpdate, KitchenOrderResponse, KitchenOrderDetail

__all__ = [
    "UserCreate", "UserResponse", "UserLogin", "Token",
    "MenuItemBase", "MenuItemCreate", "MenuItemResponse",
    "OrderItem", "OrderBase", "OrderCreate", "OrderUpdate", "OrderResponse",
    "TableBase", "TableCreate", "TableUpdate", "TableResponse",
    "InvoiceItem", "InvoiceBase", "InvoiceCreate", "InvoiceUpdate", "InvoiceResponse",
    "KitchenOrderBase", "KitchenOrderCreate", "KitchenOrderUpdate", "KitchenOrderResponse", "KitchenOrderDetail"
]