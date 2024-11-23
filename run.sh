#!/bin/bash

# Add src directory to PYTHONPATH
export PYTHONPATH=/home/vinu/Desktop/PERSONAL/INTERVIEWS/IgniteSolutions/BookSearch/src:$PYTHONPATH

echo "🚀 Starting Book Search Application..."

# Stop any existing containers
echo "Stopping any existing containers..."
docker-compose down

# Build and start the database service first
echo "Starting PostgreSQL database..."
docker-compose up -d db

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until docker-compose exec db pg_isready -h db -p 5432; do
  echo "Database is not ready... waiting"
  sleep 2
done

echo "Database is ready!"

# Initialize database
echo "Initializing database..."
if docker-compose exec -T db psql -h db -U user -d gutenberg -c '\dt' 2>/dev/null | grep -q 'public'; then
    echo "Database already contains tables, skipping initialization."
else
    echo "Loading database dump..."
    docker-compose exec -T db psql -h db -U user -d gutenberg < gutendex.dump
    if [ $? -eq 0 ]; then
        echo "Database initialized successfully!"
    else
        echo "Failed to initialize database. Check if gutendex.dump exists and is readable."
        exit 1
    fi
fi

# Start the API service
echo "Starting API service..."
docker-compose up --build api

echo "🎉 Book Search Application is now running!"
echo "API is available at: http://localhost:5000"
echo ""
