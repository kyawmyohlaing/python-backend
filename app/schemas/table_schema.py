from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TableBase(BaseModel):
    table_number: int
    capacity: int

class TableCreate(TableBase):
    pass

class TableUpdate(BaseModel):
    table_number: Optional[int] = None
    capacity: Optional[int] = None
    is_occupied: Optional[bool] = None
    current_order_id: Optional[int] = None
    status: Optional[str] = None

class TableResponse(TableBase):
    id: int
    is_occupied: bool
    current_order_id: Optional[int] = None
    status: str

    class Config:
        from_attributes = True

class TableWithOrderDetails(TableResponse):
    order_details: Optional[dict] = None

    class Config:
        from_attributes = True