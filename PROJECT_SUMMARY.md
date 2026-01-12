# AI Task Manager - Project Summary

## 🎉 Project Complete!

A full-stack AI-powered task management application that automatically extracts actionable tasks from Gmail and Google Calendar using Gemini AI.

## 📁 Project Structure

```
claude-test/
├── backend/                        # FastAPI Backend
│   ├── app/
│   │   ├── api/                   # API Routes
│   │   │   ├── deps.py           # Auth & DB dependencies
│   │   │   └── v1/
│   │   │       ├── auth.py       # OAuth endpoints
│   │   │       ├── tasks.py      # Task CRUD
│   │   │       └── users.py      # User profile
│   │   ├── jobs/                 # Background Jobs
│   │   │   ├── scheduler.py      # APScheduler setup
│   │   │   └── daily_sync.py     # Daily data collection
│   │   ├── models/               # SQLAlchemy Models
│   │   │   ├── user.py          # User with OAuth tokens
│   │   │   ├── task.py          # Task model
│   │   │   └── task_edit.py     # Edit tracking
│   │   ├── schemas/              # Pydantic Schemas
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   └── auth.py
│   │   ├── services/             # Business Logic
│   │   │   ├── auth_service.py       # OAuth flow
│   │   │   ├── gmail_service.py      # Gmail API
│   │   │   ├── calendar_service.py   # Calendar API
│   │   │   ├── gemini_service.py     # Gemini AI
│   │   │   └── task_extraction.py    # Orchestration
│   │   ├── utils/                # Utilities
│   │   │   ├── security.py       # Token encryption
│   │   │   └── date_utils.py     # Date helpers
│   │   ├── config.py             # Settings
│   │   ├── database.py           # DB setup
│   │   └── main.py               # FastAPI app
│   ├── alembic/                  # Database Migrations
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example             # Environment template
│   └── .env                     # Your configuration
│
├── frontend/                     # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   │   └── ProtectedRoute.tsx
│   │   │   ├── layout/
│   │   │   │   ├── Header.tsx
│   │   │   │   └── Layout.tsx
│   │   │   └── tasks/
│   │   │       ├── TaskItem.tsx      # Task with edit controls
│   │   │       ├── TaskList.tsx      # List of tasks
│   │   │       └── TaskFilters.tsx   # Filter UI
│   │   ├── context/
│   │   │   └── AuthContext.tsx       # Global auth state
│   │   ├── hooks/
│   │   │   └── useTasks.ts          # React Query hooks
│   │   ├── pages/
│   │   │   ├── Home.tsx             # Landing page
│   │   │   ├── Login.tsx            # Sign in page
│   │   │   ├── AuthCallback.tsx     # OAuth handler
│   │   │   └── Dashboard.tsx        # Main app
│   │   ├── services/
│   │   │   ├── api.ts              # Axios instance
│   │   │   ├── authService.ts      # Auth API
│   │   │   └── taskService.ts      # Task API
│   │   ├── types/
│   │   │   ├── user.ts
│   │   │   └── task.ts
│   │   ├── lib/
│   │   │   └── utils.ts            # Helper functions
│   │   ├── App.tsx                 # Root component
│   │   ├── main.tsx                # Entry point
│   │   └── index.css               # Tailwind styles
│   ├── package.json                # Dependencies
│   ├── vite.config.ts             # Vite config
│   ├── tailwind.config.js         # Tailwind config
│   ├── tsconfig.json              # TypeScript config
│   ├── .env.example               # Environment template
│   └── .env                       # Your configuration
│
├── README.md                      # Project overview
├── SETUP.md                       # Detailed setup guide
├── .gitignore                     # Git ignore rules
└── PROJECT_SUMMARY.md             # This file
```

## ✨ Features Implemented

