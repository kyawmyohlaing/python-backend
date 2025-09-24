from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.database import get_db
    from app.services.analytics_service import AnalyticsService
    from app.routes.user_routes import get_current_user
    from app.models.user import User, UserRole
    from app.schemas.analytics_schema import (
        SalesByEmployeeResponse,
        TipsByEmployeeResponse,
        UpsellingPerformanceResponse,
        EmployeePerformanceResponse
    )
except ImportError:
    # Try importing directly (Docker container)
    from database import get_db
    from services.analytics_service import AnalyticsService
    from routes.user_routes import get_current_user
    from models.user import User, UserRole
    from schemas.analytics_schema import (
        SalesByEmployeeResponse,
        TipsByEmployeeResponse,
        UpsellingPerformanceResponse,
        EmployeePerformanceResponse
    )

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/sales-by-employee", response_model=List[SalesByEmployeeResponse])
def get_sales_by_employee(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Get sales data by employee
    Only accessible by managers and admins
    """
    # Check if user has permission to view analytics
    if current_user.role not in [UserRole.MANAGER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access analytics"
        )
    
    return AnalyticsService.get_sales_by_employee(db, start_date, end_date)

@router.get("/tips-by-employee", response_model=List[TipsByEmployeeResponse])
def get_tips_by_employee(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Get tips data by employee
    Only accessible by managers and admins
    """
    # Check if user has permission to view analytics
    if current_user.role not in [UserRole.MANAGER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access analytics"
        )
    
    return AnalyticsService.get_tips_by_employee(db, start_date, end_date)

@router.get("/upselling-performance", response_model=List[UpsellingPerformanceResponse])
def get_upselling_performance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Get upselling performance by employee
    Only accessible by managers and admins
    """
    # Check if user has permission to view analytics
    if current_user.role not in [UserRole.MANAGER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access analytics"
        )
    
    return AnalyticsService.get_upselling_performance(db, start_date, end_date)

@router.get("/employee/{employee_id}/performance", response_model=EmployeePerformanceResponse)
def get_employee_performance(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Get comprehensive performance summary for a specific employee
    Only accessible by managers and admins
    """
    # Check if user has permission to view analytics
    if current_user.role not in [UserRole.MANAGER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access analytics"
        )
    
    performance = AnalyticsService.get_employee_performance_summary(db, employee_id, start_date, end_date)
    if not performance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )
    
    return performance