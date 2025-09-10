from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.menu import MenuItem, MenuItemCreate, MenuItemResponse

router = APIRouter(prefix="/api/menu", tags=["Menu"])

# Sample menu data - in a real application, this would come from a database
sample_menu_items = [
    {"id": 1, "name": "Shan Noodles", "price": 2.5, "category": "Myanmar Food"},
    {"id": 2, "name": "Mohinga", "price": 2.0, "category": "Myanmar Food"},
    {"id": 3, "name": "Tea Leaf Salad", "price": 3.0, "category": "Myanmar Food"},
    {"id": 4, "name": "Chicken Curry", "price": 4.5, "category": "Myanmar Food"},
]

@router.get("/", response_model=List[MenuItemResponse])
def get_menu_items():
    """Get all menu items"""
    return sample_menu_items

@router.post("/", response_model=MenuItemResponse)
def create_menu_item(menu_item: MenuItemCreate):
    """Create a new menu item"""
    # In a real application, this would save to the database
    new_id = len(sample_menu_items) + 1
    new_item = MenuItemResponse(
        id=new_id,
        name=menu_item.name,
        price=menu_item.price,
        category=menu_item.category
    )
    sample_menu_items.append(new_item.dict())
    return new_item