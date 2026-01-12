from datetime import datetime
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.services.task_extraction import extract_tasks_for_user


def daily_sync_all_users():
    """
    Daily job to sync data for all active users.
    Fetches Gmail and Calendar data, extracts tasks using Gemini.
    """
    print(f"Starting daily sync job at {datetime.utcnow()}")

    db = SessionLocal()

    try:
        # Get all active users
        users = db.query(User).filter(User.is_active == True).all()

        print(f"Found {len(users)} active users to sync")

        success_count = 0
        error_count = 0

        # Process each user
        for user in users:
            try:
                print(f"\n--- Syncing user {user.id} ({user.email}) ---")

                # Extract tasks for user
                result = extract_tasks_for_user(db, user)

                print(f"User {user.id} sync complete:")
                print(f"  - Tasks created: {result['tasks_created']}")
                print(f"  - Tasks skipped: {result['tasks_skipped']}")

                if result['errors']:
                    print(f"  - Errors: {len(result['errors'])}")
                    for error in result['errors']:
                        print(f"    * {error}")
                    error_count += 1
                else:
                    success_count += 1

            except Exception as e:
                error_count += 1
                print(f"Error syncing user {user.id}: {str(e)}")
                # Continue with next user even if one fails
                continue

        print(f"\n=== Daily sync job complete ===")
        print(f"Success: {success_count}, Errors: {error_count}")

    except Exception as e:
        print(f"Critical error in daily sync job: {str(e)}")

    finally:
        db.close()


def sync_user_data(user_id: int):
    """
    Sync data for a specific user.
    Used for manual trigger via API endpoint.

    Args:
        user_id: User ID to sync
    """
    print(f"Starting manual sync for user {user_id} at {datetime.utcnow()}")

    db = SessionLocal()

    try:
        # Get user
        user = db.query(User).filter(
            User.id == user_id,
            User.is_active == True
        ).first()

        if not user:
            print(f"User {user_id} not found or inactive")
            return

        # Extract tasks
        result = extract_tasks_for_user(db, user)

        print(f"User {user_id} sync complete:")
        print(f"  - Tasks created: {result['tasks_created']}")
        print(f"  - Tasks skipped: {result['tasks_skipped']}")

        if result['errors']:
            print(f"  - Errors: {len(result['errors'])}")
            for error in result['errors']:
                print(f"    * {error}")

    except Exception as e:
        print(f"Error syncing user {user_id}: {str(e)}")

    finally:
        db.close()
