# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.getcwd())

from celery.schedules import crontab

from query.iddb_query import (TwseIdDBQuery, OtcIdDBQuery)

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

# used to schedule tasks periodically and passing optional arguments
# Can be very useful. Celery does not seem to support scheduled task
# but only periodic
CELERYBEAT_SCHEDULE = {
    'run_scrapy_service_twseid': {
        'task': 'bin.tasks.run_scrapy_service',
        'schedule': crontab(minute=0, hour='*/8'),
        'args': (
            'twseid',
            'INFO',
            "./log/%s_%s.log" % ('twseid', datetime.today().strftime("%Y%m%d_%H%M")),
            True,
            debug
        )
    },
    'run_scrapy_service_otcid': {
        'task': 'bin.tasks.run_scrapy_service',
        'schedule': crontab(minute=0, hour='*/8'),
        'args': (
            'otcid',
            'INFO',
            "./log/%s_%s.log" % ('otcid', datetime.today().strftime("%Y%m%d_%H%M")),
            True,
            debug
        )
    },
    'run_scrapy_service_twsehistrader': {
        'task': 'bin.tasks.run_scrapy_service',
        'schedule': crontab(minute=0, hour='*/8'),
        'args': (
            'twsehistrader',
            'INFO',
            "./log/%s_%s.log" % ('twsehistrader', datetime.today().strftime("%Y%m%d_%H%M")),
            True,
            debug
        )
    },
    'run_scrapy_service_twsehisstock': {
        'task': 'bin.tasks.run_scrapy_service',
        'schedule': crontab(minute=0, hour='*/8'),
        'args': (
            'twsehisstock',
            'INFO',
            "./log/%s_%s.log" % ('twsehisstock', datetime.today().strftime("%Y%m%d_%H%M")),
            True,
            debug
        )
    },
    'run_scrapy_service_otchistrader': {
        'task': 'bin.tasks.run_scrapy_service',
        'schedule': crontab(minute=0, hour='*/8'),
        'args': (
            'otchistrader',
            'INFO',
            "./log/%s_%s.log" % ('otchistrader', datetime.today().strftime("%Y%m%d_%H%M")),
            True,
            debug
        )
    },
    'run_scrapy_service_otchisstock': {
        'task': 'bin.tasks.run_scrapy_service',
        'schedule': crontab(minute=0, hour='*/8'),
        'args': (
            'otchisstock',
            'INFO',
            "./log/%s_%s.log" % ('otchisstock', datetime.today().strftime("%Y%m%d_%H%M")),
            True,
            debug
        )
    },
    'run_algorithm_service_twsedualema': {
        'task': 'bin.tasks.run_algorithm_service',
        'schedule': crontab(minute='*/1'),
        'args': (
            'twse',
            'dualema',
            datetime.utcnow() - timedelta(days=60),
            datetime.utcnow(),
            TwseIdDBQuery().get_stockids(debug),
            [],
            debug
        )
    },
    'run_algorithm_service_otcdualema': {
        'task': 'bin.tasks.run_algorithm_service',
        'schedule': crontab(minute='*/1'),
        'args': (
            'otc',
            'dualema',
            datetime.utcnow() - timedelta(days=60),
            datetime.utcnow(),
            OtcIdDBQuery().get_stockids(debug),
            [],
            debug
        )
    },
    'run_algorithm_service_twsesuperman': {
        'task': 'bin.tasks.run_algorithm_service',
        'schedule': crontab(minute='*/1'),
        'args': (
            'twse',
            'superman',
            datetime.utcnow() - timedelta(days=60),
            datetime.utcnow(),
            TwseIdDBQuery().get_stockids(debug),
            [],
            debug
        )
    },
    'run_algorithm_service_otcsuperman': {
        'task': 'bin.tasks.run_algorithm_service',
        'schedule': crontab(minute='*/1'),
        'args': (
            'otc',
            'superman',
            datetime.utcnow() - timedelta(days=60),
            datetime.utcnow(),
            OtcIdDBQuery().get_stockids(debug),
            [],
            debug
        )
    }
}
