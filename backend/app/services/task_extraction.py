from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict
from collections import Counter

from app.models.user import User
from app.models.task import Task, SourceTypeEnum
from app.models.task_edit import TaskEdit, EditTypeEnum
from app.services.gmail_service import create_gmail_service
from app.services.calendar_service import create_calendar_service
from app.services.gemini_service import gemini_service
from app.services.auth_service import auth_service
from app.config import get_settings

settings = get_settings()


class TaskExtractionService:
    """
    Service for orchestrating task extraction from Gmail and Calendar using Gemini.
    Includes learning from user's edit history.
    """

    def __init__(self, db: Session):
        """
        Initialize task extraction service.

        Args:
            db: Database session
        """
        self.db = db

    def extract_tasks_for_user(self, user: User) -> Dict:
        """
        Extract tasks for a user from Gmail and Calendar.

        Args:
            user: User object

        Returns:
            Dictionary with extraction results (tasks_created, errors, etc.)
        """
        result = {
            'tasks_created': 0,
            'tasks_skipped': 0,
            'errors': []
        }

        try:
            # Get valid access token (refresh if needed)
            access_token = auth_service.get_valid_access_token(self.db, user)

            # Fetch Gmail threads
            gmail_threads = []
            try:
                gmail_service = create_gmail_service(access_token)
                threads = gmail_service.fetch_threads()

                # Format threads for Gemini
                for thread in threads:
                    gmail_threads.append({
                        'thread_id': thread['thread_id'],
                        'formatted': gmail_service.format_thread_for_ai(thread),
                        'url': thread['url']
                    })

                print(f"Fetched {len(gmail_threads)} Gmail threads for user {user.id}")
            except Exception as e:
                error_msg = f"Error fetching Gmail: {str(e)}"
                result['errors'].append(error_msg)
                print(error_msg)

            # Fetch Calendar events
            calendar_events = []
            try:
                calendar_service = create_calendar_service(access_token)
                events = calendar_service.fetch_events()

                # Format events for Gemini
                for event in events:
                    calendar_events.append({
                        'event_id': event['event_id'],
                        'formatted': calendar_service.format_event_for_ai(event),
                        'url': event['url']
                    })

                print(f"Fetched {len(calendar_events)} Calendar events for user {user.id}")
            except Exception as e:
                error_msg = f"Error fetching Calendar: {str(e)}"
                result['errors'].append(error_msg)
                print(error_msg)

            # Build learning context from user's edit history
            learning_context = self.build_learning_context(user)

            # Get completed tasks to avoid re-extraction
            completed_task_sources = self.get_completed_task_sources(user)

            # Extract tasks using Gemini
            if gmail_threads or calendar_events:
                try:
                    extracted_tasks = gemini_service.extract_tasks(
                        gmail_threads=gmail_threads,
                        calendar_events=calendar_events,
                        learning_context=learning_context,
                        completed_task_sources=completed_task_sources
                    )

                    print(f"Gemini extracted {len(extracted_tasks)} tasks for user {user.id}")

                    # Create tasks in database
                    for task_data in extracted_tasks:
                        created = self.create_task_from_extraction(user, task_data, gmail_threads, calendar_events)
                        if created:
                            result['tasks_created'] += 1
                        else:
                            result['tasks_skipped'] += 1

                except Exception as e:
                    error_msg = f"Error in Gemini extraction: {str(e)}"
                    result['errors'].append(error_msg)
                    print(error_msg)

            # Update user's last sync timestamp
            user.last_sync_at = datetime.utcnow()
            self.db.commit()

        except Exception as e:
            error_msg = f"Error in task extraction: {str(e)}"
            result['errors'].append(error_msg)
            print(error_msg)

        return result

    def get_completed_task_sources(self, user: User) -> Dict[str, List[str]]:
        """
        Get source IDs of tasks that have been marked as done.
        This prevents re-extracting tasks that the user already completed.

        Args:
            user: User object

        Returns:
            Dictionary with 'gmail' and 'calendar' lists of completed source_ids
        """
        # Query completed tasks
        completed_tasks = self.db.query(Task).filter(
            Task.user_id == user.id,
            Task.is_done == True,
            Task.source_id.isnot(None)
        ).all()

        # Organize by source type
        completed_sources = {
            'gmail': [],
            'calendar': []
        }

        for task in completed_tasks:
            source_type = task.source_type.value  # Convert enum to string
            if source_type in completed_sources:
                completed_sources[source_type].append(task.source_id)

        return completed_sources

    def build_learning_context(self, user: User) -> str:
        """
        Build learning context from user's edit history.

        Args:
            user: User object

        Returns:
            Learning context string for Gemini
        """
        # Get edits from last N weeks
        weeks_ago = datetime.utcnow() - timedelta(weeks=settings.LEARNING_CONTEXT_WEEKS)

        edits = self.db.query(TaskEdit).filter(
            TaskEdit.user_id == user.id,
            TaskEdit.created_at >= weeks_ago
        ).all()

        if not edits:
            return "No user edit history available yet."

        # Analyze patterns
        context_parts = []

        # Count edit types
        edit_counts = Counter([edit.edit_type for edit in edits])

        # Priority changes
        priority_changes = [e for e in edits if e.edit_type == EditTypeEnum.priority_changed]
        if priority_changes:
            context_parts.append(
                f"User has adjusted task priorities {len(priority_changes)} times. "
                f"Pay attention to priority assignment."
            )

            # Analyze priority change patterns
            priority_ups = sum(1 for e in priority_changes if self._is_priority_increase(e.old_value, e.new_value))
            priority_downs = len(priority_changes) - priority_ups
            if priority_ups > priority_downs:
                context_parts.append(
                    "User tends to increase task priorities, suggesting initial assignments may be too low."
                )
            elif priority_downs > priority_ups:
                context_parts.append(
                    "User tends to decrease task priorities, suggesting initial assignments may be too high."
                )

        # AI errors (false positives)
        ai_errors = [e for e in edits if e.edit_type == EditTypeEnum.marked_ai_error]
        if ai_errors:
            context_parts.append(
                f"User marked {len(ai_errors)} items as 'not a task' (false positives). "
                f"Be more conservative in task extraction."
            )

            # Get examples of false positives
            false_positive_tasks = []
            for edit in ai_errors[:5]:  # Get up to 5 examples
                task = self.db.query(Task).filter(Task.id == edit.task_id).first()
                if task:
                    false_positive_tasks.append(task.description[:100])

            if false_positive_tasks:
                context_parts.append(
                    f"Examples of items incorrectly identified as tasks: "
                    f"{'; '.join(false_positive_tasks)}"
                )

        # Completion rate
        marked_done = [e for e in edits if e.edit_type == EditTypeEnum.marked_done]
        if marked_done:
            context_parts.append(
                f"User has completed {len(marked_done)} tasks. "
                f"Extract tasks that are genuinely actionable."
            )

        if not context_parts:
            return "User has edit history but no clear patterns yet."

        return "\n".join(context_parts)

    def _is_priority_increase(self, old_priority: str, new_priority: str) -> bool:
        """Check if priority changed from lower to higher"""
        priority_order = {'low': 0, 'medium': 1, 'high': 2, 'urgent': 3}
        old_val = priority_order.get(old_priority, 1)
        new_val = priority_order.get(new_priority, 1)
        return new_val > old_val

    def create_task_from_extraction(
        self,
        user: User,
        task_data: Dict,
        gmail_threads: List[Dict],
        calendar_events: List[Dict]
    ) -> bool:
        """
        Create a task from extracted data, with duplicate prevention.

        Args:
            user: User object
            task_data: Extracted task data from Gemini
            gmail_threads: List of Gmail threads (for URL lookup)
            calendar_events: List of Calendar events (for URL lookup)

        Returns:
            True if task was created, False if skipped (duplicate)
        """
        # Check for duplicate by source_id
        source_id = task_data.get('source_id')
        if source_id:
            existing = self.db.query(Task).filter(
                Task.user_id == user.id,
                Task.source_id == source_id
            ).first()

            if existing:
                print(f"Skipping duplicate task with source_id: {source_id}")
                return False

        # Get source URL
        source_link = None
        source_type = task_data['source_type']

        if source_type == 'gmail':
            # Find matching thread
            for thread in gmail_threads:
                if thread['thread_id'] == source_id:
                    source_link = thread['url']
                    break
        elif source_type == 'calendar':
            # Find matching event
            for event in calendar_events:
                if event['event_id'] == source_id:
                    source_link = event['url']
                    break

        # Parse due_date string to date object
        due_date = None
        if task_data['due_date']:
            try:
                due_date = datetime.strptime(task_data['due_date'], '%Y-%m-%d').date()
            except (ValueError, TypeError):
                print(f"Warning: Could not parse due_date: {task_data['due_date']}")
                due_date = None

        # Create task
        task = Task(
            user_id=user.id,
            description=task_data['description'],
            priority=task_data['priority'],
            due_date=due_date,
            source_type=SourceTypeEnum[source_type],
            source_link=source_link,
            source_id=source_id,
            extracted_at=datetime.utcnow()
        )

        self.db.add(task)
        self.db.commit()

        print(f"Created task: {task.description[:50]}...")
        return True


def extract_tasks_for_user(db: Session, user: User) -> Dict:
    """
    Convenience function to extract tasks for a user.

    Args:
        db: Database session
        user: User object

    Returns:
        Extraction result dictionary
    """
    service = TaskExtractionService(db)
    return service.extract_tasks_for_user(user)
