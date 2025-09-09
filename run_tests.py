#!/usr/bin/env python3
"""
Test runner script for the FastAPI backend.
This script demonstrates how to run tests with both SQLite and PostgreSQL.
"""

import os
import sys
import subprocess

def run_sqlite_tests():
    """Run tests with SQLite in-memory database"""
    print("Running tests with SQLite...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", "tests/", "-v"
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0

def run_postgres_tests():
    """Run tests with PostgreSQL database"""
    postgres_url = os.getenv("TEST_POSTGRES_URL")
    if not postgres_url:
        print("Skipping PostgreSQL tests - TEST_POSTGRES_URL not set")
        return True
    
    print(f"Running tests with PostgreSQL ({postgres_url})...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", "tests/", "-v", "-k", "postgres"
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0

def main():
    """Run all tests"""
    print("FastAPI Backend Test Runner")
    print("=" * 30)
    
    # Run SQLite tests
    sqlite_success = run_sqlite_tests()
    
    # Run PostgreSQL tests
    postgres_success = run_postgres_tests()
    
    # Summary
    print("\n" + "=" * 30)
    print("Test Summary:")
    print(f"SQLite tests: {'PASSED' if sqlite_success else 'FAILED'}")
    print(f"PostgreSQL tests: {'PASSED' if postgres_success else 'SKIPPED/FAILED'}")
    
    if sqlite_success and postgres_success:
        print("All tests passed!")
        return 0
    else:
        print("Some tests failed or were skipped.")
        return 1

if __name__ == "__main__":
    sys.exit(main())