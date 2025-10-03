#!/usr/bin/env python3
"""
Script to check Docker container status for the FastAPI backend
"""

import subprocess
import sys
import time

def check_docker_installed():
    """Check if Docker is installed"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Docker is installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Docker is not installed or not in PATH")
            return False
    except FileNotFoundError:
        print("❌ Docker is not installed or not in PATH")
        return False
    except Exception as e:
        print(f"❌ Error checking Docker installation: {e}")
        return False

def check_docker_running():
    """Check if Docker daemon is running"""
    try:
        result = subprocess.run(['docker', 'info'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Docker daemon is running")
            return True
        else:
            print("❌ Docker daemon is not running")
            return False
    except Exception as e:
        print(f"❌ Error checking Docker daemon: {e}")
        return False

def check_compose_containers():
    """Check if docker-compose containers are running"""
    try:
        # Check if docker-compose is available
        result = subprocess.run(['docker-compose', 'version'], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print("❌ docker-compose is not installed or not in PATH")
            return False
        
        print("✅ docker-compose is available")
        
        # Check running containers
        result = subprocess.run(['docker-compose', 'ps'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("\nDocker Compose Containers Status:")
            print("=" * 40)
            print(result.stdout)
            
            if "db" in result.stdout and "Up" in result.stdout:
                print("✅ PostgreSQL database container is running")
                return True
            else:
                print("⚠️  PostgreSQL database container is not running")
                return False
        else:
            print("❌ Error checking docker-compose containers")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error checking docker-compose containers: {e}")
        return False

def start_database_container():
    """Start the database container"""
    try:
        print("Starting PostgreSQL database container...")
        result = subprocess.run(['docker-compose', 'up', '-d', 'db'], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Database container started successfully")
            print("Waiting for database to be ready...")
            time.sleep(10)  # Wait for database to initialize
            return True
        else:
            print("❌ Failed to start database container")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error starting database container: {e}")
        return False

def main():
    """Main function to check Docker status"""
    print("Checking Docker Environment for FastAPI Backend")
    print("=" * 50)
    
    # Check Docker installation
    if not check_docker_installed():
        print("\n❌ Docker is required but not found. Please install Docker first.")
        return
    
    # Check Docker daemon
    if not check_docker_running():
        print("\n❌ Docker daemon is not running. Please start Docker.")
        return
    
    # Check compose containers
    containers_running = check_compose_containers()
    
    if not containers_running:
        print("\nAttempting to start database container...")
        if start_database_container():
            print("\nChecking container status again...")
            check_compose_containers()
        else:
            print("\n❌ Failed to start database container. Please check the configuration.")
    else:
        print("\n✅ Docker environment is ready for the FastAPI backend!")

if __name__ == "__main__":
    main()