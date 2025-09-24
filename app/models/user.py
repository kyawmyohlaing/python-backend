from sqlalchemy import Column, Integer, String, Enum, DateTime
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


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    WAITER = "waiter"
    CASHIER = "cashier"
    MANAGER = "manager"
    CHEF = "chef"
    KITCHEN = "kitchen"
    BAR = "bar"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # Fix the enum handling to properly map database values to Python enum
    role = Column(Enum(UserRole, values_callable=lambda x: [e.value for e in x], native_enum=False))
    progress = Column(String, default="{}")
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with orders (a user can create multiple orders)
    orders = relationship("Order", back_populates="created_by_user", lazy="select")
    
    # Many-to-many relationship with orders (staff users assigned to orders)
    assigned_orders = relationship("Order", secondary="order_staff_association", back_populates="staff_users", lazy="select")