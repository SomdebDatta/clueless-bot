from datetime import datetime, timezone

def get_date():
    return datetime.now(timezone.utc).date().isoformat()