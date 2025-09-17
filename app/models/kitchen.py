from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import List
import enum

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.database (local development)
    from app.database import Base
except ImportError:
    # Try importing from database directly (Docker container)
    from database import Base

# Import the schema for MenuItemBase (it's a Pydantic model, not a SQLAlchemy model)
try:
    # Try importing from app.schemas (local development)
    from app.schemas.menu_schema import MenuItemBase
except ImportError:
    # Try importing from schemas directly (Docker container)
    from schemas.menu_schema import MenuItemBase


class KitchenOrderStatus(str, enum.Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"


class KitchenOrder(Base):
    __tablename__ = "kitchen_orders"

    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(Integer)
    order_type = Column(String)  # dine_in, takeaway, delivery
    status = Column(String, default=KitchenOrderStatus.PENDING.value)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Store order items as JSON (since they're Pydantic models, not SQLAlchemy models)
    # This is a simplified approach for demonstration
    # In a real application, you might want to create a separate table for order items