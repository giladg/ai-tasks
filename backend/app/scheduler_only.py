"""
Standalone scheduler script for running background jobs.
This runs only the APScheduler without the FastAPI web server.
"""
import time
import signal
import sys

from app.database import init_db
from app.jobs.scheduler import start_scheduler, shutdown_scheduler

# Flag to control the main loop
keep_running = True


def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    global keep_running
    print("\nReceived shutdown signal, stopping scheduler...")
    keep_running = False


def main():
    """Main function to run the scheduler."""
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("Starting background scheduler...")

    # Initialize database
    init_db()
    print("Database initialized")

    # Start the scheduler
    start_scheduler()
    print("Scheduler started successfully")

    # Keep the script running
    try:
        while keep_running:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        # Cleanup
        print("Shutting down scheduler...")
        shutdown_scheduler()
        print("Scheduler shut down successfully")
        sys.exit(0)


if __name__ == "__main__":
    main()
