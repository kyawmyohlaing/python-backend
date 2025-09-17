# Use slim Python image for smaller footprint
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code and other necessary files
COPY ./app ./app
COPY ./app/migrations ./app/migrations
COPY ./app/migrations/alembic.ini ./app/migrations/alembic.ini
COPY ./app/init_db.py ./app/init_db.py
COPY ./start.sh ./start.sh
RUN chmod +x ./start.sh

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8088

# Run the application directly
CMD ["python", "app/main.py"]