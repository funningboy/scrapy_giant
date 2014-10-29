# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.getcwd())

from celery.schedules import crontab

_rootpath = os.environ.get('ROOTPATH', './tmp')
_dbpath = os.environ.get('DBPATH', _rootpath)
_logpath = os.environ.get('LOGPATH', _rootpath)
_host = os.environ.get('HOSTNAME', 'localhost')
_port = int(os.environ.get('DBPORT', '27017'))
_mongod = os.environ.get('MONGOD', 'mongod')
_debug = os.environ.get('DEBUG', False)
debug = True if _debug else False

CELERY_DISABLE_RATE_LIMITS = True
CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": _host,
    "port": _port,
    "database": _dbpath.replace('.', '').split('/')[-1],
    "taskmeta_collection": "job",
}

CELERY_TIMEZONE = 'UTC'

#used to schedule tasks periodically and passing optional arguments
#Can be very useful. Celery does not seem to support scheduled task but only periodic
CELERYBEAT_SCHEDULE = {
    'run_scrapy_twseid': {
        'task': 'bin.tasks.run_scrapy',
        'schedule': crontab(minute=0, hour='*/8'),
        'args': ('twseid', debug)
    },
    'run_scrapy_otcid': {
        'task': 'bin.tasks.run_scrapy',
        'schedule': crontab(minute=0, hour='*/8'),
        'args': ('otcid', debug)
    },
    'run_scrapy_twsehistrader': {
        'task': 'bin.tasks.run_scrapy',
        'schedule': crontab(minute=0, hour='*/8'),
        'args': ('twsehistrader', debug)
    },
    'run_scrapy_twsehisstock': {
        'task': 'bin.tasks.run_scrapy',
        'schedule': crontab(minute=0, hour='*/8'),
        'args': ('twsehisstock', debug)
    },
    'run_scrapy_otchistrader': {
        'task': 'bin.tasks.run_scrapy',
        'schedule': crontab(minute=0, hour='*/8'),
        'args': ('otchistrader', debug)
    },
    'run_scrapy_otchisstock': {
        'task': 'bin.tasks.run_scrapy',
        'schedule': crontab(minute=0, hour='*/8'),
        'args': ('otchisstock', debug)
    }
}
