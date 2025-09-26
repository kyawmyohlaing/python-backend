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
        EmployeePerformanceResponse,
        DailySalesReportResponse,
        WeeklySalesReportResponse,
        MonthlySalesReportResponse,
        SalesReportItem
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
        EmployeePerformanceResponse,
        DailySalesReportResponse,
        WeeklySalesReportResponse,
        MonthlySalesReportResponse,
        SalesReportItem
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

    @staticmethod
    def get_daily_sales_report(db: Session, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> DailySalesReportResponse:
        """
        Get daily sales report with sales data grouped by day
        """
        try:
            # Set default date range to last 30 days if not provided
            if not start_date:
                start_date = datetime.now() - timedelta(days=30)
            if not end_date:
                end_date = datetime.now()
                
            # Query to get sales data grouped by day
            query = db.query(
                func.date(Order.created_at).label('date'),
                func.sum(Order.total).label('total_sales'),
                func.count(Order.id).label('order_count'),
                func.avg(Order.total).label('average_order_value')
            ).filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date
            ).group_by(func.date(Order.created_at))\
             .order_by(func.date(Order.created_at))
            
            results = query.all()
            
            # Format results
            sales_data = []
            total_sales = 0
            total_orders = 0
            
            for result in results:
                try:
                    # Create a dictionary with the values
                    data_dict = {
                        'date': result.date,
                        'total_sales': float(result.total_sales) if result.total_sales is not None else 0.0,
                        'order_count': int(result.order_count) if result.order_count is not None else 0,
                        'average_order_value': float(result.average_order_value) if result.average_order_value is not None else 0.0
                    }
                    
                    sales_item = SalesReportItem(**data_dict)
                    sales_data.append(sales_item)
                    
                    # Accumulate totals
                    total_sales += sales_item.total_sales
                    total_orders += sales_item.order_count
                except Exception:
                    # Skip records that can't be processed
                    continue
            
            # Calculate average daily sales
            average_daily_sales = total_sales / len(sales_data) if sales_data else 0.0
            
            # Create response
            response_dict = {
                'period': 'daily',
                'start_date': start_date,
                'end_date': end_date,
                'total_sales': total_sales,
                'total_orders': total_orders,
                'average_daily_sales': average_daily_sales,
                'sales_data': sales_data
            }
            
            return DailySalesReportResponse(**response_dict)
        except Exception as e:
            # Return empty response if query fails
            response_dict = {
                'period': 'daily',
                'start_date': start_date or datetime.now() - timedelta(days=30),
                'end_date': end_date or datetime.now(),
                'total_sales': 0,
                'total_orders': 0,
                'average_daily_sales': 0,
                'sales_data': []
            }
            return DailySalesReportResponse(**response_dict)

    @staticmethod
    def get_weekly_sales_report(db: Session, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> WeeklySalesReportResponse:
        """
        Get weekly sales report with sales data grouped by week
        """
        try:
            # Set default date range to last 12 weeks if not provided
            if not start_date:
                start_date = datetime.now() - timedelta(weeks=12)
            if not end_date:
                end_date = datetime.now()
                
            # Query to get sales data grouped by week
            # Using PostgreSQL-compatible date functions
            query = db.query(
                func.date_trunc('week', Order.created_at).label('week'),
                func.sum(Order.total).label('total_sales'),
                func.count(Order.id).label('order_count'),
                func.avg(Order.total).label('average_order_value')
            ).filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date
            ).group_by(func.date_trunc('week', Order.created_at))\
             .order_by(func.date_trunc('week', Order.created_at))
            
            results = query.all()
            
            # Format results
            sales_data = []
            total_sales = 0
            total_orders = 0
            
            for result in results:
                try:
                    # Use the actual week date from the query result
                    data_dict = {
                        'date': result.week,  # Use the actual week date from query
                        'total_sales': float(result.total_sales) if result.total_sales is not None else 0.0,
                        'order_count': int(result.order_count) if result.order_count is not None else 0,
                        'average_order_value': float(result.average_order_value) if result.average_order_value is not None else 0.0
                    }
                    
                    sales_item = SalesReportItem(**data_dict)
                    sales_data.append(sales_item)
                    
                    # Accumulate totals
                    total_sales += sales_item.total_sales
                    total_orders += sales_item.order_count
                except Exception:
                    # Skip records that can't be processed
                    continue
            
            # Calculate average weekly sales
            average_weekly_sales = total_sales / len(sales_data) if sales_data else 0.0
            
            # Create response
            response_dict = {
                'period': 'weekly',
                'start_date': start_date,
                'end_date': end_date,
                'total_sales': total_sales,
                'total_orders': total_orders,
                'average_weekly_sales': average_weekly_sales,
                'sales_data': sales_data
            }
            
            return WeeklySalesReportResponse(**response_dict)
        except Exception as e:
            # Return empty response if query fails
            response_dict = {
                'period': 'weekly',
                'start_date': start_date or datetime.now() - timedelta(weeks=12),
                'end_date': end_date or datetime.now(),
                'total_sales': 0,
                'total_orders': 0,
                'average_weekly_sales': 0,
                'sales_data': []
            }
            return WeeklySalesReportResponse(**response_dict)

    @staticmethod
    def get_monthly_sales_report(db: Session, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> MonthlySalesReportResponse:
        """
        Get monthly sales report with sales data grouped by month
        """
        try:
            # Set default date range to last 12 months if not provided
            if not start_date:
                start_date = datetime.now() - timedelta(days=365)
            if not end_date:
                end_date = datetime.now()
                
            # Query to get sales data grouped by month
            # Using PostgreSQL-compatible date functions
            query = db.query(
                func.date_trunc('month', Order.created_at).label('month'),
                func.sum(Order.total).label('total_sales'),
                func.count(Order.id).label('order_count'),
                func.avg(Order.total).label('average_order_value')
            ).filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date
            ).group_by(func.date_trunc('month', Order.created_at))\
             .order_by(func.date_trunc('month', Order.created_at))
            
            results = query.all()
            
            # Format results
            sales_data = []
            total_sales = 0
            total_orders = 0
            
            for result in results:
                try:
                    # Use the actual month date from the query result
                    data_dict = {
                        'date': result.month,  # Use the actual month date from query
                        'total_sales': float(result.total_sales) if result.total_sales is not None else 0.0,
                        'order_count': int(result.order_count) if result.order_count is not None else 0,
                        'average_order_value': float(result.average_order_value) if result.average_order_value is not None else 0.0
                    }
                    
                    sales_item = SalesReportItem(**data_dict)
                    sales_data.append(sales_item)
                    
                    # Accumulate totals
                    total_sales += sales_item.total_sales
                    total_orders += sales_item.order_count
                except Exception:
                    # Skip records that can't be processed
                    continue
            
            # Calculate average monthly sales
            average_monthly_sales = total_sales / len(sales_data) if sales_data else 0.0
            
            # Create response
            response_dict = {
                'period': 'monthly',
                'start_date': start_date,
                'end_date': end_date,
                'total_sales': total_sales,
                'total_orders': total_orders,
                'average_monthly_sales': average_monthly_sales,
                'sales_data': sales_data
            }
            
            return MonthlySalesReportResponse(**response_dict)
        except Exception as e:
            # Return empty response if query fails
            response_dict = {
                'period': 'monthly',
                'start_date': start_date or datetime.now() - timedelta(days=365),
                'end_date': end_date or datetime.now(),
                'total_sales': 0,
                'total_orders': 0,
                'average_monthly_sales': 0,
                'sales_data': []
            }
            return MonthlySalesReportResponse(**response_dict)