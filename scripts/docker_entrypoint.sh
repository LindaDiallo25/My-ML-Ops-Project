#!/bin/bash
# Docker entrypoint script for API container
# This script runs when the container starts

echo "=========================================="
echo "Starting ML-Ops API Container"
echo "=========================================="

# Wait a bit for services to be ready
echo "Waiting for services to be ready..."
sleep 5

# Initialize MinIO bucket
echo ""
echo "Initializing MinIO..."
python3 /app/scripts/init_minio.py

# Auto-register model in MLflow
echo ""
echo "Checking MLflow Model Registry..."
python3 /app/scripts/auto_register_model.py

# Check if registration was successful (ignore errors, API should start anyway)
if [ $? -eq 0 ]; then
    echo "✓ Model registration check completed"
else
    echo "⚠ Model registration had issues, but continuing to start API..."
fi

echo ""
echo "=========================================="
echo "Starting FastAPI Application"
echo "=========================================="

# Start the FastAPI application
cd /app/api
exec uvicorn main:app --host 0.0.0.0 --port 8000

