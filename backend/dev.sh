#!/bin/bash
# Local development script

set -e  # Exit on error

echo "💻 Starting local development server..."

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: Must run from backend directory"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Copying from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env from .env.example"
        echo "⚠️  Please edit .env with your credentials before continuing"
        exit 1
    else
        echo "❌ Error: No .env or .env.example found"
        exit 1
    fi
fi

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3.12 -m venv venv
fi

source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/bin/uvicorn" ]; then
    echo "📦 Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Initialize database if needed
if [ ! -f "taskmanager.db" ]; then
    echo "🗄️  Initializing database..."
    alembic upgrade head
fi

# Start development server
echo "🚀 Starting FastAPI development server..."
echo "📍 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

uvicorn app.main:app --reload
