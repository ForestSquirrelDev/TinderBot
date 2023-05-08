from datetime import datetime

_unix_epoch_datetime = datetime(1970, 1, 1)

def timestamp_milliseconds() -> int:
    return int((datetime.utcnow() - _unix_epoch_datetime).total_seconds() * 1000)

def days_to_milliseconds(days: int) -> int:
    return days * 86400000

def hours_minutes_seconds(divider: str) -> str:
    dt = datetime.now()
    return f"{dt.hour}{divider}{dt.minute}{divider}{dt.second}"
