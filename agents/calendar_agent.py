import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


class CalendarAgent:
    """Simple calendar agent preparing for future API integration."""

    def __init__(self, credentials_file: str = "config/calendar_credentials.json") -> None:
        self.credentials_file = credentials_file
        os.makedirs(os.path.dirname(credentials_file), exist_ok=True)
        if not os.path.exists(credentials_file):
            creds = {"token_path": "secrets/token.json"}
            with open(credentials_file, "w") as f:
                json.dump(creds, f, indent=2)

    def list_events(self, config: Optional[Dict[str, Any]] = None) -> List[Dict[str, str]]:
        """Return simulated calendar events."""
        now = datetime.now()
        return [
            {
                "title": "Porada s týmem",
                "start": now.strftime("%Y-%m-%d %H:%M"),
                "end": (now + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"),
            },
            {
                "title": "Call s klientem",
                "start": (now + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
                "end": (now + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M"),
            },
        ]

    def create_event(
        self,
        title: str,
        start_time: datetime,
        duration_minutes: int = 60,
    ) -> Dict[str, str]:
        """Return a simulated created event."""
        end_time = start_time + timedelta(minutes=duration_minutes)
        return {
            "title": title,
            "start": start_time.strftime("%Y-%m-%d %H:%M"),
            "end": end_time.strftime("%Y-%m-%d %H:%M"),
            "status": "created",
        }
