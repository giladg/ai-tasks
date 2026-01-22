# Deployment Guide

This guide covers deploying to production at `ai-tasks.app` while maintaining local development.

## Prerequisites

- Server with Ubuntu 22.04 or similar
- Domain name: `ai-tasks.app` pointing to your server
- Python 3.12 installed on server
- Node.js 18+ installed on server
- MySQL or PostgreSQL database

## Quick Start

### Local Development (Your Laptop)

```bash
# Backend
cd backend
./dev.sh

# Frontend (new terminal)
cd frontend
npm run dev
```

Visit: http://localhost:5173

### Production Deployment

```bash
# On production server
cd backend
./deploy.sh

# Build frontend (on your laptop or CI/CD)
cd frontend
npm run build

# Copy dist/ to server
scp -r dist/* server:/var/www/ai-tasks/
```

## Initial Production Setup

### 1. Server Setup

```bash
# SSH into your server
ssh user@ai-tasks.app

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.12 python3.12-venv python3-pip nginx mysql-server certbot python3-certbot-nginx git

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### 2. Clone Repository

```bash
# Create app directory
sudo mkdir -p /opt/ai-tasks
sudo chown $USER:$USER /opt/ai-tasks

# Clone repo
cd /opt/ai-tasks
git clone git@github.com:YOUR_USERNAME/ai-tasks.git .
```

### 3. Configure Production Environment

```bash
# Backend - Edit production config
cd /opt/ai-tasks/backend
cp .env.production .env
nano .env
```

**Generate new production keys:**
```bash
# Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate ENCRYPTION_KEY
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Update `.env` with:
- New SECRET_KEY and ENCRYPTION_KEY
- Production database credentials
- Google OAuth credentials
- Gemini API key

**Frontend:**
```bash
cd /opt/ai-tasks/frontend
# .env.production is already correct (https://ai-tasks.app)
```

### 4. Setup Database

```bash
# Create MySQL database
sudo mysql

CREATE DATABASE taskmanager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'taskmanager_user'@'localhost' IDENTIFIED BY 'strong_password_here';
GRANT ALL PRIVILEGES ON taskmanager.* TO 'taskmanager_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Update `DATABASE_URL` in `backend/.env`:
```bash
DATABASE_URL=mysql+pymysql://taskmanager_user:strong_password_here@localhost:3306/taskmanager
```

### 5. Setup Backend

```bash
cd /opt/ai-tasks/backend

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn pymysql

# Run migrations
alembic upgrade head
```

### 6. Create Gunicorn Config

```bash
nano /opt/ai-tasks/backend/gunicorn.conf.py
```

```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
accesslog = "/var/log/ai-tasks/gunicorn-access.log"
errorlog = "/var/log/ai-tasks/gunicorn-error.log"
loglevel = "info"
```

### 7. Create Systemd Services

**Backend API Service:**
```bash
sudo nano /etc/systemd/system/ai-tasks-backend.service
```

```ini
[Unit]
Description=AI Tasks Backend API
After=network.target mysql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/ai-tasks/backend
Environment="PATH=/opt/ai-tasks/backend/venv/bin"
ExecStart=/opt/ai-tasks/backend/venv/bin/gunicorn app.main:app -c gunicorn.conf.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Background Scheduler Service:**
```bash
sudo nano /etc/systemd/system/ai-tasks-scheduler.service
```

```ini
[Unit]
Description=AI Tasks Background Scheduler
After=network.target mysql.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/ai-tasks/backend
Environment="PATH=/opt/ai-tasks/backend/venv/bin"
ExecStart=/opt/ai-tasks/backend/venv/bin/python -m app.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start services:**
```bash
# Create log directory
sudo mkdir -p /var/log/ai-tasks
sudo chown www-data:www-data /var/log/ai-tasks

# Give www-data ownership
sudo chown -R www-data:www-data /opt/ai-tasks

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable ai-tasks-backend
sudo systemctl enable ai-tasks-scheduler
sudo systemctl start ai-tasks-backend
sudo systemctl start ai-tasks-scheduler

# Check status
sudo systemctl status ai-tasks-backend
sudo systemctl status ai-tasks-scheduler
```

### 8. Build Frontend

```bash
cd /opt/ai-tasks/frontend
npm install
npm run build

