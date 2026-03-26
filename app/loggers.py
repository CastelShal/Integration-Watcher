import logging, logging.config
import os

# Centralized logging setup for event and webhook routes
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s - %(module)s - %(message)s',
        },
    },
    'handlers': {
        'event_file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/events.log',
            'formatter': 'default',
            'level': logging.INFO,
        },
        'webhook_file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/webhooks.log',
            'formatter': 'default',
            'level': logging.INFO,
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': logging.INFO,
        },
    },
    'loggers': {
        "event_logger" : {
            'handlers': ['event_file', 'console'] if os.getenv('RUNNING_IN_DOCKER') else ['event_file'],
            'level': logging.INFO,
            'propagate': False,
        },
        "webhook_logger" : {
            'handlers': ['webhook_file', 'console'] if os.getenv('RUNNING_IN_DOCKER') else ['webhook_file'],
            'level': logging.INFO,
            'propagate': False,
        },
    },
    })
