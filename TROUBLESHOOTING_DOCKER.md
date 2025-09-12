# Docker Troubleshooting Guide

This document provides solutions for common issues encountered when working with the Docker setup for the FastAPI backend template.

## Table of Contents
1. [Container Restarting Issues](#container-restarting-issues)
2. [Database Connection Problems](#database-connection-problems)
3. [Port Conflicts](#port-conflicts)
4. [Volume Issues](#volume-issues)
5. [Build Failures](#build-failures)
6. [Network Problems](#network-problems)
7. [Performance Issues](#performance-issues)
8. [Additional Resources](#additional-resources)

## Container Restarting Issues

### Problem
Containers keep restarting or fail to start properly.

### Solutions
1. **Check logs for specific errors**:
   ```bash
   docker-compose logs <service_name>
   ```

2. **Ensure dependencies are ready**:
   The `start.sh` script includes a wait mechanism for PostgreSQL. If this is failing, check that the database service is properly configured.

3. **Verify environment variables**:
   Make sure all required environment variables are set in the `.env` file.

4. **Check file permissions**:
   Ensure the `start.sh` script has execute permissions:
   ```bash
   chmod +x start.sh
   ```

## Database Connection Problems

### Problem
Application cannot connect to the PostgreSQL database.

### Solutions
1. **Verify service names**:
   When running in Docker, the application should connect to the `db` service, not `localhost`:
   ```env
   # Correct for Docker
   DATABASE_URL=postgresql://postgres:password@db:5432/mydb
   ```

2. **Check database credentials**:
   Ensure the PostgreSQL username, password, and database name match between the application configuration and the `docker-compose.yml` file.

3. **Verify database service status**:
   ```bash
   docker-compose ps
   ```

4. **Check database logs**:
   ```bash
   docker-compose logs db
   ```

For more detailed database troubleshooting, see [DATABASE_TROUBLESHOOTING.md](DATABASE_TROUBLESHOOTING.md).

## Port Conflicts

### Problem
Error messages like "port is already allocated" when starting services.

### Solutions
1. **Change the port mapping in `docker-compose.yml`**:
   ```yaml
   ports:
     - "8089:8088"  # Change host port to 8089
   ```

2. **Stop conflicting services**:
   ```bash
   # Find processes using the port
   lsof -i :8088
   
   # Kill the process
   kill -9 <PID>
   ```

3. **Use different ports for different environments**:
   Set the port through environment variables:
   ```bash
   PORT=8089 docker-compose up
   ```

## Volume Issues

### Problem
Database data is lost when containers are removed or data is not persisting.

### Solutions
1. **Use named volumes for data persistence**:
   ```yaml
   volumes:
     postgres_data:
   ```

2. **Verify volume mounting**:
   ```bash
   docker volume ls
   docker volume inspect postgres_data
   ```

3. **Backup data before making changes**:
   ```bash
   docker-compose exec db pg_dump -U postgres mydb > backup.sql
   ```

## Build Failures

### Problem
Docker build process fails with package installation errors.

### Solutions
1. **Clear Docker build cache**:
   ```bash
   docker builder prune
   ```

2. **Update dependencies in `requirements.txt`**:
   Check for version conflicts or outdated packages.

3. **Use specific package versions**:
   Pin package versions to avoid compatibility issues:
   ```txt
   fastapi==0.68.0
   uvicorn==0.15.0
   ```

4. **Check network connectivity**:
   If building behind a corporate firewall, configure proxy settings:
   ```dockerfile
   ENV HTTP_PROXY=http://proxy.company.com:8080
   ENV HTTPS_PROXY=http://proxy.company.com:8080
   ```

## Network Problems

### Problem
Services cannot communicate with each other or external services.

### Solutions
1. **Verify services are on the same network**:
   ```bash
   docker network ls
   docker network inspect <network_name>
   ```

2. **Use service names for inter-container communication**:
   ```python
   # Correct for Docker
   DATABASE_URL = "postgresql://postgres:password@db:5432/mydb"
   
   # Incorrect for Docker
   DATABASE_URL = "postgresql://postgres:password@localhost:5432/mydb"
   ```

3. **Check custom network configurations**:
   Ensure custom networks in `docker-compose.yml` are properly defined.

## Performance Issues

### Problem
Application is slow or unresponsive when running in Docker.

### Solutions
1. **Allocate more resources**:
   Adjust Docker resource limits in Docker Desktop settings.

2. **Optimize database queries**:
   Add database indexes and optimize slow queries.

3. **Use appropriate Gunicorn workers**:
   Adjust the number of workers based on available CPU cores:
   ```bash
   # In Dockerfile
   CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8088"]
   ```

4. **Monitor resource usage**:
   ```bash
   docker stats
   ```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Database Troubleshooting Guide](DATABASE_TROUBLESHOOTING.md)
- [Database Issues Resolved](DATABASE_ISSUES_RESOLVED.md)

For general troubleshooting of the FastAPI backend template, see the main [README.md](README.md) file.