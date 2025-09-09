# Use slim Python image for smaller footprint
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY ./app .

# Copy entrypoint script and make it executable
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Expose port
EXPOSE 8088

# Set entrypoint
ENTRYPOINT ["/start.sh"]

# Command for Gunicorn + Uvicorn workers
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8088"]