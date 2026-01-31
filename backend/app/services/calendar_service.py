from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timezone
from typing import List, Dict, Optional

from app.config import get_settings
from app.utils.date_utils import format_calendar_datetime, get_calendar_date_range

settings = get_settings()


class CalendarService:
    """Service for interacting with Google Calendar API"""

    def __init__(self, access_token: str):
        """
        Initialize Calendar service with access token.

        Args:
            access_token: Google OAuth access token
        """
        credentials = Credentials(token=access_token)
        self.service = build('calendar', 'v3', credentials=credentials)

    def fetch_events(
        self,
        lookback_days: Optional[int] = None,
        lookforward_days: Optional[int] = None
    ) -> List[Dict]:
        """
        Fetch calendar events from past N days and future M days.

        Args:
            lookback_days: Days to look back (default: from settings)
            lookforward_days: Days to look forward (default: from settings)

        Returns:
            List of event dictionaries with formatted data
        """
        if lookback_days is None:
            lookback_days = settings.CALENDAR_LOOKBACK_DAYS
        if lookforward_days is None:
            lookforward_days = settings.CALENDAR_LOOKFORWARD_DAYS

        try:
            # Get date range
            start_date, end_date = get_calendar_date_range(lookback_days, lookforward_days)

            # Format for Calendar API
            time_min = format_calendar_datetime(start_date)
            time_max = format_calendar_datetime(end_date)

            # Fetch events from primary calendar
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=time_min,
                timeMax=time_max,
                maxResults=100,  # Can be made configurable
                singleEvents=True,  # Expand recurring events
                orderBy='startTime'
            ).execute()

            events_data = events_result.get('items', [])

            # Format events
            events = []
            for event_data in events_data:
                event = self._format_event(event_data)
                if event:
                    events.append(event)

            return events

        except HttpError as error:
            print(f"An error occurred fetching Calendar events: {error}")
            raise

    def _format_event(self, event_data: Dict) -> Optional[Dict]:
        """
        Format raw event data into structured format.

        Args:
            event_data: Raw event data from Calendar API

        Returns:
            Formatted event dictionary
        """
        event_id = event_data.get('id')
        if not event_id:
            return None

        # Get event details
        summary = event_data.get('summary', '(No Title)')
        description = event_data.get('description', '')
        location = event_data.get('location', '')
        html_link = event_data.get('htmlLink', '')

        # Get start and end times
        start = event_data.get('start', {})
        end = event_data.get('end', {})

        # Handle all-day events vs timed events
        start_datetime = self._parse_datetime(start)
        end_datetime = self._parse_datetime(end)
        is_all_day = 'date' in start  # All-day events use 'date' instead of 'dateTime'

        # Get attendees
        attendees = event_data.get('attendees', [])
        attendee_emails = [a.get('email', '') for a in attendees if a.get('email')]

        # Get organizer
        organizer = event_data.get('organizer', {})
        organizer_email = organizer.get('email', '')

        # Get status
        status = event_data.get('status', 'confirmed')  # confirmed, tentative, cancelled

        # Build Calendar URL
        calendar_url = html_link if html_link else f"https://calendar.google.com/calendar/event?eid={event_id}"

        return {
            'event_id': event_id,
            'summary': summary,
            'description': description,
            'location': location,
            'start': start_datetime,
            'end': end_datetime,
            'is_all_day': is_all_day,
            'attendees': attendee_emails,
            'organizer': organizer_email,
            'status': status,
            'url': calendar_url
        }

    def _parse_datetime(self, time_dict: Dict) -> Optional[datetime]:
        """
        Parse datetime from Calendar API time object.

        Args:
            time_dict: Time dictionary with either 'dateTime' or 'date'

        Returns:
            Parsed datetime or None
        """
        # Try dateTime first (timed events)
        if 'dateTime' in time_dict:
            try:
                return datetime.fromisoformat(time_dict['dateTime'].replace('Z', '+00:00'))
            except:
                return None

        # Try date (all-day events)
        if 'date' in time_dict:
            try:
                return datetime.strptime(time_dict['date'], '%Y-%m-%d')
            except:
                return None

        return None

    def format_event_for_ai(self, event: Dict) -> str:
        """
        Format event data for AI consumption.

        Args:
            event: Event dictionary

        Returns:
            Formatted string for Gemini
        """
        # Format times
        start_str = event['start'].strftime('%Y-%m-%d %H:%M') if event['start'] else 'Unknown'
        end_str = event['end'].strftime('%Y-%m-%d %H:%M') if event['end'] else 'Unknown'

        if event['is_all_day']:
            time_str = f"All day on {event['start'].strftime('%Y-%m-%d')}"
        else:
            time_str = f"{start_str} to {end_str}"

        # Determine if event is in the past
        is_past = False
        if event['start']:
            # Make both datetimes timezone-aware for comparison
            now = datetime.now(timezone.utc)
            event_start = event['start']
            # If event_start is naive, make it UTC-aware
            if event_start.tzinfo is None:
                event_start = event_start.replace(tzinfo=timezone.utc)
            is_past = event_start < now

        timing_note = " [PAST EVENT]" if is_past else " [UPCOMING EVENT]"

        # Format attendees
        attendees_str = ', '.join(event['attendees'][:5]) if event['attendees'] else 'None'
        if len(event['attendees']) > 5:
            attendees_str += f" and {len(event['attendees']) - 5} more"

        formatted = f"""
Title: {event['summary']}
Time: {time_str}{timing_note}
Location: {event['location'] or 'Not specified'}
Attendees: {attendees_str}
Organizer: {event['organizer'] or 'Unknown'}
Status: {event['status']}

Description:
{event['description'][:500] if event['description'] else 'No description'}
"""
        return formatted.strip()


def create_calendar_service(access_token: str) -> CalendarService:
    """
    Factory function to create Calendar service.

    Args:
        access_token: Google OAuth access token

    Returns:
        CalendarService instance
    """
    return CalendarService(access_token)
