import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import sys
import os

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the modules
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics_schema import (
    DailySalesReportResponse,
    WeeklySalesReportResponse,
    MonthlySalesReportResponse
)


class TestSalesReports:
    """Test cases for sales reports functionality"""

    def test_get_daily_sales_report(self):
        """Test daily sales report generation"""
        # Create a mock database session
        mock_db = Mock()
        
        # Create mock query results
        mock_result = Mock()
        mock_result.date = datetime.now().date()
        mock_result.total_sales = 1000.0
        mock_result.order_count = 10
        mock_result.average_order_value = 100.0
        
        # Configure the mock to return our test data
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.group_by.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = [mock_result]
        
        mock_db.query.return_value = mock_query
        
        # Call the method under test
        result = AnalyticsService.get_daily_sales_report(mock_db)
        
        # Assertions
        assert isinstance(result, DailySalesReportResponse)
        assert result.period == "daily"
        assert len(result.sales_data) == 1
        assert result.sales_data[0].total_sales == 1000.0
        assert result.sales_data[0].order_count == 10

    def test_get_weekly_sales_report(self):
        """Test weekly sales report generation"""
        # Create a mock database session
        mock_db = Mock()
        
        # Create mock query results with proper datetime object
        mock_result = Mock()
        mock_result.week = datetime.now()  # This should be a datetime object, not a string
        mock_result.total_sales = 7000.0
        mock_result.order_count = 70
        mock_result.average_order_value = 100.0
        
        # Configure the mock to return our test data
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.group_by.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = [mock_result]
        
        mock_db.query.return_value = mock_query
        
        # Call the method under test
        result = AnalyticsService.get_weekly_sales_report(mock_db)
        
        # Assertions
        assert isinstance(result, WeeklySalesReportResponse)
        assert result.period == "weekly"
        assert len(result.sales_data) == 1
        assert result.sales_data[0].total_sales == 7000.0
        assert result.sales_data[0].order_count == 70

    def test_get_monthly_sales_report(self):
        """Test monthly sales report generation"""
        # Create a mock database session
        mock_db = Mock()
        
        # Create mock query results with proper datetime object
        mock_result = Mock()
        mock_result.month = datetime.now()  # This should be a datetime object, not a string
        mock_result.total_sales = 30000.0
        mock_result.order_count = 300
        mock_result.average_order_value = 100.0
        
        # Configure the mock to return our test data
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.group_by.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = [mock_result]
        
        mock_db.query.return_value = mock_query
        
        # Call the method under test
        result = AnalyticsService.get_monthly_sales_report(mock_db)
        
        # Assertions
        assert isinstance(result, MonthlySalesReportResponse)
        assert result.period == "monthly"
        assert len(result.sales_data) == 1
        assert result.sales_data[0].total_sales == 30000.0
        assert result.sales_data[0].order_count == 300

    def test_get_daily_sales_report_with_date_range(self):
        """Test daily sales report generation with custom date range"""
        # Create a mock database session
        mock_db = Mock()
        
        # Create mock query results
        mock_result = Mock()
        mock_result.date = datetime.now().date()
        mock_result.total_sales = 1000.0
        mock_result.order_count = 10
        mock_result.average_order_value = 100.0
        
        # Configure the mock to return our test data
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.group_by.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = [mock_result]
        
        mock_db.query.return_value = mock_query
        
        # Define date range
        start_date = datetime.now() - timedelta(days=7)
        end_date = datetime.now()
        
        # Call the method under test
        result = AnalyticsService.get_daily_sales_report(mock_db, start_date, end_date)
        
        # Assertions
        assert isinstance(result, DailySalesReportResponse)
        assert result.period == "daily"
        assert result.start_date == start_date
        assert result.end_date == end_date

if __name__ == "__main__":
    pytest.main([__file__])