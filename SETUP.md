# Setup Guide - AI Task Manager

This guide will walk you through setting up the complete application from scratch.

## Prerequisites

Before you begin, ensure you have:
- Python 3.10 or higher
- Node.js 18 or higher
- A Google Cloud Platform account
- A Google AI Studio account (for Gemini API)

## Step 1: Google Cloud Setup (OAuth & APIs)

### 1.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name: "AI Task Manager" (or your choice)
4. Click "Create"

### 1.2 Enable Required APIs

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for and enable these APIs:
   - **Gmail API**
   - **Google Calendar API**
   - **Google+ API** (for user profile info)

### 1.3 Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External (or Internal if using Google Workspace)
   - App name: AI Task Manager
   - User support email: Your email
   - Developer contact: Your email
   - Add scopes:
     - `userinfo.email`
     - `userinfo.profile`
     - `gmail.readonly`
     - `calendar.readonly`
   - Add test users (your email addresses during development)
4. Create OAuth Client ID:
   - Application type: **Web application**
   - Name: AI Task Manager Web Client
   - Authorized redirect URIs:
     - `http://localhost:8000/api/v1/auth/google/callback`
   - Click "Create"
5. **Save the Client ID and Client Secret** - you'll need these!

## Step 2: Gemini API Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Select your Google Cloud project (or create a new one)
4. **Save the API key** - you'll need it!

## Step 3: Backend Setup

### 3.1 Navigate to Backend Directory

```bash
cd backend
```

### 3.2 Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 3.4 Create Environment File

```bash
cp .env.example .env
```

### 3.5 Configure Environment Variables

Edit `.env` with your preferred text editor:

```bash
nano .env  # or vim, code, etc.
```

Fill in the following values:

#### Generate Security Keys

```bash
# Generate SECRET_KEY for JWT
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"

# Generate ENCRYPTION_KEY for OAuth tokens
python -c "from cryptography.fernet import Fernet; print('ENCRYPTION_KEY=' + Fernet.generate_key().decode())"
```

Copy these generated values into your `.env` file.

#### Add Google OAuth Credentials

```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback
```

#### Add Gemini API Key

```env
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-1.5-pro
```

#### Example Complete `.env` File

```env
# Application
APP_NAME=AI Task Manager
DEBUG=False
API_V1_PREFIX=/api/v1

# Database
DATABASE_URL=sqlite:///./taskmanager.db

# Security - JWT
SECRET_KEY=your-generated-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Security - Token Encryption
ENCRYPTION_KEY=your-generated-fernet-key-here

# Google OAuth
GOOGLE_CLIENT_ID=123456789.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback

# Gemini AI
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-1.5-pro

# Background Jobs
SCHEDULER_TIMEZONE=UTC
DAILY_SYNC_HOUR=2
DAILY_SYNC_MINUTE=0

# CORS
CORS_ORIGINS=http://localhost:5173

# Data Collection
GMAIL_LOOKBACK_DAYS=14
CALENDAR_LOOKBACK_DAYS=7
CALENDAR_LOOKFORWARD_DAYS=14
LEARNING_CONTEXT_WEEKS=4
```

### 3.6 Initialize Database (Optional)

If you want to use Alembic for migrations:

```bash
alembic upgrade head
```

Otherwise, the database will be auto-created when you first run the app.

### 3.7 Start Backend Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload

# Or using Python directly
python -m app.main
```

The backend should now be running at `http://localhost:8000`

Verify it's working by visiting: `http://localhost:8000/docs` (FastAPI auto-generated docs)

## Step 4: Frontend Setup

### 4.1 Open New Terminal

Keep the backend running and open a new terminal window.

### 4.2 Navigate to Frontend Directory

```bash
cd frontend
```

### 4.3 Install Dependencies

```bash
npm install
```

This will install all required packages including React, TypeScript, Tailwind CSS, etc.

### 4.4 Verify Environment File

The `.env` file should already exist with:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### 4.5 Start Frontend Development Server

```bash
npm run dev
```

The frontend should now be running at `http://localhost:5173`

## Step 5: First Time Usage

### 5.1 Access the Application