# Create web directory
sudo mkdir -p /var/www/ai-tasks
sudo cp -r dist/* /var/www/ai-tasks/
sudo chown -R www-data:www-data /var/www/ai-tasks
```

### 9. Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/ai-tasks
```

```nginx
server {
    listen 80;
    server_name ai-tasks.app www.ai-tasks.app;

    # Redirect HTTP to HTTPS (will be added after SSL setup)
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name ai-tasks.app www.ai-tasks.app;

    # SSL certificates (will be added by certbot)
    # ssl_certificate /etc/letsencrypt/live/ai-tasks.app/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/ai-tasks.app/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Frontend (React app)
    root /var/www/ai-tasks;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    # Health check
    location /health {
        proxy_pass http://127.0.0.1:8000;
    }

    # API docs (optional - remove in production for security)
    location /docs {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/ai-tasks /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 10. Setup SSL with Let's Encrypt

```bash
# Get SSL certificate
sudo certbot --nginx -d ai-tasks.app -d www.ai-tasks.app

# Test auto-renewal
sudo certbot renew --dry-run
```

Certbot will automatically update your nginx config with SSL settings!

### 11. Update Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Click your OAuth 2.0 Client ID
3. Under "Authorized redirect URIs", add:
   - `https://ai-tasks.app/api/v1/auth/google/callback`
4. Under "Authorized JavaScript origins", add:
   - `https://ai-tasks.app`
5. Click Save

### 12. Configure Firewall

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 13. Test Deployment

```bash
# Test backend health
curl https://ai-tasks.app/health

# View logs
sudo journalctl -u ai-tasks-backend -f
sudo journalctl -u ai-tasks-scheduler -f

# Check nginx logs
sudo tail -f /var/log/nginx/error.log
```

Visit: https://ai-tasks.app

## Updating Production

### Quick Update

```bash
# On server
cd /opt/ai-tasks
git pull
cd backend
./deploy.sh

# Rebuild frontend
cd /opt/ai-tasks/frontend
npm run build
sudo cp -r dist/* /var/www/ai-tasks/
```

### Manual Update

```bash
# Backend
cd /opt/ai-tasks
git pull
cd backend
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart ai-tasks-backend
sudo systemctl restart ai-tasks-scheduler

# Frontend
cd /opt/ai-tasks/frontend
npm install
npm run build
sudo cp -r dist/* /var/www/ai-tasks/
```

## Monitoring

### Check Service Status

```bash
sudo systemctl status ai-tasks-backend
sudo systemctl status ai-tasks-scheduler
```

### View Logs

```bash
# Backend API logs
sudo journalctl -u ai-tasks-backend -f

# Scheduler logs
sudo journalctl -u ai-tasks-scheduler -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Gunicorn logs
sudo tail -f /var/log/ai-tasks/gunicorn-access.log
sudo tail -f /var/log/ai-tasks/gunicorn-error.log
```

### Database Backup

```bash
# Backup database
mysqldump -u taskmanager_user -p taskmanager > backup_$(date +%Y%m%d).sql

# Restore database
mysql -u taskmanager_user -p taskmanager < backup_20260108.sql
```

## Troubleshooting

### Backend not starting

```bash
# Check logs
sudo journalctl -u ai-tasks-backend -n 50

# Test manually
cd /opt/ai-tasks/backend
source venv/bin/activate
python -c "from app.config import get_settings; print(get_settings())"
```

### Database connection errors

```bash
# Test database connection
mysql -u taskmanager_user -p taskmanager

# Check DATABASE_URL in .env
cat /opt/ai-tasks/backend/.env | grep DATABASE_URL
```

### OAuth errors

1. Check redirect URI in Google Cloud Console matches exactly
2. Verify GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env
3. Check CORS_ORIGINS includes your domain

### Frontend not loading

```bash
# Check nginx config
sudo nginx -t

# Check file permissions
ls -la /var/www/ai-tasks/

# Rebuild frontend
cd /opt/ai-tasks/frontend
npm run build
sudo cp -r dist/* /var/www/ai-tasks/
```

## Security Checklist

- [ ] Changed SECRET_KEY and ENCRYPTION_KEY for production
- [ ] Using strong database password
- [ ] SSL/HTTPS enabled
- [ ] Firewall configured
- [ ] .env files not committed to git
- [ ] API rate limiting enabled (optional)
- [ ] Database backups configured
- [ ] Log rotation configured

## Performance Optimization

### Database Indexing

Already handled by migrations, but verify:
```sql
SHOW INDEX FROM tasks;
SHOW INDEX FROM users;
```

### Nginx Caching

Add to nginx config for static assets:
```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Gunicorn Workers

Adjust workers based on CPU cores:
```python
# gunicorn.conf.py
workers = (2 * cpu_cores) + 1
```

## Support

For issues:
1. Check logs (see Monitoring section)
2. Review error messages
3. Check configuration files
4. Test components individually

## Maintenance

### Update Dependencies

```bash
# Backend
cd /opt/ai-tasks/backend
source venv/bin/activate
pip list --outdated
pip install --upgrade <package>

# Frontend
cd /opt/ai-tasks/frontend
npm outdated
npm update
```

### Clean Up Logs

```bash
# Setup log rotation
sudo nano /etc/logrotate.d/ai-tasks
```

```
/var/log/ai-tasks/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload ai-tasks-backend > /dev/null
    endscript
}
```
