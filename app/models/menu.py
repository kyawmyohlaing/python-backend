from sqlalchemy import Column, Integer, String, Float
from database import Base
from pydantic import BaseModel
from typing import List

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    category = Column(String, index=True)

# Pydantic models for API validation
class MenuItemBase(BaseModel):
    name: str
    price: float
    category: str

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemResponse(MenuItemBase):
    id: int

    class Config:
        from_attributes = True