from datetime import datetime, timedelta, date
from typing import Tuple


def get_gmail_date_range(days: int = 14) -> Tuple[datetime, datetime]:
    """
    Get date range for Gmail query (last N days).

    Args:
        days: Number of days to look back (default: 14)

    Returns:
        Tuple of (start_datetime, end_datetime)
    """
    end = datetime.utcnow()
    start = end - timedelta(days=days)
    return start, end


def get_calendar_date_range(lookback_days: int = 7, lookforward_days: int = 14) -> Tuple[datetime, datetime]:
    """
    Get date range for Calendar query (past N days + future M days).

    Args:
        lookback_days: Number of days to look back (default: 7)
        lookforward_days: Number of days to look forward (default: 14)

    Returns:
        Tuple of (start_datetime, end_datetime)
    """
    now = datetime.utcnow()
    start = now - timedelta(days=lookback_days)
    end = now + timedelta(days=lookforward_days)
    return start, end


def format_gmail_date(dt: datetime) -> str:
    """
    Format datetime for Gmail API query.

    Args:
        dt: Datetime to format

    Returns:
        Date string in format YYYY/MM/DD
    """
    return dt.strftime('%Y/%m/%d')


def format_calendar_datetime(dt: datetime) -> str:
    """
    Format datetime for Google Calendar API query (RFC3339 format).

    Args:
        dt: Datetime to format

    Returns:
        ISO format datetime string with 'Z' suffix
    """
    return dt.isoformat() + 'Z'


def parse_date_string(date_str: str) -> date:
    """
    Parse date string in various formats to date object.

    Args:
        date_str: Date string (YYYY-MM-DD, YYYY/MM/DD, etc.)

    Returns:
        Date object
    """
    # Try common formats
    formats = [
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%d-%m-%Y',
        '%d/%m/%Y',
        '%m-%d-%Y',
        '%m/%d/%Y',
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    # If none work, raise error
    raise ValueError(f"Unable to parse date string: {date_str}")


def is_token_expired(expires_at: datetime) -> bool:
    """
    Check if OAuth token is expired (with 5 minute buffer).

    Args:
        expires_at: Token expiration datetime

    Returns:
        True if token is expired or about to expire
    """
    buffer = timedelta(minutes=5)
    return datetime.utcnow() >= (expires_at - buffer)
