from datetime import datetime
from sqlalchemy.orm import Session
import logging

from app.database import SessionLocal
from app.models.user import User
from app.services.task_extraction import extract_tasks_for_user

# Configure logging
logger = logging.getLogger(__name__)


def daily_sync_all_users():
    """
    Daily job to sync data for all active users.
    Fetches Gmail and Calendar data, extracts tasks using Gemini.
    """
    logger.info(f"Starting daily sync job at {datetime.utcnow()}")
    print(f"[DAILY_SYNC] Starting daily sync job at {datetime.utcnow()}")

    db = SessionLocal()

    try:
        # Get all active users
        users = db.query(User).filter(User.is_active == True).all()

        logger.info(f"Found {len(users)} active users to sync")
        print(f"[DAILY_SYNC] Found {len(users)} active users to sync")

        success_count = 0
        error_count = 0

        # Process each user
        for user in users:
            try:
                logger.info(f"Syncing user {user.id} ({user.email})")
                print(f"\n[DAILY_SYNC] --- Syncing user {user.id} ({user.email}) ---")

                # Extract tasks for user
                result = extract_tasks_for_user(db, user)

                logger.info(f"User {user.id} sync complete: created={result['tasks_created']}, skipped={result['tasks_skipped']}")
                print(f"[DAILY_SYNC] User {user.id} sync complete:")
                print(f"[DAILY_SYNC]   - Tasks created: {result['tasks_created']}")
                print(f"[DAILY_SYNC]   - Tasks skipped: {result['tasks_skipped']}")

                if result['errors']:
                    logger.error(f"User {user.id} had {len(result['errors'])} errors")
                    print(f"[DAILY_SYNC]   - Errors: {len(result['errors'])}")
                    for error in result['errors']:
                        logger.error(f"  Error: {error}")
                        print(f"[DAILY_SYNC]     * {error}")
                    error_count += 1
                else:
                    success_count += 1

            except Exception as e:
                error_count += 1
                logger.exception(f"Error syncing user {user.id}")
                print(f"[DAILY_SYNC] Error syncing user {user.id}: {str(e)}")
                # Continue with next user even if one fails
                continue

        logger.info(f"Daily sync job complete: success={success_count}, errors={error_count}")
        print(f"\n[DAILY_SYNC] === Daily sync job complete ===")
        print(f"[DAILY_SYNC] Success: {success_count}, Errors: {error_count}")

    except Exception as e:
        logger.critical(f"Critical error in daily sync job: {str(e)}")
        print(f"[DAILY_SYNC] Critical error in daily sync job: {str(e)}")

    finally:
        db.close()


def sync_user_data(user_id: int):
    """
    Sync data for a specific user.
    Used for manual trigger via API endpoint.

    Args:
        user_id: User ID to sync
    """
    logger.info(f"Starting manual sync for user {user_id} at {datetime.utcnow()}")
    print(f"[SYNC] Starting manual sync for user {user_id} at {datetime.utcnow()}")

    db = SessionLocal()

    try:
        # Get user
        user = db.query(User).filter(
            User.id == user_id,
            User.is_active == True
        ).first()

        if not user:
            logger.warning(f"User {user_id} not found or inactive")
            print(f"[SYNC] User {user_id} not found or inactive")
            return

        # Extract tasks
        result = extract_tasks_for_user(db, user)

        logger.info(f"User {user_id} sync complete: created={result['tasks_created']}, skipped={result['tasks_skipped']}, errors={len(result['errors'])}")
        print(f"[SYNC] User {user_id} sync complete:")
        print(f"[SYNC]   - Tasks created: {result['tasks_created']}")
        print(f"[SYNC]   - Tasks skipped: {result['tasks_skipped']}")

        if result['errors']:
            logger.error(f"User {user_id} sync had {len(result['errors'])} errors")
            print(f"[SYNC]   - Errors: {len(result['errors'])}")
            for error in result['errors']:
                logger.error(f"  Sync error: {error}")
                print(f"[SYNC]     * {error}")

    except Exception as e:
        logger.exception(f"Error syncing user {user_id}")
        print(f"[SYNC] Error syncing user {user_id}: {str(e)}")

    finally:
        db.close()
