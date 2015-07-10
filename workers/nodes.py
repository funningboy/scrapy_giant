# -*- coding: utf-8 -*-

import celery as celery

class Node(object):

    def __init__(self, on=False, func=None, args=(), kwargs={}):
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._on = on
        # internal used
        self._visited = 0
        self._rumtime = 0
        self._status = 'idle'
        self._retval = None
        self._asyncresult = None
        if not isinstance(self._func, celery.local.Proxy):
            print "func ptr should been registered at celery tasks list"

    def update_kwargs(self, args=(), kwargs={}):
        self._args = args
        self._kwargs = kwargs

    def run(self):
        if not self._asyncresult:
            self._asyncresult = self._func.delay(*self._args, **self._kwargs)

    def is_ready(self):
        if self._asyncresult:
            return self._asyncresult.ready()

    def is_success(self):
        if self._asyncresult:
            return self._asyncresult.successful()

    @property
    def task_id(self):
        if self._asyncresult:
            return self._asyncresult.task_id
 
    def finish(self):
        self._retval = self._asyncresult.get()
        self._asyncresult = None

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def retval(self):
        return self._retval

    @retval.setter
    def retval(self, retval):
        self._retval = retval

    @property 
    def visited(self):
        return self._visited

    @visited.setter
    def visited(self, visited):
        self._visited = visited

    @property
    def runtime(self):
        return self._rumtime

    @runtime.setter
    def runtime(self, runtime):
        self._rumtime = runtime
