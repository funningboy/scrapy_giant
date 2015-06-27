# -*- coding: utf-8 -*-

# http://stackoverflow.com/questions/14777910/scrapy-crawl-from-script-always-blocks-script-execution-after-scraping

import argparse
import subprocess
import signal
import socket
import time
import os
import re
from datetime import datetime
import traceback

from mongoengine import *
from bin.mongodb_driver import *


def wap_scrapy_cmd(spider, loglevel, logfile, logen=True, debug=False):
    cmd = (
        'scrapy crawl %(spider)s ' +
        '--loglevel=%(loglevel)s ' +
        '--logfile=%(logfile)s ' +
        '-s LOG_ENABLED=%(logen)s ' +
        '-s GIANT_LIMIT=%(debug)s ' +
        '-s GIANT_DEBUG=%(debug)s') % {
            'spider': spider,
            'loglevel': loglevel,
            'logfile': logfile,
            'logen': 1 if logen else 0,
            'debug': 1 if debug else 0
        }
    print cmd
    return cmd

# update stockids
def spawn_payloads(debug=False):
    procs = []
    cmds = []
    tasks = [
        ['twseid', debug],
        ['otcid', debug]
    ]
    for it in tasks:
        cmds.append(
            wap_scrapy_cmd(
                spider=it[0],
                loglevel='INFO',
                logfile='./log/%s_%s.log' % (datetime.today().strftime("%Y%m%d_%H%M"), it[0]),
                logen=True,
                debug=it[1])
        )
    for cmd in cmds:
        proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if debug:
            for line in proc.stderr:
                print line
        procs.append(proc)
    return procs


def join_payloads(procs):
    for proc in procs:
        proc.communicate()


def spawn_scrapys(debug=False):
    procs = []
    cmds = []
    tasks = [
        ['twsehistrader', debug],
        ['twsehistrader2', debug],
        ['twsehiscredit'. debug],
        ['twsehisstock', debug],
        ['twsehisfuture', debug],
        ['otchistrader', debug],
        ['otchistrader2', debug],
        ['otchiscredit', debug],
        ['otchisstock', debug],
        ['otchisfuture', debug]
    ]
    for it in tasks:
        cmds.append(
            wap_scrapy_cmd(
                spider=it[0],
                loglevel='INFO',
                logfile='./log/%s_%s.log' % (datetime.today().strftime("%Y%m%d_%H%M"), it[0]),
                logen=True,
                debug=it[1])
        )
    for cmd in cmds:
        proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if debug:
            for line in proc.stderr:
                print line
        procs.append(proc)
    return procs


def join_scrapys(procs):
    for proc in procs:
        proc.communicate()


def start_main_service(debug):
    if has_service():
        raise "please turn off mongodb service in debug mode"
    else:
        if debug:
            os.environ['ROOTPATH'] = './tmp'
        else:
            os.environ['ROOTPATH'] = './data'
        os.environ['HOSTNAME'] = 'localhost'
        os.environ['DBPORT'] = '27017'
        os.environ['MONGOD'] = 'mongod'
        update_service()
        proc = start_service()
        return proc


def close_main_service(proc, debug):
    close_service(proc)


def switch(model, db):
    """ switch mongoengine db alias as new one """
    model._meta['db_alias'] = db
    # must set _collection to none so it is re-evaluated
    model._collection = None
    return model


def main(debug):
    proc = start_main_service(debug)
    # 1st update stockids
    sprocs = spawn_payloads(debug)
    join_payloads(sprocs)
    # 2nd update all
    sprocs = spawn_scrapys(debug)
    join_scrapys(sprocs)
    close_main_service(proc, debug)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='crawler twse and otc all stocks/traders info')
    parser.add_argument('--debug', dest='debug', action='store_true', default=False, help='debug mode')
    args = parser.parse_args()
    main(args.debug)
