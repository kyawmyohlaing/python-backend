# Kitchen and Bar Page Fix

This directory contains scripts to fix the issues with the kitchen and bar pages.

## Problem
The kitchen and bar pages were not working correctly because the `kitchen_orders` table was missing from the database.

## Solution
The fix involves:
1. Deleting the existing database
2. Reinitializing the database with all necessary tables
3. Creating sample orders for testing
4. Verifying that the APIs work correctly

## How to Use

### Option 1: Automated Fix (Recommended)
Run the automated fix script:
```bash
python fix_kitchen_bar_issues.py
```

This script will:
1. Ask for confirmation before proceeding
2. Delete the existing database
3. Reinitialize the database with all tables
4. Create sample orders
5. Test the APIs
6. Provide a summary of the results

### Option 2: Manual Fix
If you prefer to do it manually:

1. Delete the existing database:
   ```bash
   del dev.db
   ```

2. Initialize the database:
   ```bash
   python init_local_db.py
   ```

3. Create sample orders:
   ```bash
   python create_sample_orders.py
   ```

4. Test the APIs:
   ```bash
   python test_kitchen_bar_apis.py
   ```

## Files
- `fix_kitchen_bar_issues.py` - Automated fix script
- `init_local_db.py` - Database initialization script
- `create_sample_orders.py` - Sample orders creation script
- `test_kitchen_bar_apis.py` - API testing script
- `test_kitchen_orders.py` - Kitchen orders testing script

## Verification
After running the fix, you should be able to:
- Access the kitchen page and see orders
- Access the bar page and see orders
- Use the menu order tracking page
- Use the billing page
- The sales report page should continue to work as before

## Support
If you continue to experience issues:
1. Make sure the backend server is running
2. Check that all scripts executed without errors
3. Verify the database was created correctly
4. Check the browser console for frontend errors