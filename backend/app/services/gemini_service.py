import google.generativeai as genai
from typing import List, Dict, Optional
import json
from datetime import datetime, date

from app.config import get_settings

settings = get_settings()

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


class GeminiService:
    """Service for interacting with Gemini API for task extraction"""

    def __init__(self):
        """Initialize Gemini service"""
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)

    def extract_tasks(
        self,
        gmail_threads: List[Dict],
        calendar_events: List[Dict],
        learning_context: Optional[str] = None
    ) -> List[Dict]:
        """
        Extract tasks from Gmail threads and Calendar events using Gemini.

        Args:
            gmail_threads: List of formatted Gmail threads
            calendar_events: List of formatted Calendar events
            learning_context: Optional context from user's edit history

        Returns:
            List of extracted task dictionaries
        """
        # Build prompt
        prompt = self._build_prompt(gmail_threads, calendar_events, learning_context)

        try:
            # Call Gemini API
            response = self.model.generate_content(prompt)

            # Parse response
            tasks = self._parse_response(response.text)

            return tasks

        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return []

    def _build_prompt(
        self,
        gmail_threads: List[Dict],
        calendar_events: List[Dict],
        learning_context: Optional[str]
    ) -> str:
        """
        Build prompt for Gemini task extraction.

        Args:
            gmail_threads: List of Gmail thread dictionaries
            calendar_events: List of Calendar event dictionaries
            learning_context: Optional learning context

        Returns:
            Complete prompt string
        """
        # System instructions
        system_prompt = """You are a task extraction assistant. Your job is to analyze emails and calendar events to identify actionable tasks.

RULES:
1. Extract ONLY concrete, actionable tasks (not informational items or FYIs)
2. A task must require the user to DO something
3. Assign priority based on urgency and importance:
   - urgent: Critical, time-sensitive, or explicitly marked as urgent
   - high: Important but not immediately critical
   - medium: Normal priority tasks
   - low: Nice-to-have, low priority items
4. Infer due dates from:
   - Explicit deadlines mentioned in emails
   - Calendar event dates (meetings often imply preparation tasks)
   - Contextual clues (e.g., "by Friday", "next week")
   - If no clear deadline, leave as null
5. Do NOT extract:
   - Informational emails (newsletters, notifications)
   - Completed past events (unless they imply follow-up actions)
   - Social invitations without action items
   - Automated system messages

OUTPUT FORMAT (must be valid JSON):
Return a JSON array of tasks. Each task must have:
{
  "description": "Clear, concise task description",
  "priority": "low" | "medium" | "high" | "urgent",
  "due_date": "YYYY-MM-DD" or null,
  "source_type": "gmail" | "calendar",
  "source_id": "thread_id or event_id from input"
}

Example output:
[
  {
    "description": "Review and approve Q4 budget proposal",
    "priority": "high",
    "due_date": "2026-01-15",
    "source_type": "gmail",
    "source_id": "thread_123"
  },
  {
    "description": "Prepare slides for team meeting on project status",
    "priority": "medium",
    "due_date": "2026-01-10",
    "source_type": "calendar",
    "source_id": "event_456"
  }
]
"""

        # Learning context section
        context_section = ""
        if learning_context:
            context_section = f"""
## USER LEARNING CONTEXT
Based on the user's past edits, here are patterns to consider:
{learning_context}

Use this to better align your task extraction with the user's preferences.
"""

        # Gmail threads section
        gmail_section = "## EMAILS\n\n"
        if gmail_threads:
            for i, thread in enumerate(gmail_threads[:20], 1):  # Limit to 20 threads
                gmail_section += f"[Email {i}] Thread ID: {thread.get('thread_id')}\n"
                gmail_section += f"{thread.get('formatted', '')}\n"
                gmail_section += "---\n\n"
        else:
            gmail_section += "No emails in this period.\n\n"

        # Calendar events section
        calendar_section = "## CALENDAR EVENTS\n\n"
        if calendar_events:
            for i, event in enumerate(calendar_events[:20], 1):  # Limit to 20 events
                calendar_section += f"[Event {i}] Event ID: {event.get('event_id')}\n"
                calendar_section += f"{event.get('formatted', '')}\n"
                calendar_section += "---\n\n"
        else:
            calendar_section += "No calendar events in this period.\n\n"

        # Task extraction instructions
        extraction_section = """
## YOUR TASK
Analyze the emails and calendar events above. Extract actionable tasks following the rules and output format specified.

Return ONLY the JSON array, no other text or explanation.
"""

        # Combine all sections
        full_prompt = (
            system_prompt +
            context_section +
            gmail_section +
            calendar_section +
            extraction_section
        )

        return full_prompt

    def _parse_response(self, response_text: str) -> List[Dict]:
        """
        Parse Gemini response into task dictionaries.

        Args:
            response_text: Raw response text from Gemini

        Returns:
            List of task dictionaries
        """
        try:
            # Clean response (remove markdown code blocks if present)
            cleaned_text = response_text.strip()

            # Remove markdown code blocks
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]  # Remove ```json
            elif cleaned_text.startswith('```'):
                cleaned_text = cleaned_text[3:]  # Remove ```

            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]  # Remove trailing ```

            cleaned_text = cleaned_text.strip()

            # Parse JSON
            tasks = json.loads(cleaned_text)

            # Validate and normalize tasks
            normalized_tasks = []
            for task in tasks:
                normalized = self._normalize_task(task)
                if normalized:
                    normalized_tasks.append(normalized)

            return normalized_tasks

        except json.JSONDecodeError as e:
            print(f"Error parsing Gemini response as JSON: {e}")
            print(f"Response text: {response_text}")
            return []
        except Exception as e:
            print(f"Error processing Gemini response: {e}")
            return []

    def _normalize_task(self, task: Dict) -> Optional[Dict]:
        """
        Normalize and validate a task dictionary.

        Args:
            task: Raw task dictionary from Gemini

        Returns:
            Normalized task dictionary or None if invalid
        """
        # Required fields
        if 'description' not in task or not task['description']:
            return None

        if 'source_type' not in task or task['source_type'] not in ['gmail', 'calendar']:
            return None

        # Normalize priority
        priority = task.get('priority', 'medium').lower()
        if priority not in ['low', 'medium', 'high', 'urgent']:
            priority = 'medium'

        # Normalize due_date
        due_date = task.get('due_date')
        if due_date:
            try:
                # Validate date format
                datetime.strptime(due_date, '%Y-%m-%d')
            except:
                due_date = None

        return {
            'description': task['description'].strip(),
            'priority': priority,
            'due_date': due_date,
            'source_type': task['source_type'],
            'source_id': task.get('source_id', ''),
        }


# Global service instance
gemini_service = GeminiService()
