import fcntl
import json
import time

from fastapi import HTTPException

from app.core.config import settings

RATE_LIMIT_FILE = "rate_limit.json"


def check_rate_limit(client_ip: str) -> None:
    path = settings.resolved_data_dir / RATE_LIMIT_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("{}", encoding="utf-8")

    with path.open("r+", encoding="utf-8") as file:
        fcntl.flock(file.fileno(), fcntl.LOCK_EX)
        try:
            content = file.read()
            limits = json.loads(content) if content.strip() else {}

            now = time.time()
            entry = limits.get(client_ip, {"count": 0, "window_start": now})
            window_start = float(entry["window_start"])
            count = int(entry["count"])

            if now - window_start >= settings.rate_limit_window_sec:
                window_start = now
                count = 0

            count += 1
            limits[client_ip] = {"count": count, "window_start": window_start}

            file.seek(0)
            file.truncate()
            file.write(json.dumps(limits))
            file.flush()
        finally:
            fcntl.flock(file.fileno(), fcntl.LOCK_UN)

    if count > settings.rate_limit_requests:
        retry_after = max(1, int(settings.rate_limit_window_sec - (now - window_start)))
        raise HTTPException(
            status_code=429,
            detail={
                "error": "rate_limit_exceeded",
                "message": "Too many requests. Please try again later.",
            },
            headers={"Retry-After": str(retry_after)},
        )
