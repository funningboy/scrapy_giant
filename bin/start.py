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

from bin.mongodb_driver import *

def wap_scrapy_cmd(spider, loglevel, logfile, logen=True, debug=False):
    cmd = (
        'scrapy crawl %(spider)s ' +
        '--loglevel=%(loglevel)s ' +
        '--logfile=%(logfile)s ' +
        '-s LOG_ENABLED=%(logen)s ' +
        '-s GIANT_DEBUG=%(debug)s') % {
            'spider': spider,
            'loglevel': loglevel,
            'logfile': logfile,
            'logen': 1 if logen else 0,
            'debug': 1 if debug else 0
        }
    if debug:
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
        proc.wait()

def spawn_scrapys(debug=False):
    procs = []
    cmds = []
    tasks = [
        ['twsehistrader', debug],
        ['twsehisstock', debug],
        ['otchistrader', debug],
        ['otchisstock', debug]
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
        proc.wait()

def main(debug):
    if debug and has_mongodb_service():
        raise "please turn off mongodb service in debug model"

    if not has_mongodb_service():
        if debug:
            os.environ['ROOTPATH'] = './tmp'
        else:
            os.environ['ROOTPATH'] = './data'
        os.environ['HOSTNAME'] = 'localhost'
        os.environ['DBPORT'] = '27017'
        os.environ['MONGOD'] = 'mongod'

        update_mongodb_service()
        proc = start_mongodb_service()

    # 1st update stockids
    sprocs = spawn_payloads(debug)
    join_payloads(sprocs)

    # 2nd update all
    sprocs = spawn_scrapys(debug)
    join_scrapys(sprocs)

    if not has_mongodb_service():
        close_mongodb_service(proc)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='crawler twse and otc all stocks/traders info')
    parser.add_argument('--debug', dest='debug', action='store_true', help='debug mode')
    args = parser.parse_args()
    main(debug=True if args.debug else False)
