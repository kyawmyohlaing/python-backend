from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.menu import MenuItem, MenuItemCreate, MenuItemResponse

router = APIRouter(prefix="/api/menu", tags=["Menu"])

@router.get("/", response_model=List[MenuItemResponse])
def get_menu_items(db: Session = Depends(get_db)):
    """Get all menu items from database"""
    menu_items = db.query(MenuItem).all()
    return menu_items

@router.post("/", response_model=MenuItemResponse)
def create_menu_item(menu_item: MenuItemCreate, db: Session = Depends(get_db)):
    """Create a new menu item"""
    db_item = MenuItem(**menu_item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/{item_id}", response_model=MenuItemResponse)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    """Get a specific menu item by ID"""
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return db_item

@router.put("/{item_id}", response_model=MenuItemResponse)
def update_menu_item(item_id: int, menu_item: MenuItemCreate, db: Session = Depends(get_db)):
    """Update a menu item"""
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    for key, value in menu_item.dict().items():
        setattr(db_item, key, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    """Delete a menu item"""
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Menu item deleted successfully"}