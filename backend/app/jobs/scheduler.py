from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from app.config import get_settings

settings = get_settings()

# Create scheduler instance
scheduler = AsyncIOScheduler()


def start_scheduler():
    """
    Start the APScheduler for background jobs.
    Called on application startup.
    """
    from app.jobs.daily_sync import daily_sync_all_users

    # Get timezone
    tz = pytz.timezone(settings.SCHEDULER_TIMEZONE)

    # Schedule daily sync job
    scheduler.add_job(
        daily_sync_all_users,
        CronTrigger(
            hour=settings.DAILY_SYNC_HOUR,
            minute=settings.DAILY_SYNC_MINUTE,
            timezone=tz
        ),
        id='daily_sync',
        name='Daily data collection and task extraction for all users',
        replace_existing=True
    )

    print(f"Scheduled daily sync job at {settings.DAILY_SYNC_HOUR}:{settings.DAILY_SYNC_MINUTE:02d} {settings.SCHEDULER_TIMEZONE}")

    # Start the scheduler
    scheduler.start()
    print("APScheduler started successfully")


def shutdown_scheduler():
    """
    Shutdown the APScheduler.
    Called on application shutdown.
    """
    if scheduler.running:
        scheduler.shutdown()
        print("APScheduler shut down successfully")
