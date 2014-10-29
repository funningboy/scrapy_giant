
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.getcwd())

from celery.schedules import crontab

CELERY_DISABLE_RATE_LIMITS = True
CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": "127.0.0.1",
    "port": 27017,
    "database": "tmp",
    "taskmeta_collection": "twsehiscoll",
}

#used to schedule tasks periodically and passing optional arguments
#Can be very useful. Celery does not seem to support scheduled task but only periodic
CELERYBEAT_SCHEDULE = {
    'run_algorithm_dualema': {
        'task': 'algorithm.tasks.run_',
        'schedule': crontab(minute='*/1'),
        'args': (datetime.utcnow() - timedelta(days=60), datetime.utcnow(), ['2317']),
    },
}
