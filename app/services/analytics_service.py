from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

# Handle imports for both local development and Docker container environments
try:
    # Try importing from app.module (local development)
    from app.models.order import Order
    from app.models.order_item import OrderItem
    from app.models.user import User, UserRole
    from app.models.menu import MenuItem
    from app.schemas.analytics_schema import (
        SalesByEmployeeResponse,
        TipsByEmployeeResponse,
        UpsellingPerformanceResponse,
        EmployeePerformanceResponse
    )
except ImportError:
    # Try importing directly (Docker container)
    from models.order import Order
    from models.order_item import OrderItem
    from models.user import User, UserRole
    from models.menu import MenuItem
    from schemas.analytics_schema import (
        SalesByEmployeeResponse,
        TipsByEmployeeResponse,
        UpsellingPerformanceResponse,
        EmployeePerformanceResponse
    )


class AnalyticsService:
    @staticmethod
    def get_sales_by_employee(db: Session, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[SalesByEmployeeResponse]:
        """
        Get sales data by employee including total sales, order count, and average order value
        """
        try:
            # Build query with date filters if provided
            query = db.query(
                User.id,
                User.username,
                User.full_name,
                User.role,
                func.count(Order.id).label('order_count'),
                func.sum(Order.total).label('total_sales'),
                func.avg(Order.total).label('average_order_value')
            ).join(Order, Order.created_by == User.id, isouter=True)\
             .filter(User.role.in_([UserRole.WAITER, UserRole.CASHIER, UserRole.BAR]))
            
            if start_date:
                query = query.filter(Order.created_at >= start_date)
            if end_date:
                query = query.filter(Order.created_at <= end_date)
                
            results = query.group_by(User.id, User.username, User.full_name, User.role)\
                          .order_by(func.sum(Order.total).desc())\
                          .all()
            
            # Format results
            sales_data = []
            for result in results:
                try:
                    # Create a dictionary with the values
                    data_dict = {
                        'employee_id': int(result.id) if result.id is not None else 0,
                        'username': str(result.username) if result.username is not None else "",
                        'full_name': str(result.full_name) if result.full_name is not None else None,
                        'role': str(result.role.value) if result.role is not None and hasattr(result.role, 'value') else "",
                        'order_count': int(result.order_count) if result.order_count is not None else 0,
                        'total_sales': float(result.total_sales) if result.total_sales is not None else 0.0,
                        'average_order_value': float(result.average_order_value) if result.average_order_value is not None else 0.0
                    }
                    
                    sales_data.append(SalesByEmployeeResponse(**data_dict))
                except Exception:
                    # Skip records that can't be processed
                    continue
                
            return sales_data
        except Exception:
            # Return empty list if query fails
            return []

    @staticmethod
    def get_tips_by_employee(db: Session, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[TipsByEmployeeResponse]:
        """
        Get tip data by employee (placeholder - would need actual tip tracking implementation)
        """
        try:
            # This is a placeholder as the current schema doesn't have tip tracking
            # In a real implementation, you would have a tips table or tip field in orders
            employees = db.query(User).filter(User.role.in_([UserRole.WAITER, UserRole.BAR])).all()
            
            tips_data = []
            for employee in employees:
                try:
                    data_dict = {
                        'employee_id': int(employee.id) if employee.id is not None else 0,
                        'username': str(employee.username) if employee.username is not None else "",
                        'full_name': str(employee.full_name) if employee.full_name is not None else None,
                        'role': str(employee.role.value) if employee.role is not None and hasattr(employee.role, 'value') else "",
                        'total_tips': 0,  # Placeholder
                        'tip_count': 0    # Placeholder
                    }
                    
                    tips_data.append(TipsByEmployeeResponse(**data_dict))
                except Exception:
                    # Skip records that can't be processed
                    continue
                
            return tips_data
        except Exception:
            # Return empty list if query fails
            return []

    @staticmethod
    def get_upselling_performance(db: Session, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[UpsellingPerformanceResponse]:
        """
        Get upselling performance by employee (placeholder - would need menu item category tracking)
        """
        try:
            # This would require tracking which items were suggested/upsold
            # For now, we'll return placeholder data
            employees = db.query(User).filter(User.role.in_([UserRole.WAITER, UserRole.BAR])).all()
            
            upselling_data = []
            for employee in employees:
                try:
                    data_dict = {
                        'employee_id': int(employee.id) if employee.id is not None else 0,
                        'username': str(employee.username) if employee.username is not None else "",
                        'full_name': str(employee.full_name) if employee.full_name is not None else None,
                        'role': str(employee.role.value) if employee.role is not None and hasattr(employee.role, 'value') else "",
                        'upsell_count': 0,      # Placeholder
                        'upsell_revenue': 0     # Placeholder
                    }
                    
                    upselling_data.append(UpsellingPerformanceResponse(**data_dict))
                except Exception:
                    # Skip records that can't be processed
                    continue
                
            return upselling_data
        except Exception:
            # Return empty list if query fails
            return []

    @staticmethod
    def get_employee_performance_summary(db: Session, employee_id: int, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> Optional[EmployeePerformanceResponse]:
        """
        Get comprehensive performance summary for a specific employee
        """
        try:
            employee = db.query(User).filter(User.id == employee_id).first()
            if not employee:
                return None
                
            # Get basic sales data
            query = db.query(
                func.count(Order.id).label('order_count'),
                func.sum(Order.total).label('total_sales'),
                func.avg(Order.total).label('average_order_value')
            ).filter(Order.created_by == employee_id)
            
            if start_date:
                query = query.filter(Order.created_at >= start_date)
            if end_date:
                query = query.filter(Order.created_at <= end_date)
                
            result = query.first()
            
            # Handle case where result might be None
            order_count = 0
            total_sales = 0.0
            average_order_value = 0.0
            
            if result:
                try:
                    order_count = int(result.order_count) if result.order_count is not None else 0
                    total_sales = float(result.total_sales) if result.total_sales is not None else 0.0
                    average_order_value = float(result.average_order_value) if result.average_order_value is not None else 0.0
                except (ValueError, TypeError):
                    # Use default values if conversion fails
                    pass
            
            try:
                data_dict = {
                    'employee_id': int(employee.id) if employee.id is not None else 0,
                    'username': str(employee.username) if employee.username is not None else "",
                    'full_name': str(employee.full_name) if employee.full_name is not None else None,
                    'role': str(employee.role.value) if employee.role is not None and hasattr(employee.role, 'value') else "",
                    'order_count': order_count,
                    'total_sales': total_sales,
                    'average_order_value': average_order_value,
                    'total_tips': 0,  # Placeholder
                    'upsell_count': 0  # Placeholder
                }
                
                return EmployeePerformanceResponse(**data_dict)
            except Exception:
                # Return None if we can't create the response
                return None
        except Exception:
            # Return None if query fails
            return None