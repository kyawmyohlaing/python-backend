#!/usr/bin/env python3
"""
Check if all required packages are installed
"""

def check_requirements():
    """Check if all required packages are installed"""
    required_packages = [
        'fastapi',
        'sqlalchemy',
        'psycopg2',
        'python-jose',
        'passlib',
        'python-dotenv',
        'pydantic'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please install them with: pip install " + " ".join(missing_packages))
        return False
    else:
        print("\nAll required packages are installed!")
        return True

if __name__ == "__main__":
    check_requirements()