### Backend Features
- ✅ Google OAuth 2.0 authentication
- ✅ JWT session management
- ✅ Encrypted OAuth token storage (Fernet)
- ✅ Gmail API integration (last 14 days)
- ✅ Google Calendar API integration (last 7 days + next 14 days)
- ✅ Gemini AI task extraction
- ✅ Learning system (analyzes last 4 weeks of edits)
- ✅ Task CRUD operations
- ✅ Task edit tracking
- ✅ Background jobs (APScheduler - daily sync at 2 AM)
- ✅ RESTful API with FastAPI
- ✅ SQLite database (easily upgradeable to MySQL)
- ✅ Alembic database migrations
- ✅ Auto-generated API documentation (Swagger)
- ✅ CORS configuration
- ✅ Token refresh logic

### Frontend Features
- ✅ React + TypeScript + Vite
- ✅ Tailwind CSS styling
- ✅ Google OAuth sign-in
- ✅ Protected routes
- ✅ Task dashboard with statistics
- ✅ Task list with filtering
- ✅ Priority editing (dropdown)
- ✅ Mark tasks as done (checkbox)
- ✅ Mark false positives as "AI error"
- ✅ Manual sync button
- ✅ Source type badges (Gmail/Calendar)
- ✅ Links to original sources
- ✅ Due date display
- ✅ Responsive design
- ✅ Loading states
- ✅ Error handling
- ✅ React Query for data management
- ✅ Axios with auth interceptors

## 🔧 Technology Stack

### Backend
| Technology | Purpose |
|------------|---------|
| FastAPI | Web framework |
| SQLAlchemy | ORM for database |
| Alembic | Database migrations |
| Pydantic | Data validation |
| APScheduler | Background jobs |
| Google API Client | Gmail & Calendar |
| Gemini API | AI task extraction |
| Cryptography (Fernet) | Token encryption |
| Python-Jose | JWT handling |

### Frontend
| Technology | Purpose |
|------------|---------|
| React 18 | UI library |
| TypeScript | Type safety |
| Vite | Build tool |
| TanStack Query | Server state management |
| React Router | Routing |
| Axios | HTTP client |
| Tailwind CSS | Styling |

## 🚀 Quick Start

### 1. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
uvicorn app.main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Access the App
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📝 API Endpoints

### Authentication
- `POST /api/v1/auth/google/login` - Get OAuth URL
- `GET /api/v1/auth/google/callback` - Handle OAuth callback
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/logout` - Logout

### Tasks
- `GET /api/v1/tasks` - List tasks (with filters)
- `GET /api/v1/tasks/{id}` - Get task
- `PATCH /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task
- `POST /api/v1/tasks/trigger-sync` - Manual sync

### Users
- `GET /api/v1/users/me` - Get profile
- `PATCH /api/v1/users/me` - Update profile

## 🗄️ Database Schema

### users
- Stores user information
- Encrypted OAuth tokens (access_token, refresh_token)
- Last sync timestamp
- Active status

### tasks
- Task description, priority, due date
- Source type (gmail/calendar)
- Source link and ID
- Completion status
- AI error flag
- Extraction timestamp

### task_edits
- Tracks all user edits
- Edit type (priority_changed, marked_done, marked_ai_error)
- Old and new values
- Timestamp for learning

## 🤖 AI Learning System

The system learns from your behavior:

1. **Priority Adjustments**: Learns if you tend to increase/decrease priorities
2. **AI Errors**: Learns what you consider "not a task"
3. **Completion Patterns**: Understands which task types you complete

Learning context includes last 4 weeks of edits and is sent to Gemini for improved task extraction.

## 🔐 Security Features

- **OAuth Tokens**: Encrypted with Fernet before database storage
- **JWT Sessions**: Secure session management with expiration
- **CSRF Protection**: State parameter in OAuth flow
- **CORS**: Configurable allowed origins
- **Input Validation**: Pydantic schemas validate all inputs
- **Rate Limiting**: Ready for implementation (slowapi)

## 📊 Task Extraction Process

1. **Data Collection** (Daily at 2 AM or manual)
   - Fetch Gmail threads (last 14 days)
   - Fetch Calendar events (last 7 days + next 14 days)

2. **Learning Context Building**
   - Query last 4 weeks of task edits
   - Analyze patterns (priority changes, AI errors, completions)
   - Summarize into concise context

