from sqlalchemy import Column, Integer, String, Float, Enum
from sqlalchemy.orm import relationship
import enum

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.database (local development)
    from app.database import Base
except ImportError:
    # Try importing from database directly (Docker container)
    from database import Base


class MenuItemCategory(str, enum.Enum):
    FOOD = "food"
    DRINK = "drink"
    ALCOHOL = "alcohol"


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    category = Column(Enum(MenuItemCategory))

    # Relationship with order items (using string reference to avoid circular imports)
    order_items = relationship("OrderItem", back_populates="menu_item", lazy="select")