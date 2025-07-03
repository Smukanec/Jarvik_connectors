
from datetime import datetime, timedelta

def list_events():
    # Dummy funkce – simulace událostí
    now = datetime.now()
    return [
        {
            "title": "Porada s týmem",
            "start": now.strftime("%Y-%m-%d %H:%M"),
            "end": (now + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")
        },
        {
            "title": "Call s klientem",
            "start": (now + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
            "end": (now + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")
        }
    ]

def create_event(title, start_time, duration_minutes=60):
    # Dummy funkce – neukládá, jen simuluje vytvoření
    end_time = start_time + timedelta(minutes=duration_minutes)
    return {
        "title": title,
        "start": start_time.strftime("%Y-%m-%d %H:%M"),
        "end": end_time.strftime("%Y-%m-%d %H:%M"),
        "status": "created"
    }
