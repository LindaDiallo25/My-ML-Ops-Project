#!/bin/bash

# MLOps Project Startup Script
# This script helps you start the API server locally

echo "🚀 Starting MLOps API Server..."
echo "================================"

# Get the project directory (where this script is located)
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "📁 Project directory: $PROJECT_DIR"
echo ""

# Check if model file exists
if [ ! -f "$PROJECT_DIR/dandelion_grass_cnn.keras" ]; then
    echo "❌ Model file not found: dandelion_grass_cnn.keras"
    echo "Please run the training script first:"
    echo "  python train_with_mlflow.py"
    exit 1
fi

echo "✅ Model file found"
echo ""

# Check if dependencies are installed
echo "📦 Checking Python dependencies..."
python3 -c "import fastapi, uvicorn, tensorflow" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies. Installing..."
    pip install fastapi uvicorn python-multipart tensorflow pillow numpy
fi

echo "✅ Dependencies ready"
echo ""

# Start the API server
echo "🌐 Starting FastAPI server on http://localhost:8000"
echo "📚 API docs will be available at http://localhost:8000/docs"
echo ""
echo "Press CTRL+C to stop the server"
echo "================================"
echo ""

cd "$PROJECT_DIR/api"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
