# AI-Powered Task Management Application

A full-stack web application that uses Google OAuth to access Gmail and Calendar data, extracts actionable tasks using Gemini AI, and learns from user feedback to improve task extraction over time.

## Features

- **Google OAuth Authentication**: Sign in with Google account
- **Gmail Integration**: Fetches email threads from last 14 days
- **Calendar Integration**: Fetches events from last 7 days + next 14 days
- **AI Task Extraction**: Uses Gemini AI to extract actionable tasks
- **Learning System**: Improves over time based on user edits (last 4 weeks)
- **Task Management**: Edit priority, mark as done, mark as AI error
- **Background Jobs**: Daily automated data collection (APScheduler)

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **SQLite**: Database (easily upgradeable to MySQL)
- **APScheduler**: Background job scheduling
- **Google APIs**: Gmail, Calendar, OAuth 2.0
- **Gemini AI**: Task extraction

### Frontend
- **React**: UI library
- **TypeScript**: Type safety
- **Vite**: Fast build tool
- **Tailwind CSS**: Styling
- **TanStack Query**: Server state management
- **React Router**: Routing

## Project Structure

```
claude-test/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   ├── jobs/        # Background jobs
│   │   └── utils/       # Utilities
│   ├── alembic/         # Database migrations
│   └── requirements.txt
│
└── frontend/            # React frontend
    ├── src/
    │   ├── components/  # React components
    │   ├── pages/       # Page components
    │   ├── services/    # API calls
    │   ├── hooks/       # Custom hooks
    │   └── context/     # React context
    └── package.json
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- Google Cloud Project with OAuth 2.0 credentials
- Gemini API key

### 1. Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - Gmail API
   - Google Calendar API
   - Google+ API (for user info)
4. Create OAuth 2.0 credentials:
   - Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:8000/api/v1/auth/google/callback`
   - Save the Client ID and Client Secret

### 2. Gemini API Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key for Gemini

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
cp .env.example .env
```

Edit `.env` and fill in the required values:

```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate ENCRYPTION_KEY
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Add your Google OAuth credentials
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret

# Add your Gemini API key
GEMINI_API_KEY=your-gemini-api-key
```

Initialize the database:

```bash
# Option 1: Using Alembic (recommended for production)
alembic upgrade head

# Option 2: Auto-create tables on first run (development)
# Tables will be created automatically when you start the server
```

Run the backend:

```bash
# Development mode (with auto-reload)
uvicorn app.main:app --reload

# Or using Python directly
python -m app.main
```

The backend will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file from example
cp .env.example .env

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

### First Time Setup

1. Start the backend server
2. Start the frontend development server
3. Navigate to `http://localhost:5173`
4. Click "Sign in with Google"
5. Grant permissions for Gmail and Calendar access
6. You'll be redirected to the dashboard

### Manual Sync

To manually trigger a data sync for testing:

```bash
# Using the API
curl -X POST http://localhost:8000/api/v1/tasks/trigger-sync \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Or use the "Sync Now" button in the UI (when implemented).

### Viewing Tasks

- Tasks are automatically synced daily at 2 AM (configurable in `.env`)
- View your tasks on the dashboard
- Filter by date, priority, status, etc.
- Edit task priority
- Mark tasks as done
- Mark false positives as "AI error"

### Learning System

The system learns from your edits:
- Priority changes: Learns your priority preferences
- Marking as "AI error": Learns what's NOT a task
- Completion patterns: Understands task types

After 4 weeks of usage, the AI will be more accurate for your specific needs.

## Development

### Backend

#### Running Tests

```bash
cd backend
pytest
```

#### Creating a Migration

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

#### Manual Token Refresh

```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Frontend

#### Build for Production

```bash
cd frontend
npm run build
```

#### Preview Production Build

```bash
npm run preview
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/google/login` - Get Google OAuth URL
- `GET /api/v1/auth/google/callback` - OAuth callback handler
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - Logout

### Tasks
- `GET /api/v1/tasks` - List tasks (with filters)
- `GET /api/v1/tasks/{id}` - Get single task
- `PATCH /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task
- `POST /api/v1/tasks/trigger-sync` - Manual sync

### Users
- `GET /api/v1/users/me` - Get user profile
- `PATCH /api/v1/users/me` - Update profile

## Configuration

### Backend Environment Variables

See `backend/.env.example` for all available options.

Key settings:
- `DAILY_SYNC_HOUR`: Hour of day for automated sync (0-23, default: 2)
- `GMAIL_LOOKBACK_DAYS`: Days to fetch Gmail data (default: 14)
- `CALENDAR_LOOKBACK_DAYS`: Past days for calendar (default: 7)
- `CALENDAR_LOOKFORWARD_DAYS`: Future days for calendar (default: 14)
- `LEARNING_CONTEXT_WEEKS`: Weeks of edit history for learning (default: 4)

### Frontend Environment Variables

See `frontend/.env.example` for options.

## Database Migration (SQLite to MySQL)

When ready to migrate to MySQL:

1. Update `DATABASE_URL` in `.env`:
   ```
   DATABASE_URL=mysql+pymysql://user:password@localhost/taskmanager
   ```

2. Install MySQL driver:
   ```bash
   pip install pymysql
   ```

3. Run migrations:
   ```bash
   alembic upgrade head
   ```

The code is database-agnostic thanks to SQLAlchemy ORM.

## Troubleshooting

### OAuth Error: redirect_uri_mismatch

Make sure the redirect URI in Google Cloud Console exactly matches:
```
http://localhost:8000/api/v1/auth/google/callback
```

### Token Expired Errors

Tokens are automatically refreshed. If issues persist:
1. Check that `ENCRYPTION_KEY` hasn't changed
2. Try logging out and back in

### Gemini API Errors

1. Verify your API key is correct
2. Check quota limits at [Google AI Studio](https://makersuite.google.com/)
3. Review logs for specific error messages

### Background Job Not Running

1. Check logs for scheduler startup message
2. Verify `DAILY_SYNC_HOUR` and `SCHEDULER_TIMEZONE` settings
3. Test with manual sync endpoint

## Security Notes

- OAuth tokens are encrypted using Fernet before storage
- JWT tokens expire after 7 days (configurable)
- Never commit `.env` files to version control
- Use strong random keys for `SECRET_KEY` and `ENCRYPTION_KEY`

## Future Enhancements

- Email/push notifications
- Multi-calendar support
- Task categories and tags
- Recurring task detection
- Analytics dashboard
- Mobile app (PWA)
- Real-time updates via webhooks

## License

Private project - All rights reserved

## Support

For issues or questions, please refer to the project documentation or create an issue in the repository.
