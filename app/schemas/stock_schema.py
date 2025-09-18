from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class IngredientBase(BaseModel):
    name: str
    category: Optional[str] = "other"
    unit: str
    current_stock: float = 0.0
    minimum_stock: float = 0.0
    cost_per_unit: float = 0.0
    supplier: Optional[str] = None

class IngredientCreate(IngredientBase):
    pass

class IngredientUpdate(IngredientBase):
    name: Optional[str] = None
    unit: Optional[str] = None

class IngredientResponse(IngredientBase):
    id: int
    last_updated: datetime

    class Config:
        from_attributes = True

class ItemIngredientBase(BaseModel):
    menu_item_id: int
    ingredient_id: int
    quantity: float
    unit: str

class ItemIngredientCreate(ItemIngredientBase):
    pass

class ItemIngredientUpdate(BaseModel):
    quantity: Optional[float] = None
    unit: Optional[str] = None

class ItemIngredientResponse(ItemIngredientBase):
    class Config:
        from_attributes = True

class StockTransactionBase(BaseModel):
    ingredient_id: int
    transaction_type: str
    quantity: float
    unit: str
    cost: Optional[float] = None
    notes: Optional[str] = None

class StockTransactionCreate(StockTransactionBase):
    pass

class StockTransactionUpdate(BaseModel):
    transaction_type: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    cost: Optional[float] = None
    notes: Optional[str] = None

class StockTransactionResponse(StockTransactionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class LowStockAlert(BaseModel):
    ingredient_id: int
    name: str
    current_stock: float
    minimum_stock: float
    unit: str