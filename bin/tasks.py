# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import subprocess

from celery import Celery

from bin.mongodb_driver import *
from bin.start import *

_rootpath = os.environ.get('ROOTPATH', './tmp')
_dbpath = os.environ.get('DBPATH', _rootpath)
_logpath = os.environ.get('LOGPATH', _rootpath)
_host = os.environ.get('HOSTNAME', 'localhost')
_port = int(os.environ.get('DBPORT', '27017'))
_mongod = os.environ.get('MONGOD', 'mongod')
_debug = os.environ.get('DEBUG', False)

#Specify mongodb host and datababse to connect to
BROKER_URL = 'mongodb://%(host)s:%(port)s/%(db)s' % {
    'host': _host,
    'port': _port,
    'db': _dbpath
}

celery = Celery('bin', broker=BROKER_URL)

#Loads settings for Backend to store results of jobs
celery.config_from_object('bin.celeryconfig')

tasks = [
    'twseid',
    'otcid',
    'twsehistrader',
    'twsehisstock',
    'otchistrader',
    'otchisstock'
]

@celery.task(name='bin.tasks.run_scrapy')
def run_scrapy_twseid(scray, debug=False):
    global tasks
    if scray not in tasks:
        return
    cmd = wap_srapy_cmd(
        spider=scray,
        loglevel='INFO',
        logfile='./log/%s_%s.log' % (datetime.today().strftime("%Y%m%d_%H%M"), scray),
        logen=True,
        debug=debug
    )
    proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    proc.wait()
