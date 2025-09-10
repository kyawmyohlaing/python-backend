from pydantic import BaseModel
from typing import List

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