from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Table
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


class IngredientCategory(str, enum.Enum):
    VEGETABLE = "vegetable"
    FRUIT = "fruit"
    MEAT = "meat"
    DAIRY = "dairy"
    GRAIN = "grain"
    SPICE = "spice"
    OTHER = "other"


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    category = Column(String)  # Using String instead of Enum for flexibility
    unit = Column(String)  # e.g., kg, g, L, mL, pieces
    current_stock = Column(Float, default=0.0)
    minimum_stock = Column(Float, default=0.0)  # Alert when stock falls below this level
    cost_per_unit = Column(Float, default=0.0)
    supplier = Column(String, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with menu items through association table
    menu_items = relationship("MenuItem", secondary="item_ingredients", back_populates="ingredients")


# Association table between MenuItem and Ingredient
item_ingredients = Table(
    "item_ingredients",
    Base.metadata,
    Column("menu_item_id", Integer, ForeignKey("menu_items.id")),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id")),
    Column("quantity", Float),  # Quantity of ingredient needed for this menu item
    Column("unit", String)  # Unit of measurement for this ingredient in this menu item
)


class StockTransactionType(str, enum.Enum):
    PURCHASE = "purchase"
    USAGE = "usage"
    WASTE = "waste"
    ADJUSTMENT = "adjustment"


class StockTransaction(Base):
    __tablename__ = "stock_transactions"

    id = Column(Integer, primary_key=True, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"))
    transaction_type = Column(String)  # Using String instead of Enum for flexibility
    quantity = Column(Float)
    unit = Column(String)
    cost = Column(Float, nullable=True)  # Cost for purchase transactions
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with ingredient
    ingredient = relationship("Ingredient", backref="transactions")