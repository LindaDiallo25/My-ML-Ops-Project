#!/bin/bash

# MLOps Frontend Startup Script
# This script helps you start the React frontend locally

echo "🎨 Starting MLOps Frontend..."
echo "=============================="

# Get the project directory (where this script is located)
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "📁 Project directory: $PROJECT_DIR"
echo ""

# Navigate to Frontend directory
cd "$PROJECT_DIR/Front"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing npm dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ npm install failed"
        exit 1
    fi
fi

echo "✅ Dependencies ready"
echo ""

# Start the dev server
echo "🌐 Starting Vite dev server..."
echo "Frontend will be available at http://localhost:5173"
echo ""
echo "⚠️  Make sure the API is running on http://localhost:8000"
echo "   (Run ./utils/start_api.sh in another terminal)"
echo ""
echo "Press CTRL+C to stop the server"
echo "=============================="
echo ""

npm run dev
