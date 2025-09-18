from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import get_db
    from app.models.stock import Ingredient, StockTransaction, item_ingredients
    from app.models.menu import MenuItem
    from app.schemas.stock_schema import (
        IngredientCreate, IngredientUpdate, IngredientResponse,
        StockTransactionCreate, StockTransactionResponse, LowStockAlert
    )
except ImportError:
    # Try importing directly (Docker container)
    from database import get_db
    from models.stock import Ingredient, StockTransaction, item_ingredients
    from models.menu import MenuItem
    from schemas.stock_schema import (
        IngredientCreate, IngredientUpdate, IngredientResponse,
        StockTransactionCreate, StockTransactionResponse, LowStockAlert
    )

router = APIRouter(prefix="/api/stock", tags=["Stock Management"])

@router.get("/ingredients", response_model=List[IngredientResponse])
def get_ingredients(db: Session = Depends(get_db)):
    """Get all ingredients"""
    ingredients = db.query(Ingredient).all()
    return ingredients

@router.get("/ingredients/{ingredient_id}", response_model=IngredientResponse)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    """Get a specific ingredient by ID"""
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient

@router.post("/ingredients", response_model=IngredientResponse)
def create_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    """Create a new ingredient"""
    # Check if ingredient with this name already exists
    existing_ingredient = db.query(Ingredient).filter(Ingredient.name == ingredient.name).first()
    if existing_ingredient:
        raise HTTPException(status_code=400, detail="Ingredient with this name already exists")
    
    db_ingredient = Ingredient(**ingredient.dict())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

@router.put("/ingredients/{ingredient_id}", response_model=IngredientResponse)
def update_ingredient(ingredient_id: int, ingredient_update: IngredientUpdate, db: Session = Depends(get_db)):
    """Update an existing ingredient"""
    db_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    # Update only provided fields
    for field, value in ingredient_update.dict(exclude_unset=True).items():
        setattr(db_ingredient, field, value)
    
    db_ingredient.last_updated = datetime.utcnow()
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

@router.delete("/ingredients/{ingredient_id}")
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    """Delete an ingredient"""
    db_ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    db.delete(db_ingredient)
    db.commit()
    return {"message": "Ingredient deleted successfully"}

@router.get("/low-stock", response_model=List[LowStockAlert])
def get_low_stock_alerts(db: Session = Depends(get_db)):
    """Get all ingredients that are below minimum stock level"""
    low_stock_ingredients = db.query(Ingredient).filter(
        Ingredient.current_stock <= Ingredient.minimum_stock
    ).all()
    
    alerts = []
    for ingredient in low_stock_ingredients:
        alerts.append(LowStockAlert(
            ingredient_id=ingredient.id,
            name=ingredient.name,
            current_stock=ingredient.current_stock,
            minimum_stock=ingredient.minimum_stock,
            unit=ingredient.unit
        ))
    
    return alerts

@router.post("/transactions", response_model=StockTransactionResponse)
def create_stock_transaction(transaction: StockTransactionCreate, db: Session = Depends(get_db)):
    """Create a new stock transaction and update ingredient stock level"""
    # Check if ingredient exists
    ingredient = db.query(Ingredient).filter(Ingredient.id == transaction.ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    # Create transaction
    db_transaction = StockTransaction(**transaction.dict())
    db.add(db_transaction)
    
    # Update ingredient stock based on transaction type
    if transaction.transaction_type == "purchase":
        ingredient.current_stock += transaction.quantity
    elif transaction.transaction_type == "usage":
        ingredient.current_stock -= transaction.quantity
    elif transaction.transaction_type == "waste":
        ingredient.current_stock -= transaction.quantity
    elif transaction.transaction_type == "adjustment":
        ingredient.current_stock = transaction.quantity
    
    ingredient.last_updated = datetime.utcnow()
    
    db.commit()
    db.refresh(db_transaction)
    db.refresh(ingredient)
    
    return db_transaction

@router.get("/transactions", response_model=List[StockTransactionResponse])
def get_stock_transactions(db: Session = Depends(get_db)):
    """Get all stock transactions"""
    transactions = db.query(StockTransaction).all()
    return transactions

@router.get("/transactions/ingredient/{ingredient_id}", response_model=List[StockTransactionResponse])
def get_ingredient_transactions(ingredient_id: int, db: Session = Depends(get_db)):
    """Get all transactions for a specific ingredient"""
    transactions = db.query(StockTransaction).filter(
        StockTransaction.ingredient_id == ingredient_id
    ).all()
    return transactions

@router.post("/menu-items/{menu_item_id}/ingredients/{ingredient_id}")
def add_ingredient_to_menu_item(menu_item_id: int, ingredient_id: int, quantity: float, unit: str, db: Session = Depends(get_db)):
    """Add an ingredient to a menu item"""
    # Check if menu item exists
    menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Check if ingredient exists
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    
    # Check if association already exists
    existing_association = db.query(item_ingredients).filter(
        item_ingredients.c.menu_item_id == menu_item_id,
        item_ingredients.c.ingredient_id == ingredient_id
    ).first()
    
    if existing_association:
        raise HTTPException(status_code=400, detail="Ingredient already associated with this menu item")
    
    # Create association
    stmt = item_ingredients.insert().values(
        menu_item_id=menu_item_id,
        ingredient_id=ingredient_id,
        quantity=quantity,
        unit=unit
    )
    db.execute(stmt)
    db.commit()
    
    return {"message": "Ingredient added to menu item successfully"}

@router.delete("/menu-items/{menu_item_id}/ingredients/{ingredient_id}")
def remove_ingredient_from_menu_item(menu_item_id: int, ingredient_id: int, db: Session = Depends(get_db)):
    """Remove an ingredient from a menu item"""
    # Check if association exists
    existing_association = db.query(item_ingredients).filter(
        item_ingredients.c.menu_item_id == menu_item_id,
        item_ingredients.c.ingredient_id == ingredient_id
    ).first()
    
    if not existing_association:
        raise HTTPException(status_code=404, detail="Ingredient not associated with this menu item")
    
    # Remove association
    stmt = item_ingredients.delete().where(
        item_ingredients.c.menu_item_id == menu_item_id,
        item_ingredients.c.ingredient_id == ingredient_id
    )
    db.execute(stmt)
    db.commit()
    
    return {"message": "Ingredient removed from menu item successfully"}