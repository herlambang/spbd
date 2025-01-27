LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {name} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
            "formatter": "verbose",
        },
    },
    "loggers": {
        "spbd": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

LOGGING_PRODUCTION = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {name} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",  # Default is stderr
            "formatter": "verbose",
        },
    },
    "loggers": {
        "spbd": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
