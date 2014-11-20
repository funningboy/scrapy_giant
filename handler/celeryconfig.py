# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
import sys

sys.path.insert(0, os.getcwd())

from bin.common import _host, _port, _dbpath, _debug

CELERY_DISABLE_RATE_LIMITS = True
CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    'host': _host,
    'port': _port,
    'database': 'handlertaskdb',
    'taskmeta_collection': 'handlercoll',
}

CELERY_TIMEZONE = 'UTC'
