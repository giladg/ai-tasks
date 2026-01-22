#!/bin/bash
# VM Preparation Script for AI Tasks Deployment
# Run this on a fresh Debian 12 (Bookworm) VM

set -e  # Exit on error

echo "🚀 Preparing VM for AI Tasks deployment..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}❌ Please don't run as root. Run as normal user with sudo privileges.${NC}"
    exit 1
fi

# Check Debian version
echo "📋 Checking system requirements..."
if ! grep -q "Debian" /etc/os-release; then
    echo -e "${YELLOW}⚠️  Warning: This script is designed for Debian 12. Proceed with caution.${NC}"
else
    echo "✓ Detected Debian Linux"
fi

# Update system
echo ""
echo "🔄 Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install Python 3.11 (included in Debian 12)
echo ""
echo "🐍 Installing Python 3.11..."
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    build-essential \
    curl \
    wget \
    git

echo "✓ Python installed: $(python3.11 --version)"

# Install Node.js 18+
echo ""
echo "📦 Installing Node.js 18..."
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt install -y nodejs
else
    echo "Node.js already installed: $(node --version)"
fi

# Install system dependencies
echo ""
echo "🔧 Installing additional system dependencies..."
sudo apt install -y \
    nginx \
    default-mysql-server \
    certbot \
    python3-certbot-nginx \
    ufw

# Secure MySQL/MariaDB installation
echo ""
echo "🔐 Configuring MySQL/MariaDB..."
echo -e "${YELLOW}Note: Debian 12 uses MariaDB (MySQL-compatible fork)${NC}"
echo -e "${YELLOW}You'll be prompted to set the root password in the next step.${NC}"
echo -e "${YELLOW}Please remember the password you set!${NC}"
sleep 3
sudo mysql_secure_installation

# Create application directory
echo ""
echo "📁 Creating application directory..."
sudo mkdir -p /opt/ai-tasks
sudo chown $USER:$USER /opt/ai-tasks

# Create log directory
echo ""
echo "📝 Creating log directory..."
sudo mkdir -p /var/log/ai-tasks
sudo chown www-data:www-data /var/log/ai-tasks

# Create web directory
echo ""
echo "🌐 Creating web directory..."
sudo mkdir -p /var/www/ai-tasks
sudo chown www-data:www-data /var/www/ai-tasks

# Configure firewall
echo ""
echo "🔥 Configuring firewall..."
sudo ufw --force enable
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw status

echo ""
echo -e "${GREEN}✅ VM preparation complete!${NC}"
echo ""
echo "================================================"
echo "📋 NEXT STEPS - Run these commands manually:"
echo "================================================"
echo ""
echo "1️⃣  Setup MySQL/MariaDB Database:"
echo "   sudo mysql"
echo "   Then run these SQL commands:"
echo "   "
echo "   CREATE DATABASE taskmanager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
echo "   CREATE USER 'taskmanager_user'@'localhost' IDENTIFIED BY 'YOUR_STRONG_PASSWORD';"
echo "   GRANT ALL PRIVILEGES ON taskmanager.* TO 'taskmanager_user'@'localhost';"
echo "   FLUSH PRIVILEGES;"
echo "   EXIT;"
echo ""
echo "   Note: MariaDB is fully MySQL-compatible, so your app will work without changes."
echo ""
echo "2️⃣  Clone your repository:"
echo "   cd /opt/ai-tasks"
echo "   git clone YOUR_REPO_URL ."
echo "   (or use: git clone git@github.com:username/ai-tasks.git .)"
echo ""
echo "3️⃣  Configure Backend Environment:"
echo "   cd /opt/ai-tasks/backend"
echo "   cp .env.production .env"
echo "   nano .env"
echo ""
echo "   Generate new keys with:"
echo "   python3 -c \"import secrets; print(secrets.token_urlsafe(32))\""
echo "   python3 -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
echo ""
echo "   Update .env with:"
echo "   - SECRET_KEY (generated above)"
echo "   - ENCRYPTION_KEY (generated above)"
echo "   - DATABASE_URL=mysql+pymysql://taskmanager_user:YOUR_PASSWORD@localhost:3306/taskmanager"
echo "   - GOOGLE_CLIENT_ID (from Google Cloud Console)"
echo "   - GOOGLE_CLIENT_SECRET (from Google Cloud Console)"
echo "   - GEMINI_API_KEY (from Google AI Studio)"
echo ""
echo "4️⃣  Setup Backend:"
echo "   cd /opt/ai-tasks/backend"
echo "   python3.11 -m venv venv"
echo "   source venv/bin/activate"
echo "   pip install --upgrade pip"
echo "   pip install -r requirements.txt"
echo "   pip install gunicorn pymysql"
echo "   alembic upgrade head"
echo ""
echo "5️⃣  Create Systemd Services:"
echo "   Run: sudo nano /etc/systemd/system/ai-tasks-backend.service"
echo "   (See DEPLOYMENT.md for full service configuration)"
echo ""
echo "6️⃣  Setup Frontend:"
echo "   cd /opt/ai-tasks/frontend"
echo "   npm install"
echo "   npm run build"
echo "   sudo cp -r dist/* /var/www/ai-tasks/"
echo ""
echo "7️⃣  Configure Nginx:"
echo "   sudo nano /etc/nginx/sites-available/ai-tasks"
echo "   (See DEPLOYMENT.md for full nginx configuration)"
echo "   sudo ln -s /etc/nginx/sites-available/ai-tasks /etc/nginx/sites-enabled/"
echo "   sudo nginx -t"
echo "   sudo systemctl reload nginx"
echo ""
echo "8️⃣  Setup SSL Certificate:"
echo "   sudo certbot --nginx -d YOUR_DOMAIN -d www.YOUR_DOMAIN"
echo ""
echo "9️⃣  Update Google Cloud Console:"
echo "   Add authorized redirect URI: https://YOUR_DOMAIN/api/v1/auth/google/callback"
echo ""
echo "🔟  Start Services:"
echo "   sudo chown -R www-data:www-data /opt/ai-tasks"
echo "   sudo systemctl daemon-reload"
echo "   sudo systemctl enable ai-tasks-backend ai-tasks-scheduler"
echo "   sudo systemctl start ai-tasks-backend ai-tasks-scheduler"
echo ""
echo "================================================"
echo "📚 For detailed instructions, see: /opt/ai-tasks/DEPLOYMENT.md"
echo "================================================"
