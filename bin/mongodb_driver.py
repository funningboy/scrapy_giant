# -*- coding: utf-8 -*-

# ref : https://github.com/mongodb/mongo-python-driver/blob/master/test/high_availability/ha_tools.py

import subprocess
import signal
import socket
import time
import os
import re
from datetime import datetime
import traceback
# ref : http://api.mongodb.org/python/current/examples/gevent.html
#from gevent import monkey; monkey.patch_socket()
from pymongo import MongoClient

from bin.logger import Logger

__all__ = ['update_mongodb_service', 'has_mongodb_service', 'start_mongodb_service', 'close_mongodb_service', 'connect_mongodb_service']

class MongoDBDriver(object):

    proc = None
    _rootpath = os.environ.get('ROOTPATH', './tmp')
    _dbpath = os.environ.get('DBPATH', _rootpath)
    _logpath = os.environ.get('LOGPATH', _rootpath)
    _host = os.environ.get('HOSTNAME', 'localhost')
    _port = int(os.environ.get('DBPORT', '27017'))
    _mongod = os.environ.get('MONGOD', 'mongod')
#    _set_name = os.environ.get('SETNAME', 'repl0')

    @classmethod
    def update(cls):
        cls._rootpath = os.environ.get('ROOTPATH', './tmp')
        cls._dbpath = os.environ.get('DBPATH', cls._rootpath)
        cls._logpath = os.environ.get('LOGPATH',cls. _rootpath)
        cls._host = os.environ.get('HOSTNAME', 'localhost')
        cls._port = int(os.environ.get('DBPORT', '27017'))
        cls._mongod = os.environ.get('MONGOD', 'mongod')
#       cls._set_name = os.environ.get('SETNAME', 'repl0')

    @classmethod
    def start_proc(cls, wait=4):
        try:
            if not os.path.exists(cls._rootpath):
                os.makedirs(cls._rootpath)
            dtime = datetime.now().strftime("%Y%m%d")
            logfile = "%s/%s_mogodb.log" % (cls._logpath, dtime)
            cmd = [
                cls._mongod,
                '--dbpath', cls._dbpath,
#                '--replSet', cls.set_name,
                '--nojournal', '--oplogSize', '64',
                '--logappend', '--logpath', logfile
            ]
            cmd = ' '.join(cmd)
            Logger.info("%s" % (cmd))
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(wait)
            return proc
        except OSError as e:
            Logger.error("%s" % (e.strerror))
            raise

    @classmethod
    def wait_for_proc(cls, proc, wait=0.25):
        trys = 0
        while proc.poll() is None and trys < 160:
            trys += 1
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                try:
                    soc.connect((cls._host, cls._port))
                    return True
                except (IOError, socket.error) as e:
                    "I/O error({0}): {1}".format(e.errno, e.strerror)
                    Logger.error("%s" % (e.strerror))
                    time.sleep(wait)
                finally:
                    pass
            finally:
                soc.close()
        return False

    @classmethod
    def kill_proc(cls, proc):
        try:
            os.kill(proc.pid, 2)  # 2 as signal.SIGKILL
            return True
        except OSError as e:
            Logger.error("%s" % (e.strerror))
        raise

    @classmethod
    def has_proc(cls):
        try:
            cmd = 'ps -ef | grep mongod'
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.stdout.read(), proc.stderr.read()
            m = re.match(r'mongod.*(--dbpath|--logpath|--replSet|--nojournal).*', stdout)
            return True if m else False
        except OSError as e:
            Logger.error("%s" % (e.strerror))
            raise

    @classmethod
    def kill_procs(cls):
        try:
            cmd = 'ps -ef | grep mongod'
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.stdout.read(), proc.stderr.read()
            for line in stdout.splitlines():
                if re.match(r'.*mongod(?<=--)dbpath', line):
                    pid = int(line.split(None, 1)[0])
                    os.kill(pid, 2)  # 2 as signal.SIGKILL
        except OSError as e:
            Logger.error("%s" % (e.strerror))
            raise

def update_mongodb_service():
    MongoDBDriver.update()

def has_mongodb_service():
    return MongoDBDriver.has_proc()

def start_mongodb_service():
    if not MongoDBDriver.has_proc():
        proc = MongoDBDriver.start_proc()
        if not MongoDBDriver.wait_for_proc(proc):
            Logger.error("%s" % ('wait for mongod service fail'))
            MongoDBDriver.kill_proc(proc)
            raise Exception()
    return proc

def close_mongodb_service(proc):
    MongoDBDriver.kill_proc(proc)

def connect_mongodb_service():
    host = os.environ.get('HOSTNAME', 'localhost')
    port = int(os.environ.get('DBPORT', '27017'))
    #return MongoClient(host, port, use_greenlets=True)
    return MongoClient(host, port)
