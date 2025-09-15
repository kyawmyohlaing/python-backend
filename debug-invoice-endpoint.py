#!/usr/bin/env python3
"""
Script to debug the invoice endpoint by directly calling the FastAPI route.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

# Set the environment to development
os.environ["ENVIRONMENT"] = "development"

from app.main import app
from fastapi.testclient import TestClient
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_invoice_endpoint():
    """Debug the invoice endpoint by making a direct call."""
    try:
        # Create a test client
        client = TestClient(app)
        
        # Try to get all invoices
        logger.info("🔍 Testing invoices endpoint...")
        response = client.get("/api/invoices/")
        
        logger.info(f"Status Code: {response.status_code}")
        logger.info(f"Response: {response.text}")
        
        if response.status_code == 200:
            logger.info("✅ Invoices endpoint working!")
            invoices = response.json()
            logger.info(f"Invoices count: {len(invoices) if isinstance(invoices, list) else 'N/A'}")
        else:
            logger.error("❌ Invoices endpoint failed!")
            
        return response.status_code == 200
            
    except Exception as e:
        logger.error(f"Failed to test invoices endpoint: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Debugging invoice endpoint directly...")
    print()
    
    success = debug_invoice_endpoint()
    
    print()
    if success:
        print("✅ Invoice endpoint test completed successfully!")
    else:
        print("❌ Invoice endpoint test failed!")