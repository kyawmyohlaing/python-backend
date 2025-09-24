from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SalesByEmployeeResponse(BaseModel):
    employee_id: int
    username: str
    full_name: Optional[str]
    role: str
    order_count: int
    total_sales: float
    average_order_value: float
    
    class Config:
        from_attributes = True

class TipsByEmployeeResponse(BaseModel):
    employee_id: int
    username: str
    full_name: Optional[str]
    role: str
    total_tips: float
    tip_count: int
    
    class Config:
        from_attributes = True

class UpsellingPerformanceResponse(BaseModel):
    employee_id: int
    username: str
    full_name: Optional[str]
    role: str
    upsell_count: int
    upsell_revenue: float
    
    class Config:
        from_attributes = True

class EmployeePerformanceResponse(BaseModel):
    employee_id: int
    username: str
    full_name: Optional[str]
    role: str
    order_count: int
    total_sales: float
    average_order_value: float
    total_tips: float
    upsell_count: int
    
    class Config:
        from_attributes = True