1. Open your browser and navigate to `http://localhost:5173`
2. You should see the landing page

### 5.2 Sign In

1. Click "Get Started" or "Sign in with Google"
2. You'll be redirected to Google's OAuth consent screen
3. Select your Google account
4. Grant the requested permissions:
   - View your email address
   - View your basic profile info
   - Read your Gmail messages
   - View your Calendar events
5. You'll be redirected back to the app at the Dashboard

### 5.3 Initial Data Sync

After signing in for the first time:

1. Click the "Sync Now" button in the Dashboard
2. Wait for the sync to complete (this may take a minute depending on your email/calendar volume)
3. Tasks will start appearing on your dashboard

## Step 6: Verify Everything Works

### 6.1 Check Backend Logs

In the backend terminal, you should see:
- Server startup messages
- API requests being logged
- Database operations
- Scheduler startup message

### 6.2 Check Frontend

In the browser:
- You should see your name/email in the header
- Dashboard shows task statistics
- Tasks are displayed (after sync)
- You can edit task priorities
- You can mark tasks as done
- You can mark false positives as "AI error"

### 6.3 Test API Documentation

Visit `http://localhost:8000/docs` to see the interactive API documentation (Swagger UI).

## Troubleshooting

### Backend Issues

**Error: No module named 'app'**
- Make sure you're in the `backend` directory
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**Error: Could not validate credentials (OAuth)**
- Double-check your `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`
- Verify redirect URI matches exactly: `http://localhost:8000/api/v1/auth/google/callback`
- Check that you added your email as a test user in Google Cloud Console

**Error: Invalid ENCRYPTION_KEY**
- Make sure you generated it correctly using the command provided
- Verify it's a valid Fernet key (should be 44 characters)

**Database errors**
- Delete `taskmanager.db` and restart to recreate
- Or run `alembic upgrade head` to apply migrations

### Frontend Issues

**Blank page or errors**
- Check browser console for errors (F12)
- Verify backend is running at `http://localhost:8000`
- Check that `.env` has correct `VITE_API_BASE_URL`
- Clear browser cache and reload

**CORS errors**
- Verify `CORS_ORIGINS` in backend `.env` includes `http://localhost:5173`
- Restart backend after changing CORS settings

**OAuth redirect not working**
- Check that redirect URI in Google Cloud Console matches exactly
- Make sure you're using `http://localhost:8000` (not 127.0.0.1)

### API Issues

**Gemini API errors**
- Verify API key is correct
- Check quota limits at [Google AI Studio](https://makersuite.google.com/)
- Review backend logs for specific error messages

**Gmail/Calendar not syncing**
- Check that APIs are enabled in Google Cloud Console
- Verify you granted the necessary permissions during OAuth
- Check backend logs for specific errors
- Try manual sync with "Sync Now" button

## Next Steps

Once everything is working:

1. **Test the learning system**: Edit some tasks (change priorities, mark as done, mark as AI error)
2. **Wait for automatic sync**: The system syncs daily at 2 AM (configurable)
3. **Monitor improvements**: Over 4 weeks, the AI will learn your preferences
4. **Explore API**: Check out the interactive docs at `/docs`

## Production Deployment

For production deployment:

1. **Update OAuth redirect URI** in Google Cloud Console
2. **Change `DEBUG=False`** in backend `.env`
3. **Use production database** (MySQL instead of SQLite)
4. **Add proper SECRET_KEY and ENCRYPTION_KEY** (never use development keys)
5. **Configure CORS_ORIGINS** for your production domain
6. **Build frontend**: `npm run build`
7. **Serve frontend** with nginx or similar
8. **Use production WSGI server** like gunicorn for backend
9. **Setup HTTPS** with SSL certificates
10. **Configure background job runner** (systemd service, supervisor, etc.)

## Support

If you encounter issues:
1. Check the backend logs for error messages
2. Check browser console for frontend errors
3. Review this guide carefully
4. Check API documentation at `/docs`

## Security Reminders

- Never commit `.env` files to version control
- Use strong, randomly generated keys
- Regularly rotate your API keys
- Monitor OAuth token usage
- Review Google Cloud Console for suspicious activity