3. **AI Processing**
   - Send emails, calendar, and learning context to Gemini
   - Gemini extracts actionable tasks
   - Returns JSON with: description, priority, due_date, source

4. **Task Storage**
   - Validate and normalize extracted tasks
   - Check for duplicates using source_id
   - Insert new tasks into database
   - Link to original source (Gmail/Calendar URL)

## 🎯 Key Design Decisions

1. **Monorepo Structure**: Backend and frontend in same repo for easier development
2. **SQLite First**: Easy development, trivial MySQL migration later
3. **Token Encryption**: OAuth tokens encrypted at rest for security
4. **Learning from Edits**: System improves over time based on user feedback
5. **Source Links**: Always link back to original email/calendar entry
6. **AI Error Flag**: Separate from "done" to track false positives
7. **Background Jobs**: APScheduler for simplicity, can scale to Celery later
8. **React Query**: Simplifies server state management and caching

## 🔄 Workflow

### User Workflow
1. Sign in with Google → Grant permissions
2. System syncs Gmail & Calendar daily
3. View extracted tasks on Dashboard
4. Edit priorities, mark as done, flag AI errors
5. System learns from edits over 4 weeks
6. Task extraction becomes more accurate

### Technical Workflow
1. OAuth flow → Store encrypted tokens
2. Daily job → Fetch emails & calendar
3. Build learning context → Send to Gemini
4. Parse AI response → Store tasks
5. User edits → Track in task_edits
6. Next sync → Include learning context

## 🚧 Future Enhancements

- [ ] Email/push notifications for reminders
- [ ] Multi-calendar support
- [ ] Task categories and tags
- [ ] Recurring task detection
- [ ] Analytics dashboard
- [ ] Mobile app (PWA or React Native)
- [ ] Real-time updates via webhooks
- [ ] Collaborative tasks
- [ ] Task comments and notes
- [ ] Advanced filtering and search
- [ ] Export tasks (CSV, JSON)
- [ ] Dark mode

## 📦 Dependencies

### Backend (requirements.txt)
- fastapi, uvicorn - Web framework
- sqlalchemy, alembic - Database
- pydantic, pydantic-settings - Validation
- python-jose, cryptography - Security
- google-api-python-client - Google APIs
- google-generativeai - Gemini
- apscheduler - Background jobs

### Frontend (package.json)
- react, react-dom - UI library
- react-router-dom - Routing
- @tanstack/react-query - Data fetching
- axios - HTTP client
- tailwindcss - Styling
- typescript - Type safety
- vite - Build tool

## 🎓 Learning Resources

### FastAPI
- [Official Docs](https://fastapi.tiangolo.com/)
- [Tutorial](https://fastapi.tiangolo.com/tutorial/)

### React Query
- [TanStack Query](https://tanstack.com/query/latest)

### Google APIs
- [Gmail API](https://developers.google.com/gmail/api)
- [Calendar API](https://developers.google.com/calendar/api)
- [OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)

### Gemini
- [Google AI Studio](https://makersuite.google.com/)
- [Gemini API Docs](https://ai.google.dev/docs)

## 📄 Documentation Files

1. **README.md** - Project overview and features
2. **SETUP.md** - Detailed setup instructions
3. **PROJECT_SUMMARY.md** - This file (complete overview)
4. **.env.example** - Environment variable templates (backend & frontend)

## ✅ Checklist Before Running

- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] Google Cloud project created
- [ ] Gmail & Calendar APIs enabled
- [ ] OAuth credentials created
- [ ] Gemini API key obtained
- [ ] Backend `.env` configured
- [ ] Backend dependencies installed
- [ ] Frontend `.env` configured
- [ ] Frontend dependencies installed

## 🎉 You're All Set!

The application is fully functional and ready to use. Follow the SETUP.md guide to configure your environment and start using the AI Task Manager!

### Quick Commands

**Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

**Access:**
- App: http://localhost:5173
- API: http://localhost:8000/docs

Enjoy your AI-powered task management! 🚀
