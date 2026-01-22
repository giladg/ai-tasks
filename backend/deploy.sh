#!/bin/bash
# Production deployment script

set -e  # Exit on error

echo "🚀 Deploying to production..."

# Check if we're in the right directory
if [ ! -f "app/main.py" ]; then
    echo "❌ Error: Must run from backend directory"
    exit 1
fi

# Backup current .env if it exists
if [ -f ".env" ]; then
    echo "📦 Backing up current .env..."
    cp .env .env.backup
fi

# Use production config
echo "🔧 Using production configuration..."
cp .env.production .env

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found. Run: python3.12 -m venv venv"
    exit 1
fi

source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Run database migrations
echo "🗄️  Running database migrations..."
alembic upgrade head

# Restart services (if using systemd)
if command -v systemctl &> /dev/null; then
    echo "🔄 Restarting services..."
    sudo systemctl restart ai-tasks-backend || echo "⚠️  Backend service not found"
    sudo systemctl restart ai-tasks-scheduler || echo "⚠️  Scheduler service not found"
else
    echo "⚠️  systemctl not found. Please restart services manually."
fi

echo "✅ Production deployment complete!"
echo ""
echo "Next steps:"
echo "  1. Check backend: curl https://ai-tasks.app/health"
echo "  2. Check logs: sudo journalctl -u ai-tasks-backend -f"
