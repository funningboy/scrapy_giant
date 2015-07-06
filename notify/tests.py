# -*- coding: utf-8 -*-

# using as celery worker
# main.INSTALLED_APPS has included handler task

import unittest
from datetime import datetime, timedelta
from main.tests import NoSQLTestCase
from notify.tasks import *
import os

skip_tests = {
    'TestNotifyGmail': False,
    'TestNotifyLine': False
}

@unittest.skipIf(skip_tests['TestNotifyGmail'], "skip")
class TestNotifyGmail(NoSQLTestCase):

    def test_on_run(self):
        kwargs = {
            'opt': 'twse',
            'targets': ['gmail'],
            'starttime': datetime.utcnow() - timedelta(days=150),
            'endtime': datetime.utcnow(),
            'base': 'stock',
            'stockids': ['2317', '2330', '1314'],
            'limit': 3,
            'debug': True,
            'cfg': {
                'GMAIL_ACCOUNT': os.environ.get('GMAIL_ACCOUNT', 'null'),
                'GMAIL_PASSWD': os.environ.get('GMAIL_PASSWD', 'null'),
                'GMAIL_RCPT': [
                    'funningboy@gmail.com'
                ]
            }
        }
        collect_ntyitem.delay(**kwargs).get()


@unittest.skipIf(skip_tests['TestNotifyLine'], "skip")
class TestNotifyLine(NoSQLTestCase):

    def test_on_run(self):
        kwargs = {
            'opt': 'twse',
            'targets': ['line'],
            'starttime': datetime.utcnow() - timedelta(days=150),
            'endtime': datetime.utcnow(),
            'base': 'stock',
            'stockids': ['2317', '2330', '1314'],
            'limit': 3,
            'debug': True,
            'cfg': {
                'LINE_ACCOUNT': os.environ.get('LINE_ACCOUNT', 'null'),
                'LINE_PASSWD': os.environ.get('LINE_PASSWD', 'null'),
                'LINE_GROUP': [
                    'stock'
                ]
            }
        }
        collect_ntyitem.delay(**kwargs).get()

