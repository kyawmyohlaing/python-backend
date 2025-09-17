from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.database (local development)
    from app.database import Base
except ImportError:
    # Try importing from database directly (Docker container)
    from database import Base


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    SERVED = "served"
    CANCELLED = "cancelled"


class OrderType(str, enum.Enum):
    DINE_IN = "dine_in"
    TAKEAWAY = "takeaway"
    DELIVERY = "delivery"


# Association table for order and users (many-to-many relationship)
order_staff_association = Table(
    "order_staff_association",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id")),
    Column("user_id", Integer, ForeignKey("users.id"))
)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    table_number = Column(Integer)
    order_type = Column(Enum(OrderType))
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    special_requests = Column(String, nullable=True)

    # Foreign key to User (the user who created the order)
    created_by = Column(Integer, ForeignKey("users.id"))

    # Relationships (using string references to avoid circular imports)
    order_items = relationship("OrderItem", back_populates="order", lazy="select")
    created_by_user = relationship("User", back_populates="orders", lazy="select")
    
    # Many-to-many relationship with staff users
    staff_users = relationship("User", secondary=order_staff_association, back_populates="assigned_orders", lazy="select")