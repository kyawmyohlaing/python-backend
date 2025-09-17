from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
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
    KITCHEN = "kitchen"
    BAR = "bar"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole))

    # Relationship with orders (a user can create multiple orders)
    orders = relationship("Order", back_populates="created_by_user", lazy="select")
    
    # Many-to-many relationship with orders (staff users assigned to orders)
    assigned_orders = relationship("Order", secondary="order_staff_association", back_populates="staff_users", lazy="select")