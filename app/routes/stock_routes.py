from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from collections import defaultdict

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

# Add the missing GET endpoint for fetching menu item ingredients
@router.get("/menu-items/{menu_item_id}/ingredients", response_model=List[dict])
def get_menu_item_ingredients(menu_item_id: int, db: Session = Depends(get_db)):
    """Get all ingredients for a menu item"""
    # Check if menu item exists
    menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Query the association table to get ingredients for this menu item
    ingredients_query = db.query(
        item_ingredients.c.ingredient_id,
        Ingredient.name,
        item_ingredients.c.quantity,
        item_ingredients.c.unit
    ).select_from(item_ingredients.join(Ingredient)).filter(
        item_ingredients.c.menu_item_id == menu_item_id
    )
    
    ingredients = ingredients_query.all()
    
    # Convert to response format
    result = []
    for ingredient in ingredients:
        result.append({
            "ingredient_id": ingredient.ingredient_id,
            "name": ingredient.name,
            "quantity": ingredient.quantity,
            "unit": ingredient.unit
        })
    
    return result

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

# Stock Analytics Endpoints
@router.get("/analytics/usage")
def get_stock_usage_analytics(db: Session = Depends(get_db)):
    """Get stock usage analytics"""
    # Get all usage transactions (transactions with type 'usage')
    usage_transactions = db.query(StockTransaction).filter(
        StockTransaction.transaction_type == "usage"
    ).all()
    
    # Aggregate usage by ingredient
    usage_data = defaultdict(lambda: {
        "quantity_used": 0.0,
        "unit": ""
    })
    
    for transaction in usage_transactions:
        usage_data[transaction.ingredient_id]["quantity_used"] += transaction.quantity
        usage_data[transaction.ingredient_id]["unit"] = transaction.unit
    
    # Get ingredient details
    ingredient_ids = list(usage_data.keys())
    ingredients = db.query(Ingredient).filter(Ingredient.id.in_(ingredient_ids)).all()
    
    # Create result data
    result_data = []
    for ingredient in ingredients:
        usage_info = usage_data.get(ingredient.id, {"quantity_used": 0.0, "unit": ""})
        result_data.append({
            "ingredient_id": ingredient.id,
            "name": ingredient.name,
            "category": ingredient.category,
            "quantity_used": round(usage_info["quantity_used"], 2),
            "unit": usage_info["unit"]
        })
    
    # Sort by quantity used (descending)
    result_data.sort(key=lambda x: x["quantity_used"], reverse=True)
    
    # Find highest and lowest usage items
    highest_usage_item = result_data[0] if result_data else None
    lowest_usage_item = result_data[-1] if result_data else None
    
    return {
        "total_ingredients": len(result_data),
        "highest_usage_item": highest_usage_item,
        "lowest_usage_item": lowest_usage_item,
        "usage_data": result_data
    }

@router.get("/analytics/costs")
def get_cost_analysis(db: Session = Depends(get_db)):
    """Get cost analysis for all ingredients"""
    ingredients = db.query(Ingredient).all()
    
    cost_data = []
    for ingredient in ingredients:
        total_cost = ingredient.current_stock * ingredient.cost_per_unit
        cost_data.append({
            "ingredient_id": ingredient.id,
            "name": ingredient.name,
            "category": ingredient.category,
            "current_stock": ingredient.current_stock,
            "unit": ingredient.unit,
            "cost_per_unit": ingredient.cost_per_unit,
            "total_cost": round(total_cost, 2)
        })
    
    # Sort by total cost (descending)
    cost_data.sort(key=lambda x: x["total_cost"], reverse=True)
    
    # Find highest value item
    highest_value_item = cost_data[0] if cost_data else None
    
    return {
        "total_ingredients": len(cost_data),
        "highest_value_item": highest_value_item,
        "cost_data": cost_data
    }

