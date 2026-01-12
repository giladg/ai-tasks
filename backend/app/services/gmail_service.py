from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import base64
import re

from app.config import get_settings
from app.utils.date_utils import format_gmail_date, get_gmail_date_range

settings = get_settings()


class GmailService:
    """Service for interacting with Gmail API"""

    def __init__(self, access_token: str):
        """
        Initialize Gmail service with access token.

        Args:
            access_token: Google OAuth access token
        """
        credentials = Credentials(token=access_token)
        self.service = build('gmail', 'v1', credentials=credentials)

    def fetch_threads(self, days: int = None) -> List[Dict]:
        """
        Fetch Gmail threads from the last N days.

        Args:
            days: Number of days to look back (default: from settings)

        Returns:
            List of thread dictionaries with formatted data
        """
        if days is None:
            days = settings.GMAIL_LOOKBACK_DAYS

        try:
            # Get date range
            start_date, end_date = get_gmail_date_range(days)

            # Build query
            query = f'after:{format_gmail_date(start_date)}'

            # Fetch thread list
            results = self.service.users().threads().list(
                userId='me',
                q=query,
                maxResults=100  # Can be made configurable
            ).execute()

            threads_data = results.get('threads', [])

            if not threads_data:
                return []

            # Fetch full thread details
            threads = []
            for thread_data in threads_data:
                thread_id = thread_data['id']
                thread = self._get_thread_details(thread_id)
                if thread:
                    threads.append(thread)

            return threads

        except HttpError as error:
            print(f"An error occurred fetching Gmail threads: {error}")
            raise

    def _get_thread_details(self, thread_id: str) -> Optional[Dict]:
        """
        Get detailed information about a specific thread.

        Args:
            thread_id: Gmail thread ID

        Returns:
            Dictionary with thread details
        """
        try:
            thread = self.service.users().threads().get(
                userId='me',
                id=thread_id,
                format='full'
            ).execute()

            # Extract messages
            messages = thread.get('messages', [])
            if not messages:
                return None

            # Get first message (thread starter)
            first_message = messages[0]

            # Extract headers
            headers = first_message.get('payload', {}).get('headers', [])
            subject = self._get_header_value(headers, 'Subject') or '(No Subject)'
            from_email = self._get_header_value(headers, 'From') or 'Unknown'
            date_str = self._get_header_value(headers, 'Date')

            # Parse date
            try:
                date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z') if date_str else None
            except:
                date = None

            # Extract body snippets from all messages
            snippets = []
            for msg in messages:
                snippet = msg.get('snippet', '')
                if snippet:
                    snippets.append(snippet)

            # Get full body of first message
            body = self._extract_message_body(first_message)

            # Build Gmail URL
            gmail_url = f"https://mail.google.com/mail/u/0/#inbox/{thread_id}"

            return {
                'thread_id': thread_id,
                'subject': subject,
                'from': from_email,
                'date': date,
                'snippet': ' '.join(snippets[:3]),  # First 3 message snippets
                'body': body,
                'message_count': len(messages),
                'url': gmail_url,
                'labels': thread.get('labelIds', [])
            }

        except HttpError as error:
            print(f"An error occurred fetching thread {thread_id}: {error}")
            return None

    def _get_header_value(self, headers: List[Dict], name: str) -> Optional[str]:
        """
        Get value of a specific header.

        Args:
            headers: List of header dictionaries
            name: Header name to find

        Returns:
            Header value or None
        """
        for header in headers:
            if header.get('name', '').lower() == name.lower():
                return header.get('value')
        return None

    def _extract_message_body(self, message: Dict) -> str:
        """
        Extract body text from a message.

        Args:
            message: Gmail message object

        Returns:
            Message body as plain text
        """
        payload = message.get('payload', {})

        # Try to get body from parts
        if 'parts' in payload:
            return self._extract_body_from_parts(payload['parts'])

        # Try to get body directly
        body_data = payload.get('body', {}).get('data', '')
        if body_data:
            return self._decode_body(body_data)

        return ''

    def _extract_body_from_parts(self, parts: List[Dict]) -> str:
        """
        Recursively extract body from message parts.

        Args:
            parts: List of message parts

        Returns:
            Combined body text
        """
        body_text = ''

        for part in parts:
            mime_type = part.get('mimeType', '')

            # Prefer plain text
            if mime_type == 'text/plain':
                body_data = part.get('body', {}).get('data', '')
                if body_data:
                    body_text += self._decode_body(body_data) + '\n'

            # Recurse into nested parts
            if 'parts' in part:
                body_text += self._extract_body_from_parts(part['parts'])

            # Fall back to HTML if no plain text
            if not body_text and mime_type == 'text/html':
                body_data = part.get('body', {}).get('data', '')
                if body_data:
                    html_text = self._decode_body(body_data)
                    # Simple HTML tag removal
                    body_text += re.sub(r'<[^>]+>', '', html_text) + '\n'

        return body_text.strip()

    def _decode_body(self, body_data: str) -> str:
        """
        Decode base64url encoded body data.

        Args:
            body_data: Base64url encoded string

        Returns:
            Decoded text
        """
        try:
            # Gmail uses URL-safe base64 encoding
            decoded_bytes = base64.urlsafe_b64decode(body_data)
            return decoded_bytes.decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"Error decoding body: {e}")
            return ''

    def format_thread_for_ai(self, thread: Dict) -> str:
        """
        Format thread data for AI consumption.

        Args:
            thread: Thread dictionary

        Returns:
            Formatted string for Gemini
        """
        formatted = f"""
Subject: {thread['subject']}
From: {thread['from']}
Date: {thread['date'].strftime('%Y-%m-%d %H:%M') if thread['date'] else 'Unknown'}
Messages: {thread['message_count']}

{thread['snippet']}

---
Full body (first message):
{thread['body'][:1000]}  # Limit body length
"""
        return formatted.strip()


def create_gmail_service(access_token: str) -> GmailService:
    """
    Factory function to create Gmail service.

    Args:
        access_token: Google OAuth access token

    Returns:
        GmailService instance
    """
    return GmailService(access_token)
