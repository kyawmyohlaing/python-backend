from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import get_db
    from app.models.menu import MenuItem
    from app.schemas.menu_schema import MenuItemCreate, MenuItemResponse
except ImportError:
    # Try importing directly (Docker container)
    from database import get_db
    from models.menu import MenuItem
    from schemas.menu_schema import MenuItemCreate, MenuItemResponse

router = APIRouter(prefix="/api/menu", tags=["Menu"])

@router.get("/", response_model=List[MenuItemResponse])
def get_menu_items(db: Session = Depends(get_db)):
    """Get all menu items from database"""
    menu_items = db.query(MenuItem).all()
    return menu_items

@router.post("/", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
def create_menu_item(menu_item: MenuItemCreate, db: Session = Depends(get_db)):
    """Create a new menu item"""
    # Check if item with same name already exists
    existing_item = db.query(MenuItem).filter(MenuItem.name == menu_item.name).first()
    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Menu item with name '{menu_item.name}' already exists"
        )
    
    try:
        db_item = MenuItem(**menu_item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating menu item: {str(e)}"
        )

# Specific routes must be defined before generic ones like /{item_id}
@router.get("/categories", response_model=List[str])
def get_menu_categories(db: Session = Depends(get_db)):
    """Get all unique menu categories"""
    categories = db.query(MenuItem.category).distinct().all()
    return [category[0] for category in categories]

@router.get("/category/{category}", response_model=List[MenuItemResponse])
def get_menu_items_by_category(category: str, db: Session = Depends(get_db)):
    """Get menu items by category"""
    menu_items = db.query(MenuItem).filter(MenuItem.category == category).all()
    return menu_items

@router.post("/batch", response_model=List[MenuItemResponse])
def create_menu_items_batch(menu_items: List[MenuItemCreate], db: Session = Depends(get_db)):
    """Create multiple menu items in batch"""
    created_items = []
    errors = []
    
    for i, menu_item in enumerate(menu_items):
        try:
            # Check if item with same name already exists
            existing_item = db.query(MenuItem).filter(MenuItem.name == menu_item.name).first()
            if existing_item:
                errors.append(f"Item {i+1}: Menu item with name '{menu_item.name}' already exists")
                continue
            
            db_item = MenuItem(**menu_item.dict())
            db.add(db_item)
            db.flush()  # Flush to get the ID without committing
            created_items.append(db_item)
        except Exception as e:
            errors.append(f"Item {i+1}: Error creating menu item '{menu_item.name}': {str(e)}")
    
    if errors:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Batch creation failed with errors: {'; '.join(errors)}"
        )
    
    try:
        db.commit()
        # Refresh all items to get their IDs
        for item in created_items:
            db.refresh(item)
        return created_items
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error committing batch creation: {str(e)}"
        )

# Generic routes must be defined AFTER specific ones
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
    
    # Check if another item with the same name already exists
    existing_item = db.query(MenuItem).filter(
        MenuItem.name == menu_item.name,
        MenuItem.id != item_id
    ).first()
    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Another menu item with name '{menu_item.name}' already exists"
        )
    
    try:
        for key, value in menu_item.dict().items():
            setattr(db_item, key, value)
        
        db.commit()
        db.refresh(db_item)
        return db_item
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating menu item: {str(e)}"
        )

@router.delete("/{item_id}")
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    """Delete a menu item"""
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    try:
        db.delete(db_item)
        db.commit()
        return {"message": "Menu item deleted successfully"}
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting menu item: {str(e)}"
        )