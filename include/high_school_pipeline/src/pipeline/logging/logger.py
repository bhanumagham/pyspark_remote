import logging
import logging.config
import os
from datetime import datetime


def setup_logging(config: dict):
    log_level = config["logging"].get("level", "INFO")
    log_path = config["logging"].get("filepath")
    

    handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "level": log_level,
            "formatter": "default",
        }
    }

    # Add file handler only if file is provided
    if log_path:
        os.makedirs(log_path, exist_ok=True)

        log_file = os.path.join(log_path, f"pipeline_{datetime.now().strftime('%Y-%m-%d')}.log")
        handlers["file"] = {
            "class": "logging.FileHandler",
            "filename": log_file,
            "level": log_level,
            "formatter": "default",
        }

    logging_config = {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            }
        },
        "handlers": handlers,
        "root": {
            "handlers": list(handlers.keys()),
            "level": log_level,
        },
    }

    logging.config.dictConfig(logging_config)


def get_logger(name: str):
    return logging.getLogger(name)