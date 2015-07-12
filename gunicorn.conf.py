from __future__ import absolute_import

import os

bind = '127.0.0.1:8080'
worders = (os.sysconf('SC_NPROCESSORS_ONLN') * 2) + 1
loglevel = 'error'
command = '/root/anaconda/bin/gunicorn'
pythonpath = '/home/sean/prj/giant/scrapy_giant/'
