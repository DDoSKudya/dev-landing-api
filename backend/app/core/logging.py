import logging

from app.core.config import settings


def setup_logging() -> None:
    settings.resolved_logs_dir.mkdir(parents=True, exist_ok=True)

    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()

    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    root.addHandler(stream)

    app_file = logging.FileHandler(settings.resolved_logs_dir / "app.log")
    app_file.setFormatter(formatter)
    root.addHandler(app_file)

    access_logger = logging.getLogger("access")
    access_logger.handlers.clear()
    access_logger.propagate = False
    access_logger.setLevel(level)

    access_file = logging.FileHandler(settings.resolved_logs_dir / "requests.log")
    access_file.setFormatter(formatter)
    access_logger.addHandler(access_file)
