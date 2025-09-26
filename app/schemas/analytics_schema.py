from pydantic import BaseModel
from typing import Optional, List
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

# New schemas for sales reports
class SalesReportItem(BaseModel):
    date: datetime
    total_sales: float
    order_count: int
    average_order_value: float
    
    class Config:
        from_attributes = True

class DailySalesReportResponse(BaseModel):
    period: str  # "daily"
    start_date: datetime
    end_date: datetime
    total_sales: float
    total_orders: int
    average_daily_sales: float
    sales_data: List[SalesReportItem]
    
    class Config:
        from_attributes = True

class WeeklySalesReportResponse(BaseModel):
    period: str  # "weekly"
    start_date: datetime
    end_date: datetime
    total_sales: float
    total_orders: int
    average_weekly_sales: float
    sales_data: List[SalesReportItem]
    
    class Config:
        from_attributes = True

class MonthlySalesReportResponse(BaseModel):
    period: str  # "monthly"
    start_date: datetime
    end_date: datetime
    total_sales: float
    total_orders: int
    average_monthly_sales: float
    sales_data: List[SalesReportItem]
    
    class Config:
        from_attributes = True