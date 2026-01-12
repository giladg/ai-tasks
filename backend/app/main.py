from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import init_db
from app.api.v1 import auth, tasks, users
from app.jobs.scheduler import start_scheduler, shutdown_scheduler

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI app.
    Handles startup and shutdown events.
    """
    # Startup
    print("Starting up...")
    init_db()  # Initialize database tables
    start_scheduler()  # Start background job scheduler
    print("Application started successfully")

    yield

    # Shutdown
    print("Shutting down...")
    shutdown_scheduler()  # Stop background job scheduler
    print("Application shut down successfully")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered task management system that extracts tasks from Gmail and Google Calendar",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "message": "AI Task Manager API",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Include API routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX, tags=["Authentication"])
app.include_router(tasks.router, prefix=settings.API_V1_PREFIX, tags=["Tasks"])
app.include_router(users.router, prefix=settings.API_V1_PREFIX, tags=["Users"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