@router.get("/analytics/trends")
def get_stock_trends(db: Session = Depends(get_db)):
    """Get stock trend analysis"""
    # Get all transactions from the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_transactions = db.query(StockTransaction).filter(
        StockTransaction.created_at >= thirty_days_ago
    ).all()
    
    # Group transactions by ingredient and calculate trends
    trend_data = defaultdict(list)
    for transaction in recent_transactions:
        trend_data[transaction.ingredient_id].append({
            "date": transaction.created_at.date(),
            "quantity": transaction.quantity,
            "type": transaction.transaction_type
        })
    
    # Calculate current and previous stock levels for each ingredient
    ingredient_ids = list(trend_data.keys())
    ingredients = db.query(Ingredient).filter(Ingredient.id.in_(ingredient_ids)).all()
    
    result_data = []
    for ingredient in ingredients:
        # Get current stock
        current_stock = ingredient.current_stock
        
        # Calculate previous stock (30 days ago)
        # This is a simplified calculation - in a real system, you'd want to look at actual historical data
        transactions = trend_data.get(ingredient.id, [])
        stock_change = 0
        for transaction in transactions:
            if transaction["type"] == "purchase":
                stock_change += transaction["quantity"]
            elif transaction["type"] in ["usage", "waste"]:
                stock_change -= transaction["quantity"]
        
        previous_stock = current_stock - stock_change
        
        # Determine trend
        if current_stock > previous_stock:
            trend = "increasing"
        elif current_stock < previous_stock:
            trend = "decreasing"
        else:
            trend = "stable"
        
        # Calculate change percentage
        change_percentage = 0
        if previous_stock != 0:
            change_percentage = ((current_stock - previous_stock) / previous_stock) * 100
        
        result_data.append({
            "ingredient_id": ingredient.id,
            "name": ingredient.name,
            "category": ingredient.category,
            "current_stock": current_stock,
            "previous_stock": round(previous_stock, 2),
            "trend": trend,
            "change_percentage": round(change_percentage, 2)
        })
    
    # Count trends
    increasing_trends = sum(1 for item in result_data if item["trend"] == "increasing")
    decreasing_trends = sum(1 for item in result_data if item["trend"] == "decreasing")
    stable_trends = sum(1 for item in result_data if item["trend"] == "stable")
    
    # Sort by change percentage (descending)
    result_data.sort(key=lambda x: x["change_percentage"], reverse=True)
    
    return {
        "total_ingredients": len(result_data),
        "increasing_trends": increasing_trends,
        "decreasing_trends": decreasing_trends,
        "stable_trends": stable_trends,
        "trend_data": result_data
    }

@router.get("/analytics/suppliers")
def get_supplier_performance(db: Session = Depends(get_db)):
    """Get supplier performance analysis"""
    # Group ingredients by supplier
    suppliers = defaultdict(list)
    ingredients = db.query(Ingredient).all()
    
    for ingredient in ingredients:
        supplier_name = ingredient.supplier or "No Supplier"
        suppliers[supplier_name].append(ingredient)
    
    # Calculate performance metrics for each supplier
    supplier_data = []
    for supplier, supplier_ingredients in suppliers.items():
        item_count = len(supplier_ingredients)
        total_value = sum(ingredient.current_stock * ingredient.cost_per_unit for ingredient in supplier_ingredients)
        avg_cost = total_value / item_count if item_count > 0 else 0
        
        # Determine performance rating (simplified)
        if avg_cost < 5:
            performance = "excellent"
        elif avg_cost < 10:
            performance = "good"
        elif avg_cost < 20:
            performance = "average"
        else:
            performance = "poor"
        
        supplier_data.append({
            "supplier": supplier,
            "item_count": item_count,
            "total_value": round(total_value, 2),
            "avg_cost": round(avg_cost, 2),
            "performance": performance
        })
    
    # Sort by item count (descending)
    supplier_data.sort(key=lambda x: x["item_count"], reverse=True)
    
    # Find top supplier
    top_supplier = supplier_data[0] if supplier_data else None
    
    # Calculate average items per supplier
    avg_items_per_supplier = sum(item["item_count"] for item in supplier_data) / len(supplier_data) if supplier_data else 0
    
    return {
        "total_suppliers": len(supplier_data),
        "top_supplier": top_supplier,
        "avg_items_per_supplier": round(avg_items_per_supplier, 1),
        "supplier_data": supplier_data
    }