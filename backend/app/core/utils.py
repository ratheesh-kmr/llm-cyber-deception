from datetime import datetime, timezone

def utc_now() -> datetime:
    """Returns naive UTC datetime object to ensure compatibility with SQLite/SQLAlchemy."""
    return datetime.now(timezone.utc).replace(tzinfo=None)
